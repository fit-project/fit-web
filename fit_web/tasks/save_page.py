#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: GPL-3.0-only
# -----
######


import os
import traceback

from fit_acquisition.tasks.task import Task
from fit_acquisition.tasks.task_worker import TaskWorker
from fit_common.gui.utils import Status

from fit_web.lang import load_translations


class TaskSavePageWorker(TaskWorker):

    def __init__(self):
        super().__init__()
        self.__translations = load_translations()

    def start(self):
        try:
            self.started.emit()

            self.acquisition_directory = self.options["acquisition_directory"]
            self.current_widget = self.options["current_widget"]

            acquisition_page_folder = os.path.join(
                self.acquisition_directory, "acquisition_page"
            )
            if not os.path.isdir(acquisition_page_folder):
                os.makedirs(acquisition_page_folder)
            self.current_widget.saveResourcesFinished.connect(self.__finished)
            self.current_widget.save_resources(acquisition_page_folder)

        except Exception as e:
            print(f"{str(e)}\n\n{traceback.format_exc()}")
            self.error.emit(
                {
                    "title": self.__translations["SAVE_PAGE_ERROR_TITLE"],
                    "message": self.__translations["SAVE_PAGE_ERROR_MESSAGE"],
                    "details": str(e),
                }
            )

    def __finished(self):
        self.finished.emit()


class TaskSavePage(Task):
    def __init__(self, logger, progress_bar=None, status_bar=None):

        self.__translations = load_translations()

        super().__init__(
            logger,
            progress_bar,
            status_bar,
            label=self.__translations["SAVE_PAGE"],
        )

        self.__worker = TaskSavePageWorker()
        self.__worker.started.connect(self._started)
        self.__worker.finished.connect(self._finished)
        self.__worker.error.connect(self._handle_error)

    def start(self):
        super().start_task(self.__translations["SAVE_PAGE_STARTED"])
        self.__worker.options = self.options
        self.__worker.start()

    def _finished(self, status=Status.SUCCESS, details=""):
        super()._finished(
            status,
            details,
            self.__translations["SAVE_PAGE_COMPLETED"].format(status.name),
        )
