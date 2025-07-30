#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: LGPL-3.0-or-later
# -----
######

import argparse
import sys

from fit_common.core import DebugLevel, debug, set_debug_level
from PySide6.QtWidgets import QApplication

from fit_web.web import Web


def parse_args():
    parser = argparse.ArgumentParser(description="FIT Web Module")
    parser.add_argument(
        "--debug",
        choices=["none", "log", "verbose"],
        default="none",  # <-- default aggiornato
        help="Set the debug level (default: none)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    set_debug_level(
        {
            "none": DebugLevel.NONE,
            "log": DebugLevel.LOG,
            "verbose": DebugLevel.VERBOSE,
        }[args.debug]
    )

    app = QApplication(sys.argv)
    window = Web()
    if window.has_valid_case:
        window.show()
        sys.exit(app.exec())
    else:
        debug(
            "User cancelled the case form. Nothing to display.", context="main fit_web"
        )
        sys.exit(0)


if __name__ == "__main__":
    main()
