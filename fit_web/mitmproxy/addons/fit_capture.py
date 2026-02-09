#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: LGPL-3.0-or-later
# -----
######

from __future__ import annotations

import asyncio
import os
from pathlib import Path

from mitmproxy import ctx, http
from mitmproxy.addons import savehar


class FitCapture:
    def __init__(self) -> None:
        self._flows: list[http.HTTPFlow] = []
        self._collecting = False
        self._control_path = Path(os.environ.get("FIT_CAPTURE_CONTROL", ""))
        self._har_path = os.environ.get("FIT_CAPTURE_HAR", "")
        self._savehar = savehar.SaveHar()
        self._last_cmd = ""
        self._task: asyncio.Task | None = None

    def load(self, loader) -> None:
        ctx.log.info("FIT capture addon loaded")

    async def _poll_control(self) -> None:
        while True:
            try:
                if self._control_path:
                    cmd = self._control_path.read_text().strip().lower()
                else:
                    cmd = ""
            except OSError:
                cmd = ""

            if cmd and cmd != self._last_cmd:
                self._last_cmd = cmd
                if cmd == "start":
                    self._collecting = True
                    self._flows.clear()
                    ctx.log.info("FIT capture started")
                elif cmd == "stop":
                    self._collecting = False
                    self._export_har()
                    ctx.log.info("FIT capture stopped")
            await asyncio.sleep(0.5)

    def running(self) -> None:
        if self._task is None:
            self._task = asyncio.create_task(self._poll_control())

    def done(self) -> None:
        if self._task is not None:
            self._task.cancel()
            self._task = None

    def response(self, flow: http.HTTPFlow) -> None:
        if self._collecting and flow.websocket is None:
            self._flows.append(flow)

    def error(self, flow: http.HTTPFlow) -> None:
        self.response(flow)

    def websocket_end(self, flow: http.HTTPFlow) -> None:
        if self._collecting:
            self._flows.append(flow)

    def _export_har(self) -> None:
        path = ctx.options.hardump or self._har_path
        if not path:
            ctx.log.warn("FIT capture: no HAR path configured")
            return
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            self._savehar.export_har(self._flows, path)
            ctx.log.info(f"FIT capture HAR exported ({len(self._flows)} flows)")
        except Exception as exc:
            ctx.log.error(f"FIT capture export failed: {exc}")


addons = [FitCapture()]
