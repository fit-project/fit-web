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
import platform
import sys

from fit_bootstrap.app_lock import acquire_app_lock, release_app_lock
from fit_bootstrap.bootstrap import Bootstrap
from fit_bootstrap.constants import STAGE_ENV, STAGE_GUI
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
from packaging.version import Version
from PySide6 import QtGui
from PySide6.QtWidgets import QApplication, QMessageBox

from fit_web.web import Web


def _log_bootstrap_result(result: BootstrapResult) -> None:
    if result.signal == BootstrapSignal.OK:
        debug("✅ Bootstrap completed", context="Main.fit_web")
    elif result.signal == BootstrapSignal.ADMIN_DENIED:
        debug("❌ Admin permissions denied", context="Main.fit_web")
    elif result.signal == BootstrapSignal.UNSUPPORTED_OS:
        debug(
            f"❌ Unsupported operating system: {result.message}", context="Main.fit_web"
        )
    else:
        debug(f"❌ Bootstrap error: {result.message}", context="Main.fit_web")


def _mac_ok():
    if sys.platform != "darwin":
        return True
    ver = platform.mac_ver()[0]  # es. '14.5.1' su Sonoma
    return ver and Version(ver) >= Version("11.3")


if not _mac_ok():
    # TODO - Finestra ad-hoc
    raise SystemExit("FIT richiede macOS 11.3 o superiore.")


def parse_args():
    parser = argparse.ArgumentParser(description="FIT Web Module")
    parser.add_argument(
        "--debug",
        choices=["none", "log", "verbose"],
        default="none",
        help="Set the debug level (default: none)",
    )
    return parser.parse_args()


def show_crash_dialog(error_message: str):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle("Application Error")
    msg_box.setText("A fatal error occurred:")
    msg_box.setDetailedText(error_message)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec()


def _run_gui() -> int:
    app = QApplication(sys.argv)

    set_gui_crash_handler(show_crash_dialog)

    if get_platform() == "win":
        app_id = "org.fit-project.fit"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

    app.setWindowIcon(QtGui.QIcon(resolve_path("icon.ico")))

    window = Web()
    if window.has_valid_case:
        window.show()
        return app.exec()
    debug(
        "❌ User cancelled the case form. Nothing to display.", context="Main.fit_web"
    )
    return 0


def main() -> int:
    if get_platform() == "macos" and os.environ.get("FIT_ASKPASS_DIALOG") == "1":
        from fit_bootstrap.macos.askpass_dialog import main as askpass_main

        return askpass_main()

    args = parse_args()
    set_debug_level(
        {
            "none": DebugLevel.NONE,
            "log": DebugLevel.LOG,
            "verbose": DebugLevel.VERBOSE,
        }[args.debug]
    )

    debug(f"argv: {sys.argv}")
    debug(f"bundled: {is_bundled()}")

    if os.environ.get(STAGE_ENV) == STAGE_GUI:
        debug(f"GUI stage admin: {is_admin()}")
        if not is_admin():
            debug("❌ GUI stage requires root privileges")
            return 1
        if not acquire_app_lock():
            debug("❌ Another instance is already running")
            return 1
        atexit.register(release_app_lock)
        return _run_gui()

    bootstrap = Bootstrap(debug_enabled=args.debug != "none")
    preflight_result = bootstrap._dispatch(
        on_signal=_log_bootstrap_result,
        argv=list(sys.argv),
        stage_env=STAGE_ENV,
        stage_gui=STAGE_GUI,
    )
    return preflight_result.code


if __name__ == "__main__":
    main()
