#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: LGPL-3.0-or-later
# -----
######

import sys

from PySide6.QtWidgets import QApplication

from fit_web.web import Web


def main():
    app = QApplication(sys.argv)
    window = Web()
    if window.has_valid_case:
        window.show()
        sys.exit(app.exec())
    else:
        print("Utente ha annullato il form del caso. Niente da mostrare.")
        sys.exit(0)


if __name__ == "__main__":
    main()
