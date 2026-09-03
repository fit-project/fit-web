from __future__ import annotations

import signal
import subprocess
import threading
import time
from pathlib import Path

import pytest

from fit_web.mitmproxy.runner import MitmproxyRunner


@pytest.mark.unit
def test_runner_init_without_base_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FIT_USER_APP_PATH", raising=False)
    runner = MitmproxyRunner()
    assert runner.output_dir is None
    assert runner.pid_file is None
    assert runner.har_file is None
    assert runner.control_file is None


@pytest.mark.unit
def test_write_control_returns_false_without_control_file(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("FIT_USER_APP_PATH", raising=False)
    runner = MitmproxyRunner()
    assert runner.start_capture() is False
    assert runner.stop_capture() is False


@pytest.mark.unit
def test_stop_capture_waits_for_matching_export_ack(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FIT_USER_APP_PATH", str(tmp_path))
    runner = MitmproxyRunner()

    def _acknowledge() -> None:
        assert runner.control_file is not None
        assert runner.export_status_file is not None
        deadline = time.monotonic() + 1
        while not runner.control_file.exists() and time.monotonic() < deadline:
            time.sleep(0.005)
        token = runner.control_file.read_text().partition(":")[2]
        runner.export_status_file.write_text(f"{token}:ok")

    thread = threading.Thread(target=_acknowledge)
    thread.start()
    assert runner.stop_capture(timeout=1) is True
    thread.join()


@pytest.mark.unit
def test_stop_capture_fails_on_export_error(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FIT_USER_APP_PATH", str(tmp_path))
    runner = MitmproxyRunner()

    def _acknowledge() -> None:
        assert runner.control_file is not None
        assert runner.export_status_file is not None
        while not runner.control_file.exists():
            time.sleep(0.005)
        token = runner.control_file.read_text().partition(":")[2]
        runner.export_status_file.write_text(f"{token}:error")

    thread = threading.Thread(target=_acknowledge)
    thread.start()
    assert runner.stop_capture(timeout=1) is False
    thread.join()


@pytest.mark.unit
def test_stop_by_pid_when_pid_missing(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("FIT_USER_APP_PATH", str(tmp_path))
    runner = MitmproxyRunner()
    assert runner.stop_by_pid() is False


@pytest.mark.unit
def test_stop_by_pid_process_already_gone(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FIT_USER_APP_PATH", str(tmp_path))
    runner = MitmproxyRunner()
    runner.output_dir.mkdir(parents=True, exist_ok=True)
    assert runner.pid_file is not None
    runner.pid_file.write_text("12345", encoding="utf-8")

    def _kill(pid: int, sig: int) -> None:
        raise ProcessLookupError

    monkeypatch.setattr("fit_web.mitmproxy.runner.os.kill", _kill)
    assert runner.stop_by_pid() is True
    assert not runner.pid_file.exists()


@pytest.mark.unit
def test_stop_by_pid_sigkill_fallback(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FIT_USER_APP_PATH", str(tmp_path))
    runner = MitmproxyRunner()
    runner.output_dir.mkdir(parents=True, exist_ok=True)
    assert runner.pid_file is not None
    runner.pid_file.write_text("222", encoding="utf-8")

    calls: list[tuple[int, int]] = []

    def _kill(pid: int, sig: int) -> None:
        calls.append((pid, sig))
        if sig == signal.SIGINT:
            raise OSError("sigint failed")

    monkeypatch.setattr("fit_web.mitmproxy.runner.os.kill", _kill)
    assert runner.stop_by_pid() is True
    assert (222, signal.SIGINT) in calls
    assert (222, signal.SIGKILL) in calls


@pytest.mark.unit
def test_start_returns_none_if_subprocess_exits_immediately(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FIT_USER_APP_PATH", str(tmp_path))
    conf_dir = tmp_path / "mitmproxy" / "conf"
    conf_dir.mkdir(parents=True)
    monkeypatch.setenv("FIT_MITM_CONF_DIR", str(conf_dir))
    monkeypatch.setenv("FIT_MITM_PORT", "9090")

    class _Proc:
        pid = 777
        stdout = None
        stderr = None

        def poll(self):
            return 1

    monkeypatch.setattr("fit_web.mitmproxy.runner.time.sleep", lambda _s: None)
    monkeypatch.setattr(
        "fit_web.mitmproxy.runner.subprocess.Popen",
        lambda *args, **kwargs: _Proc(),
    )
    runner = MitmproxyRunner()
    assert runner.start() is None


@pytest.mark.unit
def test_start_writes_pid_on_success(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("FIT_USER_APP_PATH", str(tmp_path))
    conf_dir = tmp_path / "mitmproxy" / "conf"
    conf_dir.mkdir(parents=True)
    monkeypatch.setenv("FIT_MITM_CONF_DIR", str(conf_dir))
    monkeypatch.setenv("FIT_MITM_PORT", "9090")

    popen_calls: list[list[str]] = []

    class _Proc:
        pid = 555
        stdout = None
        stderr = None

        def poll(self):
            return None

    monkeypatch.setattr("fit_web.mitmproxy.runner.time.sleep", lambda _s: None)
    def _popen(cmd, **_kwargs):
        popen_calls.append(cmd)
        return _Proc()

    monkeypatch.setattr("fit_web.mitmproxy.runner.subprocess.Popen", _popen)
    runner = MitmproxyRunner()
    proc = runner.start()
    assert proc is not None
    assert runner.pid_file is not None
    assert runner.pid_file.read_text(encoding="utf-8").strip() == "555"
    assert not any(argument.startswith("hardump=") for argument in popen_calls[0])
    assert ["--set", f"confdir={conf_dir.resolve()}"] == popen_calls[0][
        popen_calls[0].index(f"confdir={conf_dir.resolve()}") - 1 :
        popen_calls[0].index(f"confdir={conf_dir.resolve()}") + 1
    ]


@pytest.mark.unit
def test_start_kills_existing_pid_before_restarting(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FIT_USER_APP_PATH", str(tmp_path))
    conf_dir = tmp_path / "mitmproxy" / "conf"
    conf_dir.mkdir(parents=True)
    monkeypatch.setenv("FIT_MITM_CONF_DIR", str(conf_dir))

    class _Proc:
        pid = 999
        stdout = None
        stderr = None

        def poll(self):
            return None

    kill_calls: list[tuple[int, int]] = []

    def _kill(pid: int, sig: int) -> None:
        kill_calls.append((pid, sig))

    monkeypatch.setattr("fit_web.mitmproxy.runner.time.sleep", lambda _s: None)
    monkeypatch.setattr("fit_web.mitmproxy.runner.os.kill", _kill)
    monkeypatch.setattr(
        "fit_web.mitmproxy.runner.subprocess.Popen",
        lambda *args, **kwargs: _Proc(),
    )

    runner = MitmproxyRunner()
    runner.output_dir.mkdir(parents=True, exist_ok=True)
    assert runner.pid_file is not None
    runner.pid_file.write_text("321", encoding="utf-8")
    assert runner.start() is not None
    assert (321, 0) in kill_calls
    assert (321, signal.SIGKILL) in kill_calls


@pytest.mark.unit
def test_start_rejects_missing_linux_conf_dir(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FIT_USER_APP_PATH", str(tmp_path))
    monkeypatch.delenv("FIT_MITM_CONF_DIR", raising=False)
    popen_calls: list[bool] = []
    monkeypatch.setattr(
        "fit_web.mitmproxy.runner.subprocess.Popen",
        lambda *_args, **_kwargs: popen_calls.append(True),
    )

    assert MitmproxyRunner().start() is None
    assert popen_calls == []


@pytest.mark.unit
def test_start_rejects_linux_conf_dir_outside_app_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FIT_USER_APP_PATH", str(tmp_path))
    outside = tmp_path / "other-conf"
    outside.mkdir()
    monkeypatch.setenv("FIT_MITM_CONF_DIR", str(outside))

    assert MitmproxyRunner().start() is None


@pytest.mark.unit
def test_stop_terminates_and_clears_pid(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("FIT_USER_APP_PATH", str(tmp_path))
    runner = MitmproxyRunner()
    runner.output_dir.mkdir(parents=True, exist_ok=True)
    assert runner.pid_file is not None
    runner.pid_file.write_text("123", encoding="utf-8")

    class _Proc:
        def __init__(self) -> None:
            self._terminated = False

        def poll(self):
            return None

        def terminate(self):
            self._terminated = True

        def wait(self, timeout: float):
            return 0

    proc = _Proc()
    runner.stop(proc)
    assert not runner.pid_file.exists()


@pytest.mark.unit
def test_stop_forces_kill_on_timeout(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("FIT_USER_APP_PATH", str(tmp_path))
    runner = MitmproxyRunner()

    class _Proc:
        def __init__(self) -> None:
            self.killed = False

        def poll(self):
            return None

        def terminate(self):
            return None

        def wait(self, timeout: float):
            raise subprocess.TimeoutExpired("p", timeout)

        def kill(self):
            self.killed = True

    proc = _Proc()
    runner.stop(proc)
    assert proc.killed is True
