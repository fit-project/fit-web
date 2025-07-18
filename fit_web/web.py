# !/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: LGPL-3.0-or-later
# -----
######

import logging
import os

from fit_acquisition.class_names import *
from fit_configurations.controller.tabs.general.general import GeneralController
from fit_scraper.scraper import AcquisitionStatus, Scraper
from PySide6 import QtCore
from PySide6.QtWebEngineCore import (
    QWebEngineProfile,
)

from fit_web.web_ui import (
    Ui_fit_web,
)


class Web(Scraper):
    def __init__(self, wizard=None):
        logger = logging.getLogger("view.scrapers.web.web")
        packages = []
        super().__init__(logger, "web", packages, wizard)
        if self.has_valid_case:
            self.acquisition.start_tasks = [SCREENRECORDER, PACKETCAPTURE]
            self.acquisition.stop_tasks = [
                WHOIS,
                NSLOOKUP,
                HEADERS,
                SSLKEYLOG,
                SSLCERTIFICATE,
                TRACEROUTE,
                SCREENRECORDER,
                PACKETCAPTURE,
            ]

            self.__init_ui()

    def __init_ui(self):
        # HIDE STANDARD TITLE BAR
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.ui = Ui_fit_web()
        self.ui.setupUi(self)

        # CUSTOM TOP BAR
        self.ui.left_box.mouseMoveEvent = self.move_window

        # MINIMIZE BUTTON
        self.ui.minimize_button.clicked.connect(self.showMinimized)

        # CLOSE BUTTON
        self.ui.close_button.clicked.connect(self.close)

        # SET VERSION
        self.ui.version.setText(self._get_version())

        # CONFIGURATION BUTTON
        self.ui.configuration_button.clicked.connect(self.configuration_dialog)

        # CASE BUTTON
        self.ui.case_button.clicked.connect(self.show_case_info)

        # PROGRESS BAR
        self.acquisition.progress_bar = self.ui.progress_bar

        # STATUS MESSAGE
        self.acquisition.status_bar = self.ui.status_message

        # RESET AND HIDE STATUS MESSAGE AND PROGRESS BAR
        self._reset_acquisition_indicators(False)

        # SET NAVIGATION BUTTONS
        self.ui.back_button.clicked.connect(self.__back)
        self.ui.forward_button.clicked.connect(self.__forward)
        self.ui.reload_button.clicked.connect(self.__reload)
        self.ui.home_button.clicked.connect(self.__navigate_home)
        self.ui.url_line_edit.returnPressed.connect(self.__navigate_to_url)
        self.ui.stop_button.clicked.connect(self.__stop_load_url)

        # SET GLOBAL ACQUISITON BUTTONS
        self.ui.start_acquisition_button.clicked.connect(
            self.__execute_start_tasks_flow
        )
        self.ui.stop_acquisition_button.clicked.connect(self.__execute_stop_tasks_flow)

        self.ui.tabs.clear()

        # Since 1.3.0 I disabled multitab managment, but I left these methods in case I wanted to re-enable multitab
        self.ui.tabs.tabBarDoubleClicked.connect(self.__tab_open_doubleclick)
        self.ui.tabs.currentChanged.connect(self.__current_tab_changed)
        self.ui.tabs.tabCloseRequested.connect(self.__close_current_tab)

        self.__enable_all()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def move_window(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    # START GLOBAL ACQUISITON METHODS
    def __execute_start_tasks_flow(self):
        if self.create_acquisition_directory():
            if self.create_acquisition_subdirectory("screenshot"):
                self.acquisition.options = {
                    "acquisition_directory": self.acquisition_directory,
                    "screenshot_directory": os.path.join(
                        self.acquisition_directory, "screenshot"
                    ),
                    "type": "web",
                    "case_info": self.case_info,
                    "current_widget": self.ui.tabs.currentWidget(),
                    "exclude_from_hash_calculation": "",
                    "window_pos": self.pos(),
                }

                super().execute_start_tasks_flow()

                self.__enable_all()

    def __execute_stop_tasks_flow(self):

        url = self.ui.tabs.currentWidget().url().toString()
        self.ui.tabs.currentWidget().page().reset_default_path()
        self.acquisition.options["url"] = url
        self.acquisition.options["current_widget"] = self.ui.tabs.currentWidget()

        super().execute_stop_tasks_flow()

        self.__enable_all()

    # END GLOBAL ACQUISITON METHODS

    # START ACQUISITON EVENTS
    def on_start_tasks_finished(self):
        print("finito di eseguire tutti i task della lista di Acquisition start_tasks")
        return super().on_start_tasks_finished()

    def on_stop_tasks_finished(self):
        self.acquisition.start_post_acquisition()
        print("finito di eseguire tutti i task della lista di Acquisition  stop_tasks")

    def on_post_acquisition_finished(self):
        print("finito di eseguire tutti i task della lista di Acquisition post_tasks")

        profile = QWebEngineProfile.defaultProfile()
        profile.clearHttpCache()

        try:
            self.ui.tabs.currentWidget().saveResourcesFinished.disconnect()
        except TypeError:
            pass

        super().on_post_acquisition_finished()

        self.__enable_all()

    # END ACQUISITON EVENTS

    # START NAVIGATION METHODS
    def __back(self):
        self.ui.tabs.currentWidget().back()

    def __forward(self):
        self.ui.tabs.currentWidget().forward()

    def __reload(self):
        self.ui.tabs.currentWidget().reload()

    def __navigate_home(self):
        self.ui.tabs.currentWidget().setUrl(
            QtCore.QUrl(GeneralController().configuration["home_page_url"])
        )

    def __navigate_to_url(self):  # Does not receive the Url
        q = QtCore.QUrl(self.url_line_edit.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.ui.tabs.currentWidget().setUrl(q)

    def __stop_load_url(self):
        self.ui.tabs.currentWidget().stop()

    # END NAVIGATION METHODS

    # START TAB METHODS
    def __tab_open_doubleclick(self, i):
        if i == -1 and self.isEnabled():  # No tab under the click
            self.add_new_tab()

    def __current_tab_changed(self, i):
        if self.tabs.currentWidget() is not None:
            qurl = self.tabs.currentWidget().url()
            self.__update_urlbar(qurl, self.tabs.currentWidget())
            self.update_title(self.tabs.currentWidget())

    def __close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    # END TAB METHODS

    def __enable_all(self):
        if self.acquisition_status in (
            AcquisitionStatus.UNSTARTED,
            AcquisitionStatus.FINISHED,
        ):
            self.__enable_screenshot_buttons(False)
            self.__enable_navigation_buttons(True)
            self.setEnabled(True)
        elif self.acquisition_status == AcquisitionStatus.STARTED:
            self.__enable_screenshot_buttons(True)
            self.__enable_navigation_buttons(True)
            self.setEnabled(True)
        elif self.acquisition_status == AcquisitionStatus.STOPPED:
            self.setEnabled(False)

        self.__enable_acquisition_buttons()

    def __enable_acquisition_buttons(self):
        if self.acquisition_status in (
            AcquisitionStatus.UNSTARTED,
            AcquisitionStatus.FINISHED,
        ):
            stop = False
            start = True
        elif self.acquisition_status == AcquisitionStatus.STARTED:
            start = False
            stop = True
        elif self.acquisition_status == AcquisitionStatus.STOPPED:
            stop = start = False

        self.ui.start_acquisition_button.setEnabled(start)
        self.ui.stop_acquisition_button.setEnabled(stop)

    def __enable_screenshot_buttons(self, enable):
        self.ui.screenshot_visible_area_button.setEnabled(enable)
        self.ui.screenshot_selected_area_button.setEnabled(enable)
        self.ui.screenshot_full_page_button.setEnabled(enable)

    def __enable_navigation_buttons(self, enable):
        self.ui.back_button.setEnabled(enable)
        self.ui.forward_button.setEnabled(enable)
        self.ui.reload_button.setEnabled(enable)
        self.ui.home_button.setEnabled(enable)
        self.ui.url_line_edit.setEnabled(enable)
        self.ui.stop_button.setEnabled(enable)
