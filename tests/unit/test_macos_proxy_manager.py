from __future__ import annotations

import subprocess

import pytest

from fit_web.os_proxy_setup import ProxyState
from fit_web.os_proxy_setup.macos.proxy import MacProxyManager


@pytest.mark.unit
def test_parse_enabled_and_port_helpers() -> None:
    manager = MacProxyManager("Wi-Fi")
    assert manager._parse_enabled("Enabled: Yes") is True
    assert manager._parse_enabled("Enabled: No") is False
    assert manager._parse_port("8080") == 8080
    assert manager._parse_port("abc") is None
    assert manager._parse_value("Server: 127.0.0.1", "Server") == "127.0.0.1"


@pytest.mark.unit
def test_snapshot_success(monkeypatch: pytest.MonkeyPatch) -> None:
    manager = MacProxyManager("Wi-Fi")
    monkeypatch.setattr(manager, "_get_web_proxy", lambda: (True, "127.0.0.1", 8080))
    monkeypatch.setattr(
        manager, "_get_secure_proxy", lambda: (True, "127.0.0.1", 8080)
    )
    monkeypatch.setattr(manager, "_get_auto_proxy_state", lambda: False)
    monkeypatch.setattr(manager, "_get_auto_proxy_url", lambda: None)
    monkeypatch.setattr(manager, "_get_bypass_domains", lambda: ["localhost"])

    state = manager.snapshot()
    assert isinstance(state, ProxyState)
    assert state.web_enabled is True
    assert state.secure_enabled is True
    assert state.bypass_domains == ["localhost"]


@pytest.mark.unit
def test_snapshot_failure_returns_none(monkeypatch: pytest.MonkeyPatch) -> None:
    manager = MacProxyManager("Wi-Fi")

    def _raise():
        raise subprocess.CalledProcessError(1, "networksetup")

    monkeypatch.setattr(manager, "_get_web_proxy", _raise)
    assert manager.snapshot() is None


@pytest.mark.unit
def test_merge_bypass_domains_adds_required() -> None:
    manager = MacProxyManager("Wi-Fi")
    merged = manager._merge_bypass_domains(["example.com"])
    for required in manager.REQUIRED_BYPASS:
        assert required in merged
    assert "example.com" in merged


@pytest.mark.unit
def test_get_bypass_domains_parsing(monkeypatch: pytest.MonkeyPatch) -> None:
    manager = MacProxyManager("Wi-Fi")
    monkeypatch.setattr(
        manager,
        "_run_networksetup",
        lambda args, check=False: "There aren't any bypass domains set\nlocalhost\n",
    )
    assert manager._get_bypass_domains() == ["localhost"]


@pytest.mark.unit
def test_enable_capture_proxy_configures_expected_steps(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manager = MacProxyManager("Wi-Fi")
    calls: list[tuple[str, object]] = []
    monkeypatch.setattr(manager, "_get_bypass_domains", lambda: ["example.org"])
    monkeypatch.setattr(
        manager,
        "_set_auto_proxy_state",
        lambda enabled: calls.append(("auto_state", enabled)),
    )
    monkeypatch.setattr(
        manager, "_set_web_proxy", lambda host, port: calls.append(("web_proxy", host, port))
    )
    monkeypatch.setattr(
        manager,
        "_set_secure_proxy",
        lambda host, port: calls.append(("secure_proxy", host, port)),
    )
    monkeypatch.setattr(
        manager, "_set_web_proxy_state", lambda enabled: calls.append(("web_state", enabled))
    )
    monkeypatch.setattr(
        manager,
        "_set_secure_proxy_state",
        lambda enabled: calls.append(("secure_state", enabled)),
    )
    monkeypatch.setattr(
        manager, "_set_bypass_domains", lambda domains: calls.append(("bypass", tuple(domains)))
    )

    manager.enable_capture_proxy("127.0.0.1", 9090)
    assert ("auto_state", False) in calls
    assert ("web_proxy", "127.0.0.1", 9090) in calls
    assert ("secure_proxy", "127.0.0.1", 9090) in calls
    bypass_calls = [c for c in calls if c[0] == "bypass"]
    assert bypass_calls
    for required in manager.REQUIRED_BYPASS:
        assert required in bypass_calls[0][1]


@pytest.mark.unit
def test_restore_replays_saved_configuration(monkeypatch: pytest.MonkeyPatch) -> None:
    manager = MacProxyManager("Wi-Fi")
    state = ProxyState(
        web_enabled=True,
        web_host="10.0.0.5",
        web_port=8888,
        secure_enabled=False,
        secure_host=None,
        secure_port=None,
        auto_enabled=True,
        auto_url="http://pac.local/proxy.pac",
        bypass_domains=["localhost", "example.net"],
    )
    calls: list[tuple[str, object]] = []
    monkeypatch.setattr(
        manager, "_set_auto_proxy_url", lambda url: calls.append(("auto_url", url))
    )
    monkeypatch.setattr(
        manager,
        "_set_auto_proxy_state",
        lambda enabled: calls.append(("auto_state", enabled)),
    )
    monkeypatch.setattr(
        manager, "_set_web_proxy", lambda host, port: calls.append(("web_proxy", host, port))
    )
    monkeypatch.setattr(
        manager, "_set_web_proxy_state", lambda enabled: calls.append(("web_state", enabled))
    )
    monkeypatch.setattr(
        manager, "_set_secure_proxy_state", lambda enabled: calls.append(("secure_state", enabled))
    )
    monkeypatch.setattr(
        manager, "_set_bypass_domains", lambda domains: calls.append(("bypass", tuple(domains)))
    )

    manager.restore(state)
    assert ("auto_url", "http://pac.local/proxy.pac") in calls
    assert ("auto_state", True) in calls
    assert ("web_proxy", "10.0.0.5", 8888) in calls
    assert ("web_state", True) in calls
    assert ("secure_state", False) in calls
    assert ("bypass", ("localhost", "example.net")) in calls
