#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: LGPL-3.0-or-later
# -----
######

from __future__ import annotations

import ast
import subprocess
from typing import Any, Iterable

from fit_common.core import debug, get_context

from fit_web.os_proxy_setup import ProxyState


class LinuxProxyManager:
    """Manage the desktop proxy settings exposed by GNOME's gsettings."""

    PROXY_SCHEMA = "org.gnome.system.proxy"
    HTTP_SCHEMA = "org.gnome.system.proxy.http"
    HTTPS_SCHEMA = "org.gnome.system.proxy.https"
    REQUIRED_BYPASS = ["localhost", "127.0.0.1", "::1"]

    def snapshot(self) -> ProxyState | None:
        try:
            mode = self._get_string(self.PROXY_SCHEMA, "mode")
            web = self._get_proxy(self.HTTP_SCHEMA, has_enabled_key=True)
            secure = self._get_proxy(self.HTTPS_SCHEMA, has_enabled_key=False)
            auto_url = self._get_string(self.PROXY_SCHEMA, "autoconfig-url")
            bypass = self._get_string_list(self.PROXY_SCHEMA, "ignore-hosts")
            return ProxyState(
                web_enabled=mode == "manual" and web[0],
                web_host=web[1],
                web_port=web[2],
                secure_enabled=mode == "manual" and secure[0],
                secure_host=secure[1],
                secure_port=secure[2],
                auto_enabled=mode == "auto",
                auto_url=auto_url or None,
                bypass_domains=bypass,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError) as exc:
            debug(
                f"❌ Unable to snapshot proxy state: {exc}",
                context=get_context(self),
            )
            return None

    def enable_capture_proxy(self, host: str, port: int) -> None:
        bypass = self._merge_bypass_domains(
            self._get_string_list(self.PROXY_SCHEMA, "ignore-hosts")
        )

        self._set_string(self.HTTP_SCHEMA, "host", host)
        self._set_int(self.HTTP_SCHEMA, "port", port)
        self._set_bool(self.HTTP_SCHEMA, "enabled", True)
        self._set_string(self.HTTPS_SCHEMA, "host", host)
        self._set_int(self.HTTPS_SCHEMA, "port", port)
        self._set_string_list(self.PROXY_SCHEMA, "ignore-hosts", bypass)
        self._set_string(self.PROXY_SCHEMA, "mode", "manual")

    def restore(self, state: ProxyState) -> None:
        debug("ℹ️ restore: start", context=get_context(self))

        self._restore_proxy(
            self.HTTP_SCHEMA,
            state.web_enabled,
            state.web_host,
            state.web_port,
            has_enabled_key=True,
        )
        self._restore_proxy(
            self.HTTPS_SCHEMA,
            state.secure_enabled,
            state.secure_host,
            state.secure_port,
            has_enabled_key=False,
        )
        self._set_string_list(
            self.PROXY_SCHEMA, "ignore-hosts", state.bypass_domains
        )

        if state.auto_enabled and state.auto_url:
            self._set_string(self.PROXY_SCHEMA, "autoconfig-url", state.auto_url)
            mode = "auto"
        elif state.web_enabled or state.secure_enabled:
            mode = "manual"
        else:
            mode = "none"
        self._set_string(self.PROXY_SCHEMA, "mode", mode)
        debug("✅ restore: done", context=get_context(self))

    def _run_gsettings(self, args: list[str], check: bool = True) -> str:
        debug(f"ℹ️ gsettings: start {' '.join(args)}", context=get_context(self))
        result = subprocess.run(
            ["gsettings", *args],
            capture_output=True,
            text=True,
            check=check,
        )
        debug(f"✅ gsettings: done {' '.join(args)}", context=get_context(self))
        return result.stdout.strip()

    def _get_value(self, schema: str, key: str) -> Any:
        output = self._run_gsettings(["get", schema, key])
        try:
            return ast.literal_eval(output)
        except (SyntaxError, ValueError):
            if output == "true":
                return True
            if output == "false":
                return False
            try:
                return int(output)
            except ValueError as exc:
                raise ValueError(
                    f"Unable to parse gsettings value for {schema} {key}: {output}"
                ) from exc

    def _get_string(self, schema: str, key: str) -> str:
        value = self._get_value(schema, key)
        if not isinstance(value, str):
            raise ValueError(f"Expected a string for {schema} {key}")
        return value

    def _get_string_list(self, schema: str, key: str) -> list[str]:
        value = self._get_value(schema, key)
        if not isinstance(value, list) or not all(
            isinstance(item, str) for item in value
        ):
            raise ValueError(f"Expected a string list for {schema} {key}")
        return value

    def _get_proxy(
        self, schema: str, *, has_enabled_key: bool
    ) -> tuple[bool, str | None, int | None]:
        host = self._get_string(schema, "host") or None
        port = self._get_value(schema, "port")
        if not isinstance(port, int) or isinstance(port, bool):
            raise ValueError(f"Expected an integer for {schema} port")
        if has_enabled_key:
            enabled = self._get_value(schema, "enabled")
            if not isinstance(enabled, bool):
                raise ValueError(f"Expected a boolean for {schema} enabled")
        else:
            enabled = host is not None and port > 0
        return enabled, host, port

    def _set_value(self, schema: str, key: str, value: str) -> None:
        self._run_gsettings(["set", schema, key, value], check=False)

    def _set_string(self, schema: str, key: str, value: str) -> None:
        self._set_value(schema, key, repr(value))

    def _set_int(self, schema: str, key: str, value: int) -> None:
        self._set_value(schema, key, str(value))

    def _set_bool(self, schema: str, key: str, value: bool) -> None:
        self._set_value(schema, key, "true" if value else "false")

    def _set_string_list(
        self, schema: str, key: str, values: Iterable[str]
    ) -> None:
        self._set_value(schema, key, repr([value for value in values if value]))

    def _restore_proxy(
        self,
        schema: str,
        enabled: bool,
        host: str | None,
        port: int | None,
        *,
        has_enabled_key: bool,
    ) -> None:
        self._set_string(schema, "host", host or "")
        if port is not None:
            self._set_int(schema, "port", port)
        if has_enabled_key:
            self._set_bool(schema, "enabled", enabled)
        elif not enabled and host is None:
            self._set_int(schema, "port", 0)

    def _merge_bypass_domains(self, domains: list[str]) -> list[str]:
        combined = list(domains)
        for required in self.REQUIRED_BYPASS:
            if required not in combined:
                combined.append(required)
        return combined
