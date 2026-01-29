from dataclasses import dataclass

from fit_common.core import debug, get_platform


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


__all__ = ["get_proxy_manager", "ProxyState"]
