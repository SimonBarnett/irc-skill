#!/usr/bin/env python3
"""Thin IRC client entry for irc-skill (P2). Env/CLI only; no exe drop."""
from __future__ import annotations

import argparse
import os
import signal
import socket
import ssl
import sys
import threading
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class ClientConfig:
    host: str
    port: int
    nick: str
    password: str
    tls: bool
    realname: str
    channel: str


def _env_str(key: str) -> str | None:
    v = (os.environ.get(key) or "").strip()
    return v or None


def _env_port() -> int | None:
    raw = _env_str("AGENTIC_IRC_PORT")
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        return None


def tls_for(port: int, tls_flag: bool, no_tls_flag: bool) -> bool:
    if no_tls_flag:
        return False
    if tls_flag:
        return True
    return port == 6697


def resolve_config(args: argparse.Namespace) -> ClientConfig | None:
    host = (args.host or _env_str("AGENTIC_IRC_HOST") or "").strip()
    port = args.port or _env_port() or 0
    nick = (args.nick or _env_str("AGENTIC_IRC_NICK") or "").strip()
    password = (args.password or _env_str("AGENTIC_IRC_PASSWORD") or "").strip()
    if not host or not port:
        return None
    use_tls = tls_for(port, bool(args.tls), bool(args.no_tls))
    channel = (args.channel or "").strip()
    realname = (args.realname or nick or "irc-skill").strip()
    return ClientConfig(
        host=host,
        port=port,
        nick=nick,
        password=password,
        tls=use_tls,
        realname=realname or "irc-skill",
        channel=channel,
    )


def dry_run_message(cfg: ClientConfig, agentic_compose: bool = False) -> str:
    mode = "tls" if cfg.tls else "plain"
    nick_part = f" nick={cfg.nick}" if cfg.nick else ""
    compose_part = " agentic-compose" if agentic_compose else ""
    return (
        f"INFO target {cfg.host}:{cfg.port} ({mode}){nick_part}{compose_part} "
        f"(dry-run; no connection)"
    )


def connect_socket(cfg: ClientConfig) -> ssl.SSLSocket | socket.socket:
    raw = socket.create_connection((cfg.host, cfg.port), 20)
    raw.settimeout(None)
    if not cfg.tls:
        return raw
    ctx = ssl.create_default_context()
    sock = ctx.wrap_socket(raw, server_hostname=cfg.host)
    sock.settimeout(None)
    return sock


def send_line(sock: ssl.SSLSocket | socket.socket, line: str) -> None:
    sock.sendall((line + "\r\n").encode("utf-8"))


def nick_from_prefix(prefix: str) -> str:
    if not prefix:
        return ""
    return prefix.split("!", 1)[0].lstrip(":")


def format_incoming_chat(cmd: str, prefix: str, args: list[str], trailing: str) -> str | None:
    if cmd not in ("PRIVMSG", "NOTICE") or not args:
        return None
    nick = nick_from_prefix(prefix)
    return f"FROM {nick} {args[0]} {trailing}"


def user_input_to_wire(text: str, default_channel: str) -> str | None:
    line = text.strip()
    if not line:
        return None
    if line.startswith("PRIVMSG "):
        return line
    if line.startswith("/msg "):
        rest = line[5:].strip()
        sp = rest.find(" ")
        if sp < 0:
            return None
        target = rest[:sp]
        body = rest[sp + 1 :].strip()
        if not body:
            return None
        return f"PRIVMSG {target} :{body}"
    if line.startswith("/"):
        return None
    ch = (default_channel or "").strip()
    if not ch:
        return None
    if not ch.startswith("#"):
        ch = "#" + ch.lstrip("#")
    return f"PRIVMSG {ch} :{line}"


def parse_irc_line(line: str) -> tuple[str, str, list[str], str]:
    if not line:
        return "", "", [], ""
    if line[0] == ":":
        sp = line.find(" ")
        if sp < 0:
            return line[1:], "", [], ""
        prefix = line[1:sp]
        rest = line[sp + 1 :]
    else:
        prefix = ""
        rest = line
    if " :" in rest:
        head, trailing = rest.split(" :", 1)
    else:
        head, trailing = rest, ""
    parts = head.split()
    if not parts:
        return prefix, "", [], trailing
    cmd = parts[0]
    args = parts[1:] if len(parts) > 1 else []
    return prefix, cmd, args, trailing


