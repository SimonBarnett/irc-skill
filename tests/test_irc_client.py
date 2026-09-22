"""No-network unit tests for irc-skill client config (P2)."""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLIENT = ROOT / "scripts" / "irc_client.py"
sys.path.insert(0, str(ROOT / "scripts"))
import irc_client as mod  # noqa: E402


def test_tls_for_port_6697():
    assert mod.tls_for(6697, False, False) is True
    assert mod.tls_for(6667, False, False) is False
    assert mod.tls_for(6667, True, False) is True
    assert mod.tls_for(6697, False, True) is False


def test_dry_run_subprocess_no_password():
    env = os.environ.copy()
    for key in list(env):
        if key.startswith("AGENTIC_IRC_"):
            del env[key]
    proc = subprocess.run(
        [sys.executable, str(CLIENT), "--dry-run", "--host", "example.test", "--port", "6697"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert proc.returncode == 0
    out = proc.stdout + proc.stderr
    assert "example.test:6697" in out
    assert "PASSWORD" not in out.upper()


def test_dry_run_agentic_compose_flag():
    env = os.environ.copy()
    for key in list(env):
        if key.startswith("AGENTIC_IRC_"):
            del env[key]
    proc = subprocess.run(
        [
            sys.executable,
            str(CLIENT),
            "--dry-run",
            "--agentic-compose",
            "--host",
            "example.test",
            "--port",
            "6697",
        ],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert proc.returncode == 0
    assert "agentic-compose" in proc.stdout


def test_compose_scripts_present():
    root = ROOT / "scripts"
    assert (root / "agentic_compose.py").is_file()
    assert (root / "irc_seal.py").is_file()
    assert (root / "irc_filexfer.py").is_file()


def test_resolve_agentic_scripts_when_installed():
    mod_path = ROOT / "scripts" / "agentic_compose.py"
    spec = importlib.util.spec_from_file_location("agentic_compose", mod_path)
    assert spec and spec.loader
    ac = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ac)
    path = ac.resolve_agentic_scripts()
    # Optional on CI; on dev boxes with agentic-irc skill it should resolve.
    if path is not None:
        assert (path / "seal.py").is_file()


def test_format_incoming_privmsg():
    line = ":alice!u@h PRIVMSG #bobiverse :hello"
    prefix, cmd, args, trailing = mod.parse_irc_line(line)
    out = mod.format_incoming_chat(cmd, prefix, args, trailing)
    assert out == "FROM alice #bobiverse hello"


def test_on_line_prints_privmsg_without_compose(capsys):
    cfg = mod.ClientConfig(
        host="h",
        port=6697,
        nick="bot",
        password="",
        tls=True,
        realname="bot",
        channel="#chan",
    )
    session = mod.IrcSession(cfg, agentic_compose=False)
    session.on_line(":bob!u@h PRIVMSG #chan :ping")
    captured = capsys.readouterr()
    assert "FROM bob #chan ping" in captured.out


def test_user_input_to_wire_channel():
    assert mod.user_input_to_wire("hi there", "#bobiverse") == "PRIVMSG #bobiverse :hi there"
    assert mod.user_input_to_wire("PRIVMSG #x :y", "#bobiverse") == "PRIVMSG #x :y"
    assert mod.user_input_to_wire("/msg simon hello", "#bobiverse") == "PRIVMSG simon :hello"


def test_missing_host_port_exit_2():
    env = os.environ.copy()
    for key in list(env):
        if key.startswith("AGENTIC_IRC_"):
            del env[key]
    proc = subprocess.run(
        [sys.executable, str(CLIENT), "--dry-run"],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert proc.returncode == 2


def _test_config(nick: str = "fleetseat") -> mod.ClientConfig:
    return mod.ClientConfig(
        host="example.test",
        port=6667,
        nick=nick,
        password="",
        tls=False,
        realname=nick,
        channel="",
    )


class _CaptureSock:
    def __init__(self, recv_chunks: list[bytes]) -> None:
        self.sent: list[str] = []
        self._chunks = list(recv_chunks)
        self._lock = threading.Lock()

    def sendall(self, data: bytes) -> None:
        self.sent.append(data.decode("utf-8"))

    def recv(self, _n: int) -> bytes:
        with self._lock:
            if self._chunks:
                return self._chunks.pop(0)
        return b""


def test_alternate_nick_appends_l():
    assert mod.alternate_nick("bob") == "bob_l"


def test_433_then_001_continues_with_alt_nick():
    cfg = _test_config("fleetseat")
    session = mod.IrcSession(cfg)
    sock = _CaptureSock([])
    session.sock = sock
    session.on_line(":srv 433 * fleetseat :Nickname is already in use")
    assert not session.stop.is_set()
    assert session.nick == "fleetseat_l"
    assert any("NICK fleetseat_l" in line for line in sock.sent)
    session.on_line(":srv 001 fleetseat_l :Welcome")
    assert session.registered.is_set()
    assert not session.stop.is_set()


def test_433_twice_stops():
    cfg = _test_config()
    session = mod.IrcSession(cfg)
    session.sock = _CaptureSock([])
    session.on_line(":srv 433 * fleetseat :in use")
    session.on_line(":srv 433 * fleetseat_l :still in use")
    assert session.stop.is_set()


def test_464_fails_closed_on_line():
    cfg = _test_config()
    session = mod.IrcSession(cfg)
    session.sock = _CaptureSock([])
    session.on_line(":srv 464 * :Password incorrect")
    assert session.stop.is_set()
    assert not session.registered.is_set()


def test_464_run_exits_nonzero(monkeypatch):
    chunk = b":srv 464 * :Password incorrect\r\n"

    def fake_connect(_cfg: mod.ClientConfig) -> _CaptureSock:
        return _CaptureSock([chunk])

    monkeypatch.setattr(mod, "connect_socket", fake_connect)
    session = mod.IrcSession(_test_config())
    code = session.run()
    assert code != 0
