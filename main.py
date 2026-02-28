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
from fit_bootstrap.lang import load_translations as bootstrap_load_translations
from fit_bootstrap.signals import BootstrapResult, BootstrapSignal
from fit_common.core import (
    DebugLevel,
    debug,
    get_platform,
    is_admin,
    is_bundled,
    open_macos_privacy_settings,
    resolve_path,
    set_debug_level,
    set_gui_crash_handler,
)
from fit_common.gui.utils import show_dialog
from packaging.version import Version
from PySide6 import QtGui
from PySide6.QtWidgets import QApplication

from fit_web.lang import load_translations
from fit_web.mitmproxy.runner import MitmproxyRunner
from fit_web.web import Web

_FFMPEG_HELP_KEYS = {
    "macos": "BOOSTSTRAP_FFMPEG_PATH_NOT_FOUND_HELP_MACOS",
    "win": "BOOSTSTRAP_FFMPEG_PATH_NOT_FOUND_HELP_WINDOWS",
    "lin": "BOOSTSTRAP_FFMPEG_PATH_NOT_FOUND_HELP_LINUX",
}


def _log_bootstrap_result(result: BootstrapResult) -> None:
    __translations = bootstrap_load_translations()
    title = __translations.get("BOOSTSTRAP_ERROR_DIALOG_TITLE")
    if result.signal == BootstrapSignal.OK:
        debug("✅ Bootstrap completed", context="main.fit_bootstrap")
    elif result.signal == BootstrapSignal.ADMIN_DENIED:
        debug("❌ Admin permissions denied", context="main.fit_bootstrap")
        admin_type = "administrator" if get_platform() == "win" else "root"
        message = __translations.get("BOOSTSTRAP_ADMIN_DENIED_MESSAGE", "").format(
            admin_type, admin_type
        )
        show_dialog("error", title, message, "")
    elif result.signal == BootstrapSignal.CERTIFICATE_NOT_INSTALLED:
        debug("❌ Certificate installation failed", context="main.fit_bootstrap")
        show_dialog(
            "error",
            title,
            __translations.get("BOOSTSTRAP_CERTIFICATE_NOT_INSTALLED_MESSAGE", ""),
        )
    elif result.signal == BootstrapSignal.FFMPEG_PATH_NOT_FOUND:
        debug("❌ ffmpeg path not found", context="main.fit_bootstrap")
        base_message = __translations.get(
            "BOOSTSTRAP_FFMPEG_PATH_NOT_FOUND_MESSAGE",
            "",
        )
        platform_key = get_platform()
        help_key = _FFMPEG_HELP_KEYS.get(platform_key)
        help_text = __translations.get(help_key, "") if help_key is not None else ""
        if base_message and "{}" in base_message:
            dialog_message = base_message.format(help_text)
        else:
            dialog_message = base_message
            if help_text:
                dialog_message = f"{dialog_message}<br><br>{help_text}"
        show_dialog("warning", title, dialog_message)
    elif result.signal == BootstrapSignal.UNSUPPORTED_OS:
        debug(
            f"❌ Unsupported operating system: {result.message}",
            context="main.fit_bootstrap",
        )
        show_dialog(
            "error",
            title,
            __translations.get("BOOSTSTRAP_UNSUPPORTED_OS_MESSAGE", ""),
        )
    elif result.signal == BootstrapSignal.FFMPEG_SCREEN_RECORDING_PERMISSIONS_DENIED:
        debug("❌ Screen recording permissions denied", context="main.fit_bootstrap")
        show_dialog(
            "error",
            title,
            __translations.get(
                "BOOSTSTRAP_FFMPEG_SCREEN_RECORDING_PERMISSIONS_DENIED_MESSAGE", ""
            ),
        )
        open_macos_privacy_settings()
    elif result.signal == BootstrapSignal.FFMPEG_SCREEN_RECORDING_TEST_FAILED:
        debug("❌ Screen recording test failed", context="main.fit_bootstrap")
        show_dialog(
            "error",
            title,
            __translations.get(
                "BOOSTSTRAP_FFMPEG_SCREEN_RECORDING_TEST_FAILED_MESSAGE", ""
            ),
        )
        open_macos_privacy_settings()
    else:
        debug(f"❌ Bootstrap error: {result.message}", context="main.fit_bootstrap")
        show_dialog(
            "error",
            title,
            __translations.get("BOOSTSTRAP_UNKNOW_ERROR_MSG", "")
            + f"<br><br>{result.message}",
        )


def _mac_ok():
    if get_platform() != "macos":
        return True
    ver = platform.mac_ver()[0]  # es. '14.5.1' su Sonoma
    return ver and Version(ver) >= Version("11.3")


def _ensure_macos_or_exit() -> None:
    if get_platform() == "macos":
        return

    __translations = load_translations()
    show_dialog(
        "error",
        __translations.get("UNSUPPORTED_OS_DIALOG_TITLE"),
        __translations.get("UNSUPPORTED_OS_DIALOG_MESSAGE"),
        "",
    )
    debug(f"❌ Unsupported operating system: {get_platform()}", context="main.fit_web")
    raise SystemExit("❌ Unsupported operating system")


_ensure_macos_or_exit()


if not _mac_ok():
    __translations = load_translations()
    show_dialog(
        "error",
        __translations.get("OS_VERSION_ERROR_DIALOG_TITLE"),
        __translations.get("MACOS_VERSION_ERROR_DIALOG_MESSAGE").format(
            platform.mac_ver()[0]
        ),
        "",
    )
    debug("❌ macOS version not supported", context="main.fit_web")
    raise SystemExit("❌ macOS version not supported")


def show_crash_dialog(error_message: str):
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

    if os.environ.get("FIT_MITM_LAUNCH") == "1":
        from mitmproxy.tools.main import mitmdump

        return mitmdump()

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

    bootstrap = Bootstrap(debug_enabled=args.debug != "none")

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
