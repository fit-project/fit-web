#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: GPL-3.0-only
# -----
######

import logging
import logging.config
import os

import pytest
from fit_common.core import resolve_path
from fit_common.gui.utils import State, Status
from fit_configurations.logger import LogConfigTools
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QLabel, QMainWindow, QProgressBar, QVBoxLayout, QWidget

from fit_web.lang import load_translations
from fit_web.tasks.save_page import TaskSavePage
from fit_web.web_profile import WebEnginePage
from fit_web.web_view import WebEngineView

translations = load_translations()
logger = logging.getLogger("view.scrapers.web.web")


@pytest.fixture(scope="module")
def test_folder():
    folder = resolve_path("acquisition/tasks/save_page_test_folder")
    os.makedirs(folder, exist_ok=True)
    return folder


@pytest.fixture
def task_instance(qtbot, test_folder):
    window = QMainWindow()
    qtbot.addWidget(window)

    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)

    web_view = WebEngineView()
    web_view.set_download_request_handler()

    page = WebEnginePage(web_view)
    page.certificateError.connect(page.handleCertificateError)
    web_view.setPage(page)

    progress_bar = QProgressBar()
    status_bar = QLabel()
    layout.addWidget(web_view)
    layout = QVBoxLayout(web_view)
    layout.addWidget(progress_bar)
    layout.addWidget(status_bar)

    window.setCentralWidget(central_widget)
    window.resize(1024, 768)

    web_view.setUrl(QUrl("https://example.com"))
    with qtbot.waitSignal(web_view.loadFinished, timeout=10000):
        pass

    log_tools = LogConfigTools()
    log_tools.set_dynamic_loggers()
    log_tools.change_filehandlers_path(test_folder)
    logging.config.dictConfig(log_tools.config)

    task = TaskSavePage(
        logger,
        progress_bar=progress_bar,
        status_bar=status_bar,
    )

    task.options = {
        "acquisition_directory": test_folder,
        "current_widget": web_view,
    }

    task._test_window = window

    return task


def test_init_save_page_task(task_instance):
    task = task_instance

    assert task.label == translations["SAVE_PAGE"]
    assert task.state == State.INITIALIZATED
    assert task.status == Status.SUCCESS


def test_save_page_task(task_instance, qtbot):
    task = task_instance

    with qtbot.waitSignal(task.started, timeout=3000):
        task.start()

    assert task.state == State.STARTED
    assert task.status == Status.SUCCESS
    assert task.details == ""

    with qtbot.waitSignal(task.finished, timeout=3000):
        pass

    assert task.state == State.COMPLETED
    assert task.status == Status.SUCCESS

    expected_file = os.path.join(
        task.options["acquisition_directory"], "acquisition_page", "example.com.html"
    )
    assert os.path.exists(expected_file)
