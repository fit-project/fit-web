from __future__ import annotations

import subprocess

import pytest

from fit_web import os_proxy_setup as proxy_setup
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
