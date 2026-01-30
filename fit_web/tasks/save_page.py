#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: GPL-3.0-only
# -----
######


import os
import shutil
import tempfile
import zipfile

from fit_acquisition.tasks.task import Task
from fit_acquisition.tasks.task_worker import TaskWorker
from fit_bootstrap.constants import FIT_USER_APP_PATH
from fit_common.core import debug, get_context, log_exception
from fit_common.gui.utils import Status
from har2warc.har2warc import har2warc
from wacz import main as wacz_main

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
            debug("ℹ️ Starting WACZ build", context=get_context(self))
            self._build_wacz()
            debug("✅ WACZ build completed", context=get_context(self))
            self.finished.emit()

        except Exception as e:
            debug(
                "Exception during save page task:",
                str(e),
                context=get_context(self),
            )
            log_exception(e, context=get_context(self))
            self.error.emit(
                {
                    "title": self.__translations["SAVE_PAGE_ERROR_TITLE"],
                    "message": self.__translations["SAVE_PAGE_ERROR_MESSAGE"],
                    "details": str(e),
                }
            )

    def _get_capture_har_path(self) -> str | None:
        base_path = os.environ.get(FIT_USER_APP_PATH)
        if not base_path:
            return None
        return os.path.join(base_path, "mitmproxy", "capture.har")

    def _build_wacz(self) -> None:
        har_path = self._get_capture_har_path()
        if not har_path or not os.path.exists(har_path):
            raise FileNotFoundError("capture.har not found")
        debug(f"ℹ️ capture.har: {har_path}", context=get_context(self))
        with tempfile.TemporaryDirectory(
            prefix="fit_wacz_", dir=self.acquisition_directory
        ) as temp_dir:
            debug(f"ℹ️ wacz temp_dir: {temp_dir}", context=get_context(self))
            warc_path = os.path.join(temp_dir, "data.warc.gz")
            debug("ℹ️ Converting HAR to WARC", context=get_context(self))
            har2warc(
                har_path,
                warc_path,
                gzip=True,
                filename=warc_path,
                rec_title="FIT capture",
            )
            debug(f"✅ WARC created: {warc_path}", context=get_context(self))

            wacz_path = os.path.join(temp_dir, "archive.wacz")
            debug("ℹ️ Creating WACZ archive", context=get_context(self))
            result = wacz_main.main(
                [
                    "create",
                    warc_path,
                    "-o",
                    wacz_path,
                    "--detect-pages",
                    "--text",
                ]
            )
            if result not in (0, None):
                raise RuntimeError(f"WACZ creation failed (code={result})")
            debug(f"✅ WACZ created: {wacz_path}", context=get_context(self))

            final_wacz = os.path.join(
                self.acquisition_directory, "archive.wacz"
            )
            shutil.copyfile(wacz_path, final_wacz)
            debug(f"✅ WACZ saved: {final_wacz}", context=get_context(self))


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
