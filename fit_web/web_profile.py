#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: GPL-3.0-only
# -----
######


from PySide6.QtCore import Signal
from PySide6.QtWebEngineCore import (
    QWebEnginePage,
    QWebEngineProfile,
)


class WebEngineProfile(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(WebEngineProfile, cls).__new__(cls)
            profile = QWebEngineProfile.defaultProfile()
            cls.default_download_path = profile.downloadPath()
            profile.clearAllVisitedLinks()
            cookie_store = profile.cookieStore()
            cookie_store.deleteAllCookies()

        return cls.instance


class WebEnginePage(QWebEnginePage):
    new_page_after_link_with_target_blank_attribute = Signal(QWebEnginePage)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__default_profile = WebEngineProfile()

    def handleCertificateError(self, error):
        error.acceptCertificate()

    # When you click a link that has the target="_blank" attribute, QT calls the CreateWindow method in
    # QWebEnginePage to create a new tab/new window.
    def createWindow(
        self,
        _type,
    ):
        page = WebEnginePage(self)
        page.profile().setDownloadPath(self.profile().downloadPath())
        self.new_page_after_link_with_target_blank_attribute.emit(page)
        return page

    def reset_default_path(self):
        self.profile().setDownloadPath(self.__default_profile.default_download_path)
