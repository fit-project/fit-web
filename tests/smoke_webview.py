#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: LGPL-3.0-or-later
# -----
######

from fit_webview_bridge import SystemWebView
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

URL = "https://www.facebook.com/reel/574839388710756/"

app = QApplication([])

view = SystemWebView()
view.setMinimumSize(900, 600)
view.setUrl(URL)  # carica una pagina semplice
view.show()


def on_loaded_ok():
    print("[SMOKE] page loaded:", URL)
    # aspetta un attimo e termina (così non resta bloccato nei test CI)
    QTimer.singleShot(1500, app.quit)


# se la tua classe espone loadFinished(bool), usala; altrimenti togli l'argomento
try:
    view.loadFinished.connect(
        lambda ok: on_loaded_ok() if ok else print("[SMOKE] load failed")
    )
except Exception:
    # fallback se non esiste il segnale; esci comunque dopo 2s
    QTimer.singleShot(2000, app.quit)

app.exec()