class IrcSession:
    def __init__(self, cfg: ClientConfig, agentic_compose: bool = False) -> None:
        self.cfg = cfg
        self.agentic_compose = agentic_compose
        self.stop = threading.Event()
        self.registered = threading.Event()
        self.sock: ssl.SSLSocket | socket.socket | None = None
        self._compose: object | None = None

    def reader(self) -> None:
        assert self.sock is not None
        buf = b""
        while not self.stop.is_set():
            try:
                chunk = self.sock.recv(4096)
            except OSError:
                break
            if not chunk:
                break
            buf += chunk
            while b"\r\n" in buf:
                raw, buf = buf.split(b"\r\n", 1)
                line = raw.decode("utf-8", errors="replace")
                self.on_line(line)
        self.stop.set()

    def on_line(self, line: str) -> None:
        prefix, cmd, args, trailing = parse_irc_line(line)
        if cmd == "PING":
            payload = trailing or (args[0] if args else "")
            if self.sock:
                send_line(self.sock, "PONG " + payload)
            return
        if cmd == "001" or (cmd.isdigit() and int(cmd) == 1):
            self.registered.set()
            if trailing:
                print(f"FROM server * {trailing}", flush=True)
            return
        if cmd == "JOIN" and args:
            print(f"FROM {nick_from_prefix(prefix)} JOIN {args[0]}", flush=True)
            return
        if cmd in ("PRIVMSG", "NOTICE") and args:
            chat = format_incoming_chat(cmd, prefix, args, trailing)
            if chat:
                print(chat, flush=True)
            if cmd == "PRIVMSG" and self._compose is not None:
                self._compose.handle_privmsg(prefix, args[0], trailing)
            return
        if cmd in ("ERROR", "433", "464"):
            print(f"INFO server {cmd} {trailing or ' '.join(args)}", file=sys.stderr)
            self.stop.set()

    def run(self) -> int:
        if not self.cfg.nick:
            print(
                "INFO irc-skill: nick UNKNOWN. Set AGENTIC_IRC_NICK or pass --nick.",
                file=sys.stderr,
            )
            return 2
        mode = "tls" if self.cfg.tls else "plain"
        print(
            f"INFO connecting {self.cfg.host}:{self.cfg.port} ({mode}) nick={self.cfg.nick}",
            file=sys.stderr,
        )
        self.sock = connect_socket(self.cfg)
        threading.Thread(target=self.reader, daemon=True).start()
        if self.cfg.password:
            send_line(self.sock, "PASS " + self.cfg.password)
        send_line(self.sock, "NICK " + self.cfg.nick)
        send_line(self.sock, f"USER {self.cfg.nick} 0 * :{self.cfg.realname}")
        if not self.registered.wait(30):
            print("INFO NO 001 (registration timeout)", file=sys.stderr)
            self.stop.set()
            return 1
        if self.cfg.channel:
            send_line(self.sock, "JOIN " + self.cfg.channel)
        if self.agentic_compose:
            if not self.cfg.channel:
                print(
                    "INFO irc-skill: --agentic-compose requires --channel for SEAL/FILE wire.",
                    file=sys.stderr,
                )
                self.stop.set()
                return 2
            from agentic_compose import AgenticCompose

            def _send_raw(raw: str) -> None:
                if self.sock:
                    send_line(self.sock, raw)

            try:
                self._compose = AgenticCompose(self.cfg.nick, self.cfg.channel, _send_raw)
            except RuntimeError as e:
                print(f"INFO {e}", file=sys.stderr)
                self.stop.set()
                return 2
            threading.Thread(target=self._compose.outbox_loop, daemon=True).start()
            print(
                f"INFO agentic-compose on home={self._compose.home} channel={self.cfg.channel}",
                file=sys.stderr,
            )
        print(f"INFO registered as {self.cfg.nick}", file=sys.stderr)
        threading.Thread(target=self._stdin_loop, daemon=True).start()
        if not self.agentic_compose:
            threading.Thread(target=self._outbox_loop, daemon=True).start()
        while not self.stop.is_set():
            time.sleep(0.5)
        return 0

    def _send_user_wire(self, wire: str) -> None:
        if self.sock and wire:
            send_line(self.sock, wire)

    def _stdin_loop(self) -> None:
        for raw in sys.stdin:
            if self.stop.is_set():
                break
            wire = user_input_to_wire(raw, self.cfg.channel)
            if wire:
                self._send_user_wire(wire)

    def _outbox_loop(self) -> None:
        from agentic_compose import (
            agentic_home,
            load_outbox_pos,
            save_outbox_pos,
            take_outbox_lines,
        )

        path = agentic_home() / "outbox.txt"
        while not self.stop.is_set():
            try:
                if not path.exists():
                    time.sleep(1.0)
                    continue
                last = load_outbox_pos(path)
                lines, new_last = take_outbox_lines(path, last)
                for line in lines:
                    wire = user_input_to_wire(line, self.cfg.channel)
                    if wire:
                        self._send_user_wire(wire)
                    time.sleep(0.35)
                if new_last != last:
                    save_outbox_pos(path, new_last)
            except OSError:
                pass
            time.sleep(1.0)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="irc-skill Python IRC client (P2). Host/port/nick/pass from flags or AGENTIC_IRC_* env."
    )
    p.add_argument("--host", default="", help="IRC host (else AGENTIC_IRC_HOST)")
    p.add_argument("--port", type=int, default=0, help="IRC port (else AGENTIC_IRC_PORT)")
    p.add_argument("--nick", default="", help="IRC nick (else AGENTIC_IRC_NICK)")
    p.add_argument("--password", default="", help="IRC PASS (else AGENTIC_IRC_PASSWORD; never logged)")
    p.add_argument("--channel", default="", help="Optional JOIN after 001")
    p.add_argument("--realname", default="", help="USER realname (default nick or irc-skill)")
    p.add_argument("--tls", action="store_true", help="Use TLS (also default for port 6697)")
    p.add_argument("--no-tls", action="store_true", help="Plain socket even on 6697")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print resolved target (no password) and exit 0 without connecting",
    )
    p.add_argument(
        "--agentic-compose",
        action="store_true",
        help="SEAL v2 + FILE v1 via agentic_irc scripts (needs AGENTIC_IRC_HOME identity; --channel)",
    )
    return p


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    cfg = resolve_config(args)
    if cfg is None:
        print(
            "INFO irc-skill: host/port UNKNOWN. "
            "Set AGENTIC_IRC_HOST and AGENTIC_IRC_PORT or pass --host/--port.",
            file=sys.stderr,
        )
        raise SystemExit(2)

    if args.dry_run:
        print(dry_run_message(cfg, bool(args.agentic_compose)))
        raise SystemExit(0)

    session = IrcSession(cfg, agentic_compose=bool(args.agentic_compose))

    def _stop(*_a: object) -> None:
        session.stop.set()

    signal.signal(signal.SIGINT, _stop)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, _stop)
    raise SystemExit(session.run())


if __name__ == "__main__":
    main()
