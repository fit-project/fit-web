#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: LGPL-3.0-or-later
# -----
######

import argparse
import atexit
import ctypes
import os
import sys

from fit_bootstrap.app_lock import acquire_app_lock, release_app_lock
from fit_bootstrap.bootstrap import Bootstrap
from fit_bootstrap.caller import CallerProfile
from fit_bootstrap.constants import STAGE_ENV, STAGE_GUI
from fit_bootstrap.lang import load_translations as bootstrap_load_translations
from fit_bootstrap.signals import BootstrapResult, BootstrapSignal
from fit_common.core import (
    DebugLevel,
    debug,
    get_platform,
    is_admin,
    is_bundled,
    resolve_path,
    set_debug_level,
    set_gui_crash_handler,
)
from fit_common.gui.utils import show_dialog
from PySide6 import QtGui
from PySide6.QtWidgets import QApplication

from fit_web.lang import load_translations
from fit_web.mitmproxy.runner import MitmproxyRunner
from fit_web.os_proxy_setup import (
    restore_persisted_proxy_state,
    run_proxy_restore_watchdog,
)
from fit_web.web import Web


def _log_bootstrap_result(result: BootstrapResult) -> None:
    __translations = bootstrap_load_translations()
    title = __translations.get("BOOSTSTRAP_ERROR_DIALOG_TITLE")
    if result.signal == BootstrapSignal.OK:
        debug("✅ Bootstrap completed", context="main.fit_bootstrap")
    else:
        restore_persisted_proxy_state()
        debug(f"❌ Bootstrap error: {result.message}", context="main.fit_bootstrap")
        show_dialog("error", title, result.message)


def show_crash_dialog(error_message: str):
    restore_persisted_proxy_state()
    __translations = load_translations()

    show_dialog(
        "error",
        __translations.get("APPLICATION_ERROR_DIALOG_TITLE"),
        __translations.get("APPLICATION_ERROR_DIALOG_MESSAGE"),
        error_message,
    )


def parse_args():
    parser = argparse.ArgumentParser(description="FIT Web Module")
    parser.add_argument(
        "--debug",
        choices=["none", "log", "verbose"],
        default="none",
        help="Set the debug level (default: none)",
    )
    return parser.parse_args()


def _run_gui() -> int:
    restore_persisted_proxy_state()
    app = QApplication(sys.argv)

    set_gui_crash_handler(show_crash_dialog)

    if get_platform() == "win":
        app_id = "org.fit-project.fit"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

    app.setWindowIcon(QtGui.QIcon(resolve_path("icon.ico")))

    window = Web()
    mitm_runner = MitmproxyRunner(window)
    if window.has_valid_case:
        window.show()
        return app.exec()

    mitm_runner.stop_by_pid()
    debug(
        "❌ User cancelled the case form. Nothing to display.", context="main.fit_web"
    )
    return 0


def main() -> int:
    if os.environ.get("FIT_PROXY_RESTORE_WATCHDOG") == "1":
        parent_pid = os.environ.get("FIT_PROXY_RESTORE_PARENT_PID")
        if not parent_pid:
            return 1
        try:
            return run_proxy_restore_watchdog(int(parent_pid))
        except ValueError:
            return 1

    if os.environ.get("FIT_MITM_LAUNCH") == "1":
        from mitmproxy.tools.main import mitmdump

        return mitmdump()

    if get_platform() == "macos" and os.environ.get("FIT_ASKPASS_DIALOG") == "1":
        from fit_bootstrap.macos.askpass_dialog import main as askpass_main

        return askpass_main()

    if os.environ.get("FIT_UPDATE_DIALOG") == "1":
        from fit_bootstrap.updater import main as updater_main

        return updater_main()

    restore_persisted_proxy_state()

    args = parse_args()
    set_debug_level(
        {
            "none": DebugLevel.NONE,
            "log": DebugLevel.LOG,
            "verbose": DebugLevel.VERBOSE,
        }[args.debug]
    )
    debug(f"Freeze directory: {resolve_path("")}", context="main.fit_web")
    debug(f"argv: {sys.argv}", context="main.fit_web")
    debug(f"bundled: {is_bundled()}", context="main.fit_web")

    if os.environ.get(STAGE_ENV) == STAGE_GUI:
        debug(f"GUI stage admin: {is_admin()}", context="main.fit_web")
        if not is_admin():
            debug("❌ GUI stage requires root privileges", context="main.fit_web")
            return 1
        if not acquire_app_lock():
            debug("❌ Another instance is already running", context="main.fit_web")
            return 1
        atexit.register(release_app_lock)
        return _run_gui()

    bootstrap = Bootstrap(
        debug_enabled=args.debug != "none", caller=CallerProfile.FIT_WEB
    )

    mitm_runner = MitmproxyRunner()
    if not mitm_runner.start():
        debug("❌ mitmproxy start failed", context="main.fit_web")
        return 1

    preflight_result = bootstrap._dispatch(
        on_signal=_log_bootstrap_result,
        argv=list(sys.argv),
        stage_env=STAGE_ENV,
        stage_gui=STAGE_GUI,
    )

    if preflight_result.code != 0:
        mitm_runner.stop_by_pid()

    return preflight_result.code


if __name__ == "__main__":
    main()
