"""Compose with SimonBarnett/agentic_irc for SEAL v2 and FILE v1 (issue #5).

Does not vendor crypto or replace the fleet connector; resolves ~/.grok/skills/agentic-irc/scripts
or AGENTIC_IRC_REPO and delegates / imports there.
"""
from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Callable

SendFn = Callable[[str], None]


def grok_home() -> Path:
    return Path(os.environ.get("GROK_HOME", Path.home() / ".grok")).expanduser()


def agentic_home() -> Path:
    raw = os.environ.get("AGENTIC_IRC_HOME")
    if raw:
        return Path(raw).expanduser()
    return Path.home() / ".agentic-irc"


def resolve_agentic_scripts() -> Path | None:
    candidates: list[Path] = []
    repo = os.environ.get("AGENTIC_IRC_REPO", "").strip()
    if repo:
        candidates.append(Path(repo).expanduser() / "scripts")
    candidates.append(grok_home() / "skills" / "agentic-irc" / "scripts")
    here = Path(__file__).resolve().parent
    candidates.append(here.parent.parent / "agentic_irc" / "scripts")
    for path in candidates:
        if (path / "seal.py").is_file() and (path / "filexfer.py").is_file():
            return path
    return None


def delegate_to_agentic(script: str, argv: list[str]) -> int:
    scripts = resolve_agentic_scripts()
    if scripts is None:
        print(
            "INFO irc-skill: agentic_irc scripts not found. "
            "Install agentic-irc skill (python scripts/install_skill.py in that repo) "
            "or set AGENTIC_IRC_REPO to a clone.",
            file=sys.stderr,
        )
        return 2
    target = scripts / script
    proc = subprocess.run([sys.executable, str(target), *argv], check=False)
    return int(proc.returncode)


def take_outbox_lines(path: Path, last: int) -> tuple[list[str], int]:
    try:
        data = path.read_bytes()
    except OSError:
        return [], last
    if last > len(data):
        last = 0
    buf = data[last:]
    lines: list[str] = []
    consumed = 0
    while True:
        nl = buf.find(b"\n", consumed)
        if nl < 0:
            break
        raw = buf[consumed:nl].rstrip(b"\r")
        text = raw.decode("utf-8", "replace").strip()
        if text:
            lines.append(text)
        consumed = nl + 1
    return lines, last + consumed


def outbox_pos_path(outbox: Path) -> Path:
    return Path(str(outbox) + ".pos")


def load_outbox_pos(outbox: Path) -> int:
    p = outbox_pos_path(outbox)
    if not p.exists():
        return 0
    try:
        n = int(p.read_text(encoding="utf-8").strip() or "0")
    except (ValueError, OSError):
        return 0
    return n if n >= 0 else 0


def save_outbox_pos(outbox: Path, pos: int) -> None:
    outbox_pos_path(outbox).write_text(str(int(pos)) + "\n", encoding="utf-8")


