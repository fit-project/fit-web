#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: GPL-3.0-only
# -----
######

import os
from datetime import datetime
from json import loads

import numpy as np
from fit_acquisition.tasks.task import Task
from fit_acquisition.tasks.task_worker import TaskWorker
from fit_common.core import debug, get_context, log_exception
from fit_common.gui.utils import Status
from PIL import Image
from PySide6 import QtCore

from fit_web.lang import load_translations


def screenshot_filename(path, basename, extention=".png"):
    return os.path.join(
        path,
        basename + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f") + extention,
    )


class TaskFullPageScreenShotWorker(TaskWorker):
    def __init__(self):
        super().__init__()
        self.__translations = load_translations()

        self.__capture_queue = []
        self.__capture_files = []
        self.__current_token = None
        self.__start_point_y = 0
        self.__current_widget = None
        self.__acquisistion_directory = None
        self.__screenshot_directory = None
        self.__is_task = False
        self.__connected = False

    def __ensure_connected(self):
        if not self.__connected:
            self.__current_widget.captureFinished.connect(self._on_capture_finished)
            self.__connected = True

    def __scroll_and_shoot(self):
        if not self.__capture_queue:
            imgs = [Image.open(i) for i in self.__capture_files]
            min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
            stacked = np.vstack([i.resize(min_shape) for i in imgs])
            out = Image.fromarray(stacked)

            whole_img_filename = screenshot_filename(
                self.__screenshot_directory, "full_page"
            )
            if self.__is_task:
                whole_img_filename = os.path.join(
                    self.__acquisistion_directory, "screenshot.png"
                )

            out.save(whole_img_filename)

            self.__current_widget.evaluateJavaScript(
                f"window.scrollTo(0, {self.__start_point_y});"
            )
            return

        y, fname = self.__capture_queue.pop(0)

        self.__current_widget.evaluateJavaScript(f"window.scrollTo(0, {y});")

        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(120, loop.quit)
        loop.exec()

        self.__current_token = self.__current_widget.captureVisiblePage(fname)

        self.__capture_files.append(fname)

    def _on_capture_finished(self, token, ok, filePath, error):
        # filtra: gestisci solo il token corrente
        if self.__current_token is not None and token != self.__current_token:
            return
        self.__current_token = None

        if not ok:
            raise ValueError(error or "captureVisiblePage failed")

        # passa allo step successivo
        self.__scroll_and_shoot()

    def take_screenshot(
        self,
        acquisition_directory,
        current_widget,
        screenshot_directory=None,
        is_task=False,
    ):
        self.__current_widget = current_widget
        self.__acquisistion_directory = acquisition_directory
        self.__screenshot_directory = screenshot_directory
        self.__is_task = is_task

        # 1) metrics
        __token = current_widget.evaluateJavaScriptWithResult(
            "(() => ({ y: window.scrollY,"
            "         h: Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),"
            "         vh: window.innerHeight }))()"
        )

        def on_javascript_result(result, token, error):
            if token != __token:
                raise ValueError(
                    self.__translations[
                        "MISMATCHED_JAVASCRIPT_RESULT_TOKEN_ERROR"
                    ].format(__token, token)
                )
            if error:
                raise ValueError(error)

            page_metrics = loads(result) if isinstance(result, str) else result
            self.__start_point_y = page_metrics["y"]

            # 2) Create the output directory and build the capture queue
            full_page_folder = None
            if acquisition_directory is not None:
                full_page_folder = os.path.join(
                    acquisition_directory, f"full_page/{current_widget.url().host()}/"
                )
                os.makedirs(full_page_folder, exist_ok=True)

            # scroll to the top
            current_widget.evaluateJavaScript("window.scrollTo(0, 0);")

            step = max(1, int(page_metrics["vh"]))
            end = int(page_metrics["h"])
            self.__capture_queue = []
            self.__capture_files = []

            y = 0
            part = 0
            while y < end:
                fname = screenshot_filename(full_page_folder, f"part_{part}")
                self.__capture_queue.append((y, fname))
                y += step
                part += 1

            # 3) connect the signal and start the capture chain
            self.__ensure_connected()

            # small initial delay
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(120, loop.quit)
            loop.exec()

            self.__scroll_and_shoot()

        current_widget.javaScriptResult.connect(on_javascript_result)

    def start(self):
        try:
            self.started.emit()
            self.take_screenshot(
                acquisition_directory=self.options["acquisition_directory"],
                current_widget=self.options["current_widget"],
                screenshot_directory=self.options["screenshot_directory"],
                is_task=True,
            )
            self.finished.emit()
        except Exception as e:
            debug(
                "Exception during screenshot task:",
                str(e),
                context=get_context(self),
            )
            log_exception(e, context=get_context(self))
            self.error.emit(
                {
                    "title": self.__translations["SCREENSHOT_ERROR_TITLE"],
                    "message": self.__translations[
                        "FULL_PAGE_SCREENSHOT_ERROR_MESSAGE"
                    ],
                    "details": str(e),
                }
            )


class TaskFullPageScreenShot(Task):
    def __init__(self, logger, progress_bar=None, status_bar=None):

        self.__translations = load_translations()

        super().__init__(
            logger,
            progress_bar,
            status_bar,
            label=self.__translations["FULL_PAGE_SCREENSHOT"],
        )

        self.__worker = TaskFullPageScreenShotWorker()
        self.__worker.started.connect(self._started)
        self.__worker.finished.connect(self._finished)
        self.__worker.error.connect(self._handle_error)

    def start(self):
        super().start_task(self.__translations["FULL_PAGE_SCREENSHOT_STARTED"])
        self.__worker.options = self.options
        self.__worker.start()

    def _finished(self, status=Status.SUCCESS, details=""):
        super()._finished(
            status,
            details,
            self.__translations["FULL_PAGE_SCREENSHOT_COMPLETED"].format(status.name),
        )
