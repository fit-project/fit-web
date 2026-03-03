from __future__ import annotations

import json
import os
import subprocess
import types
from pathlib import Path

import pytest

from fit_web import os_proxy_setup as proxy_setup
from fit_web.os_proxy_setup import ProxyState
from fit_web.os_proxy_setup.macos.proxy import MacProxyManager


@pytest.mark.unit
def test_get_proxy_manager_for_macos_without_service(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(proxy_setup, "get_platform", lambda: "macos")
    monkeypatch.setattr(MacProxyManager, "detect_service", staticmethod(lambda: None))
    assert proxy_setup.get_proxy_manager() is None


@pytest.mark.unit
def test_get_proxy_manager_for_macos_with_service(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(proxy_setup, "get_platform", lambda: "macos")
    monkeypatch.setattr(
        MacProxyManager, "detect_service", staticmethod(lambda: "Wi-Fi")
    )
    manager = proxy_setup.get_proxy_manager()
    assert isinstance(manager, MacProxyManager)
    assert manager.service == "Wi-Fi"


@pytest.mark.unit
def test_get_proxy_manager_for_windows(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(proxy_setup, "get_platform", lambda: "win")
    manager = proxy_setup.get_proxy_manager()
    assert manager.__class__.__name__ == "WinProxyManager"


@pytest.mark.unit
def test_get_proxy_manager_for_linux(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(proxy_setup, "get_platform", lambda: "linux")
    manager = proxy_setup.get_proxy_manager()
    assert manager.__class__.__name__ == "LinuxProxyManager"


@pytest.mark.unit
def test_get_proxy_manager_for_unsupported_platform(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(proxy_setup, "get_platform", lambda: "plan9")
    assert proxy_setup.get_proxy_manager() is None


@pytest.mark.unit
def test_detect_service_prefers_wifi(monkeypatch: pytest.MonkeyPatch) -> None:
    class _Result:
        stdout = "An asterisk (*) denotes disabled services.\nWi-Fi\nEthernet\n"

    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: _Result(),
    )
    assert MacProxyManager.detect_service() == "Wi-Fi"


@pytest.mark.unit
def test_detect_service_fallback_first(monkeypatch: pytest.MonkeyPatch) -> None:
    class _Result:
        stdout = "Thunderbolt Bridge\nUSB 10/100/1000 LAN\n"

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: _Result())
    assert MacProxyManager.detect_service() == "Thunderbolt Bridge"


@pytest.mark.unit
def test_detect_service_returns_none_on_command_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _raise(*_args, **_kwargs):
        raise subprocess.CalledProcessError(1, "networksetup")

    monkeypatch.setattr(subprocess, "run", _raise)
    assert MacProxyManager.detect_service() is None


@pytest.mark.unit
def test_persist_proxy_state_writes_expected_payload(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FIT_USER_APP_PATH", str(tmp_path))
    monkeypatch.setattr(proxy_setup, "get_platform", lambda: "macos")
    state = ProxyState(
        web_enabled=True,
        web_host="127.0.0.1",
        web_port=9090,
        secure_enabled=True,
        secure_host="127.0.0.1",
        secure_port=9090,
        auto_enabled=False,
        auto_url=None,
        bypass_domains=["localhost"],
    )
    manager = types.SimpleNamespace(service="Wi-Fi")

    assert proxy_setup.persist_proxy_state(manager, state) is True

    payload = json.loads((tmp_path / "proxy_state.json").read_text(encoding="utf-8"))
    assert payload["platform"] == "macos"
    assert payload["service"] == "Wi-Fi"
    assert payload["state"]["web_port"] == 9090


@pytest.mark.unit
def test_restore_persisted_proxy_state_replays_snapshot(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FIT_USER_APP_PATH", str(tmp_path))
    (tmp_path / "proxy_state.json").write_text(
        json.dumps(
            {
                "platform": "macos",
                "service": "Wi-Fi",
                "state": {
                    "web_enabled": True,
                    "web_host": "127.0.0.1",
                    "web_port": 9090,
                    "secure_enabled": False,
                    "secure_host": None,
                    "secure_port": None,
                    "auto_enabled": False,
                    "auto_url": None,
                    "bypass_domains": ["localhost"],
                },
            }
        ),
        encoding="utf-8",
    )
    restored: list[ProxyState] = []

    class _Manager:
        def __init__(self, service: str) -> None:
            self.service = service

        def restore(self, state: ProxyState) -> None:
            restored.append(state)

    monkeypatch.setattr(MacProxyManager, "restore", _Manager.restore)
    monkeypatch.setattr(MacProxyManager, "__init__", _Manager.__init__)

    assert proxy_setup.restore_persisted_proxy_state() is True
    assert restored
    assert not (tmp_path / "proxy_state.json").exists()


@pytest.mark.unit
def test_launch_proxy_restore_watchdog_starts_detached_process(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FIT_USER_APP_PATH", str(tmp_path))
    (tmp_path / "proxy_state.json").write_text("{}", encoding="utf-8")
    popen_calls: list[dict[str, object]] = []

    monkeypatch.setattr(proxy_setup.sys, "frozen", False, raising=False)

    def _popen(cmd, **kwargs):
        popen_calls.append({"cmd": cmd, "kwargs": kwargs})
        return types.SimpleNamespace(pid=123)

    monkeypatch.setattr(proxy_setup.subprocess, "Popen", _popen)
    assert proxy_setup.launch_proxy_restore_watchdog() is True
    assert popen_calls
    env = popen_calls[0]["kwargs"]["env"]
    assert env["FIT_PROXY_RESTORE_WATCHDOG"] == "1"
    assert env["FIT_PROXY_RESTORE_PARENT_PID"] == str(os.getpid())


@pytest.mark.unit
def test_run_proxy_restore_watchdog_restores_after_parent_exit(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FIT_USER_APP_PATH", str(tmp_path))
    (tmp_path / "proxy_state.json").write_text("{}", encoding="utf-8")
    pid_checks = iter([True, False])
    restore_calls: list[bool] = []

    monkeypatch.setattr(proxy_setup, "_pid_exists", lambda _pid: next(pid_checks))
    monkeypatch.setattr(proxy_setup.time, "sleep", lambda _secs: None)
    monkeypatch.setattr(
        proxy_setup,
        "restore_persisted_proxy_state",
        lambda: restore_calls.append(True) or True,
    )

    assert proxy_setup.run_proxy_restore_watchdog(999, poll_interval=0) == 0
    assert restore_calls == [True]


@pytest.mark.unit
def test_run_proxy_restore_watchdog_exits_when_state_file_removed(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FIT_USER_APP_PATH", str(tmp_path))
    state_path = tmp_path / "proxy_state.json"
    state_path.write_text("{}", encoding="utf-8")
    pid_checks = iter([True])
    restore_calls: list[bool] = []

    def _pid_exists(_pid: int) -> bool:
        if state_path.exists():
            state_path.unlink()
        return next(pid_checks)

    monkeypatch.setattr(proxy_setup, "_pid_exists", _pid_exists)
    monkeypatch.setattr(
        proxy_setup,
        "restore_persisted_proxy_state",
        lambda: restore_calls.append(True) or True,
    )

    assert proxy_setup.run_proxy_restore_watchdog(999, poll_interval=0) == 0
    assert restore_calls == []
