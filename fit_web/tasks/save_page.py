#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: GPL-3.0-only
# -----
######


import os

from fit_common.gui.utils import Status
from fit_acquisition.tasks.task import Task
from fit_web.lang import load_translations


class TaskSavePage(Task):
    def __init__(self, logger, progress_bar=None, status_bar=None):

        self.__translations = load_translations()

        super().__init__(
            logger,
            progress_bar,
            status_bar,
            label=self.__translations["SAVE_PAGE"],
        )

    def start(self):
        try:
            super().start_task(self.__translations["SAVE_PAGE_STARTED"])

            self.acquisition_directory = self.options["acquisition_directory"]
            self.current_widget = self.options["current_widget"]

            acquisition_page_folder = os.path.join(
                self.acquisition_directory, "acquisition_page"
            )
            if not os.path.isdir(acquisition_page_folder):
                os.makedirs(acquisition_page_folder)
            self.current_widget.saveResourcesFinished.connect(self._finished)
            self.current_widget.save_resources(acquisition_page_folder)

        except Exception as e:
            error_details = str(e)
            self._handle_error({"details": error_details})

    def _finished(self, status=Status.SUCCESS, details=""):
        super()._finished(status, details, self.__translations["SAVE_PAGE_COMPLETED"])
