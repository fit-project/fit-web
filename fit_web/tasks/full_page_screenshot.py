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

import numpy as np
from fit_acquisition.tasks.task import Task
from fit_acquisition.tasks.task_worker import TaskWorker
from fit_common.core import debug, log_exception
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

    def take_screenshot(
        self,
        acquisition_directory,
        current_widget,
        screenshot_directory=None,
        is_task=False,
    ):

        current_widget = current_widget
        acquisition_directory = acquisition_directory

        if acquisition_directory is not None:
            full_page_folder = os.path.join(
                acquisition_directory
                + "/full_page/{}/".format(current_widget.url().host())
            )
            if not os.path.isdir(full_page_folder):
                os.makedirs(full_page_folder)

            start_point_y = current_widget.page().scrollPosition().y()

            # move page on top
            current_widget.page().runJavaScript("window.scrollTo(0, 0);")

            next = 0
            part = 0
            step = current_widget.height()
            end = current_widget.page().contentsSize().toSize().height()
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(500, loop.quit)
            loop.exec()

            images = []

            while next < end:
                filename = screenshot_filename(full_page_folder, "part_" + str(part))
                if next == 0:
                    current_widget.grab().save(filename)
                else:
                    current_widget.page().runJavaScript(
                        "window.scrollTo({}, {});".format(0, next)
                    )

                    ### Waiting everything is synchronized
                    loop = QtCore.QEventLoop()
                    QtCore.QTimer.singleShot(500, loop.quit)
                    loop.exec()
                    current_widget.grab().save(filename)

                images.append(filename)

                part += 1
                next += step

            # combine all images part in an unique image
            imgs = [Image.open(i) for i in images]
            # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
            min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]

            # for a vertical stacking it is simple: use vstack
            imgs_comb = np.vstack([i.resize(min_shape) for i in imgs])
            imgs_comb = Image.fromarray(imgs_comb)

            whole_img_filename = screenshot_filename(
                screenshot_directory, "full_page" + ""
            )
            if is_task:
                whole_img_filename = os.path.join(
                    acquisition_directory, "screenshot.png"
                )

            imgs_comb.save(whole_img_filename)

            if is_task is not True:
                current_widget.page().runJavaScript(
                    f"window.scrollTo(0, {start_point_y});"
                )

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
                context="ScreenshotTask.start",
            )
            log_exception(e, context="ScreenshotTask.start")
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
