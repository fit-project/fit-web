import json
import os
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from fit_common.core import debug, get_platform
from fit_bootstrap.constants import FIT_USER_APP_PATH

_PROXY_RESTORE_WATCHDOG_ENV = "FIT_PROXY_RESTORE_WATCHDOG"
_PROXY_RESTORE_PARENT_PID_ENV = "FIT_PROXY_RESTORE_PARENT_PID"


@dataclass(frozen=True)
class ProxyState:
    web_enabled: bool
    web_host: str | None
    web_port: int | None
    secure_enabled: bool
    secure_host: str | None
    secure_port: int | None
    auto_enabled: bool
    auto_url: str | None
    bypass_domains: list[str]


def _get_proxy_state_path() -> str | None:
    base_path = os.environ.get(FIT_USER_APP_PATH)
    if not base_path:
        return None
    return os.path.join(base_path, "proxy_state.json")


def _pid_exists(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def persist_proxy_state(manager, state: ProxyState) -> bool:
    path = _get_proxy_state_path()
    if not path:
        debug(
            "❌ FIT_USER_APP_PATH not set; cannot persist proxy state",
            context="fit_web.os_proxy_setup",
        )
        return False

    payload = {
        "platform": get_platform(),
        "state": asdict(state),
    }
    service = getattr(manager, "service", None)
    if service:
        payload["service"] = service

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
        debug(f"✅ Persisted proxy state to {path}", context="fit_web.os_proxy_setup")
        return True
    except OSError as exc:
        debug(
            f"❌ Unable to persist proxy state: {exc}",
            context="fit_web.os_proxy_setup",
        )
        return False


def clear_persisted_proxy_state() -> bool:
    path = _get_proxy_state_path()
    if not path:
        return False
    try:
        if os.path.exists(path):
            os.unlink(path)
        return True
    except OSError as exc:
        debug(
            f"❌ Unable to clear persisted proxy state: {exc}",
            context="fit_web.os_proxy_setup",
        )
        return False


def restore_persisted_proxy_state() -> bool:
    path = _get_proxy_state_path()
    if not path or not os.path.exists(path):
        return False

    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        debug(
            f"❌ Unable to load persisted proxy state: {exc}",
            context="fit_web.os_proxy_setup",
        )
        clear_persisted_proxy_state()
        return False

    try:
        state = ProxyState(**payload["state"])
    except (KeyError, TypeError) as exc:
        debug(
            f"❌ Invalid persisted proxy state payload: {exc}",
            context="fit_web.os_proxy_setup",
        )
        clear_persisted_proxy_state()
        return False

    manager = None
    platform = payload.get("platform")
    if platform == "macos":
        from .macos.proxy import MacProxyManager

        service = payload.get("service") or MacProxyManager.detect_service()
        if service:
            manager = MacProxyManager(service)
    else:
        manager = get_proxy_manager()

    if manager is None or not hasattr(manager, "restore"):
        debug(
            "❌ Unable to recreate proxy manager for persisted restore",
            context="fit_web.os_proxy_setup",
        )
        return False

    try:
        manager.restore(state)
    except Exception as exc:
        debug(
            f"❌ Persisted proxy restore failed: {exc}",
            context="fit_web.os_proxy_setup",
        )
        return False

    clear_persisted_proxy_state()
    debug("✅ Restored persisted proxy state", context="fit_web.os_proxy_setup")
    return True


def launch_proxy_restore_watchdog() -> bool:
    path = _get_proxy_state_path()
    if not path or not os.path.exists(path):
        return False

    env = os.environ.copy()
    env[_PROXY_RESTORE_WATCHDOG_ENV] = "1"
    env[_PROXY_RESTORE_PARENT_PID_ENV] = str(os.getpid())

    if getattr(sys, "frozen", False):
        cmd = [sys.executable]
    else:
        cmd = [sys.executable, str(Path(__file__).resolve().parents[2] / "main.py")]

    try:
        subprocess.Popen(
            cmd,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        debug("✅ Proxy restore watchdog started", context="fit_web.os_proxy_setup")
        return True
    except OSError as exc:
        debug(
            f"❌ Unable to start proxy restore watchdog: {exc}",
            context="fit_web.os_proxy_setup",
        )
        return False


def run_proxy_restore_watchdog(
    parent_pid: int,
    poll_interval: float = 0.5,
) -> int:
    path = _get_proxy_state_path()
    if not path:
        return 1

    while _pid_exists(parent_pid):
        if not os.path.exists(path):
            return 0
        time.sleep(poll_interval)

    if not os.path.exists(path):
        return 0

    return 0 if restore_persisted_proxy_state() else 1


def get_proxy_manager():
    platform = get_platform()
    if platform == "macos":
        from .macos.proxy import MacProxyManager

        service = MacProxyManager.detect_service()
        if not service:
            debug(
                "❌ No active network service found", context="fit_web.os_proxy_setup"
            )
            return None
        return MacProxyManager(service)
    if platform == "win":
        from .win.proxy import WinProxyManager

        return WinProxyManager()
    if platform == "linux":
        from .lin.proxy import LinuxProxyManager

        return LinuxProxyManager()

    debug(f"❌ Unsupported platform: {platform}", context="os_proxy_setup")
    return None


__all__ = [
    "ProxyState",
    "clear_persisted_proxy_state",
    "get_proxy_manager",
    "launch_proxy_restore_watchdog",
    "persist_proxy_state",
    "restore_persisted_proxy_state",
    "run_proxy_restore_watchdog",
]
