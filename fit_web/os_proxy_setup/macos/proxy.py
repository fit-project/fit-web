#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: LGPL-3.0-or-later
# -----
######

from __future__ import annotations

import subprocess
from typing import Iterable

from fit_common.core import debug, get_context

from fit_web.os_proxy_setup import ProxyState


class MacProxyManager:
    REQUIRED_BYPASS = ["localhost", "127.0.0.1", "::1"]

    def __init__(self, service: str):
        self.service = service

    @staticmethod
    def detect_service() -> str | None:
        try:
            result = subprocess.run(
                ["networksetup", "-listallnetworkservices"],
                capture_output=True,
                text=True,
                check=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            debug(f"❌ Unable to list network services: {exc}", context="macos.proxy")
            return None

        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        services: list[str] = []
        for line in lines:
            if line.startswith("An asterisk ("):
                continue
            if line.startswith("*"):
                continue
            services.append(line)

        if not services:
            return None

        if "Wi-Fi" in services:
            return "Wi-Fi"
        if "Ethernet" in services:
            return "Ethernet"
        return services[0]

    def snapshot(self) -> ProxyState | None:
        try:
            web = self._get_web_proxy()
            secure = self._get_secure_proxy()
            auto_enabled = self._get_auto_proxy_state()
            auto_url = self._get_auto_proxy_url()
            bypass = self._get_bypass_domains()
            return ProxyState(
                web_enabled=web[0],
                web_host=web[1],
                web_port=web[2],
                secure_enabled=secure[0],
                secure_host=secure[1],
                secure_port=secure[2],
                auto_enabled=auto_enabled,
                auto_url=auto_url,
                bypass_domains=bypass,
            )
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            debug(
                f"❌ Unable to snapshot proxy state: {exc}", context=get_context(self)
            )
            return None

    def enable_capture_proxy(self, host: str, port: int) -> None:
        bypass = self._merge_bypass_domains(self._get_bypass_domains())

        self._set_auto_proxy_state(False)
        self._set_web_proxy(host, port)
        self._set_secure_proxy(host, port)
        self._set_web_proxy_state(True)
        self._set_secure_proxy_state(True)
        self._set_bypass_domains(bypass)

    def restore(self, state: ProxyState) -> None:
        debug("ℹ️ restore: start", context=get_context(self))
        if state.auto_enabled and state.auto_url:
            debug("ℹ️ restore: set auto proxy url/state", context=get_context(self))
            self._set_auto_proxy_url(state.auto_url)
            self._set_auto_proxy_state(True)
        else:
            debug("ℹ️ restore: disable auto proxy", context=get_context(self))
            self._set_auto_proxy_state(False)

        if state.web_enabled and state.web_host and state.web_port is not None:
            debug("ℹ️ restore: set web proxy", context=get_context(self))
            self._set_web_proxy(state.web_host, state.web_port)
            self._set_web_proxy_state(True)
        else:
            debug("ℹ️ restore: disable web proxy", context=get_context(self))
            self._set_web_proxy_state(False)

        if state.secure_enabled and state.secure_host and state.secure_port is not None:
            debug("ℹ️ restore: set secure proxy", context=get_context(self))
            self._set_secure_proxy(state.secure_host, state.secure_port)
            self._set_secure_proxy_state(True)
        else:
            debug("ℹ️ restore: disable secure proxy", context=get_context(self))
            self._set_secure_proxy_state(False)

        debug("ℹ️ restore: set bypass domains", context=get_context(self))
        self._set_bypass_domains(state.bypass_domains)
        debug("✅ restore: done", context=get_context(self))

    def _run_networksetup(self, args: list[str], check: bool = True) -> str:
        debug(
            f"ℹ️ networksetup: start {' '.join(args)}",
            context=get_context(self),
        )
        result = subprocess.run(
            ["networksetup", *args],
            capture_output=True,
            text=True,
            check=check,
        )
        debug(
            f"✅ networksetup: done {' '.join(args)}",
            context=get_context(self),
        )
        return result.stdout

    def _parse_enabled(self, output: str) -> bool:
        for line in output.splitlines():
            if line.lower().startswith("enabled:"):
                value = line.split(":", 1)[1].strip().lower()
                return value in {"yes", "on", "true", "1"}
        return False

    def _parse_value(self, output: str, key: str) -> str | None:
        key_lower = key.lower() + ":"
        for line in output.splitlines():
            if line.lower().startswith(key_lower):
                return line.split(":", 1)[1].strip()
        return None

    def _parse_port(self, value: str | None) -> int | None:
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            return None

    def _get_web_proxy(self) -> tuple[bool, str | None, int | None]:
        output = self._run_networksetup(["-getwebproxy", self.service])
        enabled = self._parse_enabled(output)
        host = self._parse_value(output, "Server")
        port = self._parse_port(self._parse_value(output, "Port"))
        return enabled, host, port

    def _get_secure_proxy(self) -> tuple[bool, str | None, int | None]:
        output = self._run_networksetup(["-getsecurewebproxy", self.service])
        enabled = self._parse_enabled(output)
        host = self._parse_value(output, "Server")
        port = self._parse_port(self._parse_value(output, "Port"))
        return enabled, host, port

    def _get_auto_proxy_state(self) -> bool:
        output = self._run_networksetup(
            ["-getautoproxystate", self.service], check=False
        )
        return self._parse_enabled(output)

    def _get_auto_proxy_url(self) -> str | None:
        output = self._run_networksetup(["-getautoproxyurl", self.service], check=False)
        return self._parse_value(output, "URL")

    def _get_bypass_domains(self) -> list[str]:
        output = self._run_networksetup(
            ["-getproxybypassdomains", self.service], check=False
        )
        domains: list[str] = []
        for line in output.splitlines():
            entry = line.strip()
            if not entry:
                continue
            if "There aren't any" in entry or "No proxy bypass" in entry:
                continue
            domains.append(entry)
        return domains

    def _set_web_proxy(self, host: str, port: int) -> None:
        self._run_networksetup(["-setwebproxy", self.service, host, str(port)], False)

    def _set_secure_proxy(self, host: str, port: int) -> None:
        self._run_networksetup(
            ["-setsecurewebproxy", self.service, host, str(port)], False
        )

    def _set_web_proxy_state(self, enabled: bool) -> None:
        self._run_networksetup(
            ["-setwebproxystate", self.service, "on" if enabled else "off"],
            False,
        )

    def _set_secure_proxy_state(self, enabled: bool) -> None:
        self._run_networksetup(
            [
                "-setsecurewebproxystate",
                self.service,
                "on" if enabled else "off",
            ],
            False,
        )

    def _set_auto_proxy_state(self, enabled: bool) -> None:
        self._run_networksetup(
            ["-setautoproxystate", self.service, "on" if enabled else "off"],
            False,
        )

    def _set_auto_proxy_url(self, url: str) -> None:
        self._run_networksetup(["-setautoproxyurl", self.service, url], False)

    def _set_bypass_domains(self, domains: Iterable[str]) -> None:
        args = ["-setproxybypassdomains", self.service]
        domains_list = [domain for domain in domains if domain]
        if domains_list:
            args.extend(domains_list)
        else:
            args.append("")
        self._run_networksetup(args, False)

    def _merge_bypass_domains(self, domains: list[str]) -> list[str]:
        combined = list(domains)
        for required in self.REQUIRED_BYPASS:
            if required not in combined:
                combined.append(required)
        return combined