class AgenticCompose:
    """SEAL/FILE receive + outbox send using agentic_irc modules."""

    def __init__(self, nick: str, channel: str, send: SendFn) -> None:
        self.nick = nick
        self.channel = channel
        self.send = send
        self.home = agentic_home()
        self.outbox = self.home / "outbox.txt"
        self.inbox = self.home / "inbox"
        self.inbox.mkdir(parents=True, exist_ok=True)
        scripts = resolve_agentic_scripts()
        if scripts is None:
            raise RuntimeError("agentic_irc scripts not found")
        if str(scripts) not in sys.path:
            sys.path.insert(0, str(scripts))
        import seal  # noqa: WPS433
        import wire  # noqa: WPS433
        import filexfer  # noqa: WPS433
        import protect  # noqa: WPS433

        self._seal = seal
        self._wire = wire
        self._filexfer = filexfer
        self._protect = protect
        self.fragments = seal.FragmentStore()
        self.file_bags = filexfer.FileBag()
        self.peers = seal.load_peers()
        try:
            self.ident = seal.load_ident()
        except SystemExit:
            self.ident = None
        self._stop = threading.Event()

    def info(self, msg: str) -> None:
        print(msg, file=sys.stderr, flush=True)

    def say(self, msg: str) -> None:
        ch = self.channel
        if not ch.startswith("#"):
            ch = "#" + ch.lstrip("#")
        self.send(f"PRIVMSG {ch} :{msg}")

    def _file_outbox(self, line: str) -> None:
        with self.outbox.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    def _finish_file(self, fid: str, sha: str, data: bytes | None) -> None:
        if data is None:
            self.info(f"INFO file DONE id={fid} fail (incomplete)")
            return
        offer = self.file_bags._offers.get(fid.lower(), {})
        name = offer.get("name") or "file.bin"
        expect = offer.get("sha") or sha
        if self._filexfer.complete_write(self.home, fid, name, data, expect):
            self.info(f"INFO file DONE id={fid} ok")
        else:
            self.info(f"INFO file DONE id={fid} fail")

    def _take_airc_file(self, msg_id: str, pt: bytes) -> bool:
        if not pt.startswith(b"AIRC-FILE v1"):
            return False
        env = self._filexfer.decode_airc_file(pt)
        if env is None:
            self.info(f"INFO file DONE id={msg_id} fail")
            return True
        offer = self.file_bags._offers.get(msg_id.lower(), {})
        if offer:
            if offer.get("sha") and str(offer["sha"]).lower() != env["sha256"]:
                self.info(f"INFO file DONE id={msg_id} fail")
                return True
        if self._filexfer.complete_write(
            self.home, msg_id, env["name"], env["data"], env["sha256"]
        ):
            self.info(f"INFO file DONE id={msg_id} ok (tier S)")
        else:
            self.info(f"INFO file DONE id={msg_id} fail")
        return True

    def handle_file(self, src: str, body: str) -> None:
        fl = self._wire.parse_file_line(body)
        if not fl:
            return
        if fl.verb == "OFFER":
            name = fl.fields[-1] if fl.fields else ""
            nbytes = fl.fields[3] if len(fl.fields) > 3 else ""
            sha = fl.fields[4] if len(fl.fields) > 4 else ""
            tier = fl.fields[5] if len(fl.fields) > 5 else ""
            if not fl.file_id:
                return
            if not self.file_bags.note_offer(src, fl.file_id, name, sha, nbytes, tier):
                self.info(f"INFO file OFFER id={fl.file_id} ignored (duplicate)")
                return
            self.info(f"INFO file OFFER id={fl.file_id} name={name} bytes={nbytes}")
            extra = 0
            try:
                extra = int(nbytes or 0)
            except (TypeError, ValueError):
                extra = 0
            if self._filexfer.would_exceed_cap(self.home, extra=extra):
                self._file_outbox(f"FILE v1 REFUSE {fl.file_id} :disk")
            else:
                self._file_outbox(f"FILE v1 ACCEPT {fl.file_id}")
        if fl.verb == "CHUNK" and fl.chunk_b64 and fl.i and fl.n and fl.file_id:
            data = self.file_bags.add_chunk(src, fl.file_id, fl.i, fl.n, fl.chunk_b64)
            if data is not None:
                pending = self.file_bags.take_pending_done(fl.file_id)
                if pending is not None:
                    self._finish_file(
                        fl.file_id,
                        pending,
                        self.file_bags.take_assembled(fl.file_id) or data,
                    )
        if fl.verb == "ABORT" and fl.file_id:
            self.file_bags.abort(fl.file_id)
            self.info(f"INFO file ABORT id={fl.file_id}")
        if fl.verb == "DONE" and fl.file_id:
            sha = fl.fields[1] if len(fl.fields) > 1 else ""
            data = self.file_bags.peek_assembled(fl.file_id)
            if data is None:
                self.file_bags.note_done(fl.file_id, sha)
                self.info(f"INFO file DONE id={fl.file_id} wait (incomplete)")
                return
            self._finish_file(fl.file_id, sha, self.file_bags.take_assembled(fl.file_id))

    def handle_privmsg(self, prefix: str, target: str, body: str) -> None:
        src = prefix.split("!", 1)[0].lstrip(":")
        tgt_l = target.lower()
        ch = self.channel if self.channel.startswith("#") else "#" + self.channel.lstrip("#")
        to_channel = tgt_l == ch.lower()
        to_me = tgt_l == self.nick.lower()
        if not to_channel and not to_me:
            return
        pk = self._seal.parse_agpk_line(body)
        if pk is not None:
            result = self._seal.tofu_pin(self.peers, src, pk)
            if result == "pinned":
                self._seal.save_peers(self.peers)
                self.info(f"INFO peer {src} AGPK pinned")
            elif result == "mismatch":
                self.info(f"INFO peer {src} AGPK mismatch (ignored)")
            return
        parsed = self._seal.parse_seal_line(body)
        if parsed is None:
            self.handle_file(src, body)
            return
        if parsed.version == 2 and parsed.from_nick and parsed.from_nick.lower() != src.lower():
            self.info("INFO SEAL prefix != from_nick, drop")
            return
        if parsed.to_nick.lower() != self.nick.lower():
            return
        if parsed.version != 2:
            self.info(f"INFO SEAL {parsed.msg_id} v1 ignored")
            return
        payload = self.fragments.add(parsed)
        if payload is None:
            return
        if self.ident is None:
            self.info(f"INFO SEAL {parsed.msg_id} dropped (no identity; run agentic seal genkey)")
            return
        try:
            blob = self._seal.b64d(payload)
            from_nick = parsed.from_nick or src
            pin = self.peers.get(from_nick.lower(), {}).get("pk")
            if not pin:
                self.info(f"INFO SEAL {parsed.msg_id} dropped (no AGPK pin for {from_nick})")
                return
            pt = self._seal.open_bytes_v2(
                blob,
                self.ident,
                ch,
                parsed.to_nick,
                from_nick,
                parsed.msg_id,
                pin,
            )
        except Exception as e:
            self.info(f"INFO SEAL {parsed.msg_id} decrypt failed {type(e).__name__}")
            return
        if self._take_airc_file(parsed.msg_id, pt):
            return
        dest = self.inbox / f"{parsed.msg_id}.bin"
        if dest.exists():
            self.info(f"INFO SEAL {parsed.msg_id} inbox id exists, skip write")
            return
        dest.write_bytes(pt)
        self._protect.protect_path(dest)
        self.info(f"INFO SEAL {parsed.msg_id} -> inbox ({len(pt)} bytes)")

    def drain_outbox_once(self) -> None:
        path = self.outbox
        if not path.exists():
            return
        last = load_outbox_pos(path)
        lines, new_last = take_outbox_lines(path, last)
        for line in lines:
            if line.startswith("PRIVMSG "):
                self.send(line)
            else:
                self.say(line)
            time.sleep(0.35)
        if new_last != last:
            save_outbox_pos(path, new_last)

    def outbox_loop(self) -> None:
        while not self._stop.is_set():
            try:
                self.drain_outbox_once()
            except OSError:
                pass
            time.sleep(1.0)

    def stop(self) -> None:
        self._stop.set()


def compose_available() -> bool:
    return resolve_agentic_scripts() is not None
