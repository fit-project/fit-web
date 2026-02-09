#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: LGPL-3.0-or-later
# -----
######

from __future__ import annotations

import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

from fit_bootstrap.constants import (
    FIT_DEBUG_ENABLED,
    FIT_LOG_APP_PATH,
    FIT_MITM_PORT,
    FIT_USER_APP_PATH,
)
from fit_common.core import debug, get_context


class MitmproxyRunner:
    def __init__(self, _parent=None) -> None:
        base_path = os.environ.get(FIT_USER_APP_PATH)
        if not base_path:
            debug(
                "❌ FIT_USER_APP_PATH not set; cannot start mitmproxy",
                context=get_context(self),
            )
            self.output_dir = None
            self.pid_file = None
            self.har_file = None
            return
        self.output_dir = Path(base_path) / "mitmproxy"
        self.pid_file = self.output_dir / "mitmproxy.pid"
        self.har_file = self.output_dir / "capture.har"
        self.control_file = self.output_dir / "capture.control"

    def start(self) -> subprocess.Popen[str] | None:
        if self.output_dir is None or self.pid_file is None or self.har_file is None:
            return None

        debug(
            f"ℹ️ FIT_DEBUG_ENABLED={os.environ.get(FIT_DEBUG_ENABLED)}",
            context=get_context(self),
        )

        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            debug(
                f"❌ Unable to create output directory: {exc}",
                context=get_context(self),
            )
            return None
        self._reset_capture_files()

        existing_pid = self._read_pid()
        if existing_pid:
            try:
                os.kill(existing_pid, 0)
                debug(
                    f"ℹ️ mitmproxy already running (pid={existing_pid}), killing it",
                    context=get_context(self),
                )
                os.kill(existing_pid, signal.SIGKILL)
                self._clear_pid()
            except ProcessLookupError:
                self._clear_pid()
            except PermissionError:
                debug(
                    f"❌ mitmproxy already running (pid={existing_pid}) but no permission to signal it",
                    context=get_context(self),
                )
                return None

        log_file = None
        if os.environ.get(FIT_DEBUG_ENABLED) == "1":
            try:
                log_base = os.environ.get(FIT_LOG_APP_PATH)
                if not log_base:
                    debug(
                        "❌ FIT_LOG_APP_PATH not set; cannot open mitmproxy log",
                        context=get_context(self),
                    )
                    return None
                log_path = Path(log_base) / "mitmproxy.log"

                if log_path.exists():
                    log_path.unlink()
                log_file = log_path.open("a")
            except OSError as exc:
                debug(
                    f"❌ Unable to open mitmproxy log file: {exc}",
                    context=get_context(self),
                )

        base_cmd: list[str]
        extra_env = None
        if getattr(sys, "frozen", False):
            base_cmd = [sys.executable]
            extra_env = {"FIT_MITM_LAUNCH": "1"}
        else:
            base_cmd = [
                sys.executable,
                "-c",
                "from mitmproxy.tools.main import mitmdump; mitmdump()",
            ]

        cmd = [
            *base_cmd,
            "-s",
            str(Path(__file__).parent / "addons" / "fit_capture.py"),
            "--set",
            f"hardump={self.har_file}",
        ]
        mitm_port = os.environ.get(FIT_MITM_PORT)
        if mitm_port:
            try:
                port_value = int(mitm_port)
                cmd += ["--listen-port", str(port_value)]
            except ValueError:
                debug(
                    f"❌ Invalid {FIT_MITM_PORT} value: {mitm_port}",
                    context=get_context(self),
                )
        if os.environ.get(FIT_DEBUG_ENABLED) == "1":
            cmd += ["--set", "termlog_verbosity=debug"]
        debug(f"ℹ️ mitm cmd: {cmd}", context=get_context(self))
        try:
            stdout = subprocess.PIPE if log_file else subprocess.DEVNULL
            stderr = subprocess.PIPE if log_file else subprocess.DEVNULL
            env = os.environ.copy()
            if extra_env:
                env.update(extra_env)
            env["FIT_CAPTURE_CONTROL"] = str(self.control_file)
            env["FIT_CAPTURE_HAR"] = str(self.har_file)
            proc = subprocess.Popen(
                cmd,
                stdout=stdout,
                stderr=stderr,
                text=True,
                bufsize=1,
                env=env,
            )
        except FileNotFoundError:
            if log_file:
                log_file.close()
            debug("❌ Unable to launch mitmproxy module", context=get_context(self))
            return None

        if log_file:
            self._pipe_to_file(proc.stdout, log_file)
            self._pipe_to_file(proc.stderr, log_file)

        time.sleep(0.2)
        exit_code = proc.poll()
        if exit_code is not None:
            if log_file:
                log_file.write(f"mitmproxy exited immediately (code={exit_code})\n")
                log_file.close()
            debug(
                f"❌ mitmproxy exited immediately after start (code={exit_code})",
                context=get_context(self),
            )
            return None

        self._write_pid(proc.pid)
        debug(f"✅ mitmproxy started (pid={proc.pid})", context=get_context(self))
        self._write_control("stop")
        return proc

    def _pipe_to_file(self, stream: subprocess.Popen[str] | None, log_file) -> None:
        if stream is None:
            return

        def _worker() -> None:
            for line in stream:
                log_file.write(line)
            log_file.flush()

        thread = threading.Thread(target=_worker, daemon=True)
        thread.start()

    def stop(self, proc: subprocess.Popen[str] | None) -> None:
        if not proc or proc.poll() is not None:
            return
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
        self._clear_pid()

    def stop_by_pid(self) -> bool:
        pid = self._read_pid()
        if not pid:
            debug("❌ mitmproxy pid not found", context=get_context(self))
            return False
        try:
            os.kill(pid, signal.SIGINT)
            debug(f"Sent SIGINT to mitmproxy pid {pid}", context=get_context(self))
            os.kill(pid, 0)
        except ProcessLookupError:
            self._clear_pid()
            debug("ℹ️ mitmproxy process already stopped", context=get_context(self))
            return True
        except OSError:
            try:
                os.kill(pid, signal.SIGKILL)
                debug(
                    f"ℹ️ Sent SIGKILL to mitmproxy pid {pid}", context=get_context(self)
                )
            except OSError as exc:
                debug(f"❌ Unable to stop mitmproxy: {exc}", context=get_context(self))
                return False
        except OSError as exc:
            debug(f"❌ Unable to stop mitmproxy: {exc}", context=get_context(self))
            return False
        self._clear_pid()
        if self.har_file:
            debug(f"ℹ️ HAR exists: {self.har_file.exists()}", context=get_context(self))
        return True

    def start_capture(self) -> bool:
        return self._write_control("start")

    def stop_capture(self) -> bool:
        return self._write_control("stop")

    def _write_pid(self, pid: int) -> None:
        try:
            if self.pid_file is None:
                return
            self.pid_file.write_text(str(pid))
        except OSError as exc:
            debug(
                f"❌ Unable to write mitmproxy pid file: {exc}",
                context=get_context(self),
            )

    def _read_pid(self) -> int | None:
        try:
            if self.pid_file is None:
                return None
            return int(self.pid_file.read_text().strip())
        except (OSError, ValueError):
            return None

    def _clear_pid(self) -> None:
        try:
            if self.pid_file is None:
                return
            self.pid_file.unlink()
        except OSError:
            pass

    def _write_control(self, command: str) -> bool:
        try:
            if self.control_file is None:
                return False
            self.control_file.parent.mkdir(parents=True, exist_ok=True)
            self.control_file.write_text(command)
            debug(f"ℹ️ Capture control: {command}", context=get_context(self))
            return True
        except OSError as exc:
            debug(
                f"❌ Unable to write capture control: {exc}", context=get_context(self)
            )
            return False

    def _reset_capture_files(self) -> None:
        if self.har_file is not None:
            try:
                if self.har_file.exists():
                    self.har_file.unlink()
            except OSError as exc:
                debug(
                    f"❌ Unable to reset capture.har: {exc}", context=get_context(self)
                )
        if self.control_file is not None:
            try:
                if self.control_file.exists():
                    self.control_file.unlink()
            except OSError as exc:
                debug(
                    f"❌ Unable to reset capture.control: {exc}",
                    context=get_context(self),
                )
