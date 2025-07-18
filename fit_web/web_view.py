#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: GPL-3.0-only
# -----
######

import os
from urllib.parse import urlparse

from PySide6.QtCore import Signal
from PySide6.QtWebEngineCore import (
    QWebEngineDownloadRequest,
)
from PySide6.QtWebEngineWidgets import QWebEngineView


class WebEngineView(QWebEngineView):
    saveResourcesFinished = Signal()
    downloadItemFinished = Signal(QWebEngineDownloadRequest)
    downloadProgressChanged = Signal(int, int)
    downloadStarted = Signal(QWebEngineDownloadRequest)
    downloadError = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def set_download_request_handler(self):
        self.page().profile().downloadRequested.connect(self.__handle_download_request)

    def set_acquisition_dir(self, acquisition_directory):
        default_download_path = os.path.join(acquisition_directory, "downloads")
        if not os.path.isdir(default_download_path):
            os.makedirs(default_download_path)

        self.page().profile().setDownloadPath(default_download_path)

    def save_resources(self, acquisition_page_folder):
        hostname = urlparse(self.url().toString()).hostname
        if not hostname:
            hostname = "unknown"

        self.page().save(
            os.path.join(acquisition_page_folder, hostname + ".html"),
            format=QWebEngineDownloadRequest.SavePageFormat.CompleteHtmlSaveFormat,
        )

    def __handle_download_request(self, download):

        if download.isSavePageDownload():
            download.isFinishedChanged.connect(self.saveResourcesFinished.emit)

        else:
            self.downloadStarted.emit(download)

            download.receivedBytesChanged.connect(
                lambda: self.downloadProgressChanged.emit(
                    download.receivedBytes(),
                    download.totalBytes(),
                )
            )
            download.totalBytesChanged.connect(
                lambda: self.downloadProgressChanged.emit(
                    download.receivedBytes(),
                    download.totalBytes(),
                )
            )

            download.isFinishedChanged.connect(
                lambda: self.downloadItemFinished.emit(download)
            )

            download.accept()

    def closeEvent(self, event):
        self.page().profile().clearHttpCache()
