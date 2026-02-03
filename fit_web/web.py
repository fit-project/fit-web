# !/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: LGPL-3.0-or-later
# -----
######

import atexit
import logging
import os

from fit_acquisition.class_names import class_names
from fit_common.core import debug, get_context, get_version
from fit_common.gui.error import Error
from fit_configurations.controller.tabs.general.general import GeneralController
from fit_scraper.scraper import AcquisitionStatus, Scraper
from fit_webview_bridge import SystemWebView
from PySide6 import QtCore, QtGui, QtWidgets

from fit_web.lang import load_translations
from fit_web.mitmproxy.runner import MitmproxyRunner
from fit_web.os_proxy_setup import ProxyState, get_proxy_manager
from fit_web.selected_area_screenshot import SelectAreaScreenshot
from fit_web.tasks.full_page_screenshot import (
    TaskFullPageScreenShotWorker,
    screenshot_filename,
)
from fit_web.web_ui import (
    Ui_fit_web,
)


class Web(Scraper):
    def __init__(self, wizard=None):
        logger = logging.getLogger("scrapers.web")
        packages = ["fit_web.tasks"]

        super().__init__(logger, "web", packages, wizard)

        if self.has_valid_case:

            class_names.register("SAVE_PAGE", "TaskSavePage")
            class_names.register("FULL_PAGE_SCREENSHOT", "TaskFullPageScreenShot")

            self.acquisition.start_tasks = [
                class_names.PACKETCAPTURE,
            ]
            self.acquisition.stop_tasks = [
                class_names.WHOIS,
                class_names.NSLOOKUP,
                class_names.HEADERS,
                class_names.SSLKEYLOG,
                class_names.SSLCERTIFICATE,
                class_names.TRACEROUTE,
                class_names.PACKETCAPTURE,
                class_names.SAVE_PAGE,
            ]

            self.acquisition.external_tasks = [class_names.FULL_PAGE_SCREENSHOT]

            self.mitm_runner = MitmproxyRunner(self)
            self.proxy_manager = get_proxy_manager()
            self.proxy_state: ProxyState | None = None
            atexit.register(self.__restore_os_proxy)

            self.__translations = load_translations()
            self.__init_ui()
            self.__enable_all()
            self.__add_new_tab(
                QtCore.QUrl(GeneralController().configuration["home_page_url"]),
                "Homepage",
            )

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
        self.ui.version.setText(f"v{get_version()}")

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

        # SET LOCAL ACQUISITON BUTTONS
        self.ui.screenshot_visible_area_button.clicked.connect(self.__take_screenshot)
        self.ui.screenshot_selected_area_button.clicked.connect(
            self.__take_screenshot_selected_area
        )

        self.ui.screenshot_full_page_button.clicked.connect(
            self.__take_full_page_screenshot
        )
        self.ui.screenshot_full_page_button.setEnabled(True)

        self.ui.tabs.clear()

        # Since 1.3.0 I disabled multitab managment, but I left these methods in case I wanted to re-enable multitab
        self.ui.tabs.tabBarDoubleClicked.connect(self.__tab_open_doubleclick)
        self.ui.tabs.currentChanged.connect(self.__current_tab_changed)
        self.ui.tabs.tabCloseRequested.connect(self.__close_current_tab)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def move_window(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    # START GLOBAL ACQUISITON METHODS
    def __execute_start_tasks_flow(self):
        debug("ℹ️ __execute_start_tasks_flow called", context=get_context(self))
        if self.create_acquisition_directory():
            debug("ℹ️ acquisition directory created", context=get_context(self))
            if self.create_acquisition_subdirectory("screenshot"):
                debug("ℹ️ screenshot subdirectory created", context=get_context(self))
                if self.create_acquisition_subdirectory("downloads"):
                    debug("ℹ️ downloads subdirectory created", context=get_context(self))
                    self.ui.tabs.currentWidget().setDownloadDirectory(
                        os.path.join(self.acquisition_directory, "downloads")
                    )
                    self.screenshot_directory = os.path.join(
                        self.acquisition_directory, "screenshot"
                    )
                    self.acquisition.options = {
                        "acquisition_directory": self.acquisition_directory,
                        "screenshot_directory": self.screenshot_directory,
                        "type": "web",
                        "case_info": self.case_info,
                        "current_widget": self.ui.tabs.currentWidget(),
                        "window_pos": self.pos(),
                    }

                    debug("ℹ️ configuring OS proxy", context=get_context(self))
                    if not self.__configure_os_proxy():
                        error_dlg = Error(
                            QtWidgets.QMessageBox.Icon.Critical,
                            self.__translations["OS_PROXY_CONFIG_ERROR_TITLE"],
                            self.__translations["OS_PROXY_CONFIG_ERROR_MESSAGE"],
                            "",
                        )
                        error_dlg.exec()
                        return

                    debug("ℹ️ starting mitm capture", context=get_context(self))
                    if not self.__start_mitm_capture():
                        self.__restore_os_proxy()
                        error_dlg = Error(
                            QtWidgets.QMessageBox.Icon.Critical,
                            self.__translations["MITM_PROXY_ERROR_TITLE"],
                            self.__translations["MITM_PROXY_ERROR_MESSAGE"],
                            "",
                        )
                        error_dlg.exec()

                        return

                    super().execute_start_tasks_flow()

                    self.__enable_all()

    def __execute_stop_tasks_flow(self):
        debug("ℹ️ __execute_stop_tasks_flow called", context=get_context(self))
        self.acquisition_status = AcquisitionStatus.STOPPED
        self.acquisition.log_stop_message()
        self._reset_acquisition_indicators(True)
        self.__enable_all()

        debug("ℹ️ stopping mitm capture", context=get_context(self))
        if not self.__stop_mitm_capture():
            debug(
                "❌ Unable to stop mitm capture cleanly",
                context=get_context(self),
            )

        debug("ℹ️ restore configuring OS proxy", context=get_context(self))
        if not self.__restore_os_proxy():
            debug(
                "❌ Unable to restore OS proxy cleanly",
                context=get_context(self),
            )

        debug(
            f"ℹ️ stop loop: thread={QtCore.QThread.currentThread()} "
            f"app_thread={QtCore.QCoreApplication.instance().thread() if QtCore.QCoreApplication.instance() else None}",
            context=get_context(self),
        )
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(500, loop.quit)
        loop.exec()
        debug("ℹ️ stop loop: done", context=get_context(self))

        url = self.ui.tabs.currentWidget().url().toString()
        self.acquisition.options["url"] = url
        self.acquisition.options["current_widget"] = self.ui.tabs.currentWidget()
        debug("ℹ️ before start TaskFullPageScreenShot", context=get_context(self))
        task = self.acquisition.tasks_manager.get_task("TaskFullPageScreenShot")
        debug("ℹ️ after start TaskFullPageScreenShot", context=get_context(self))
        if task:
            task.finished.connect(self.execute_stop_tasks_flow)
            task.options = self.acquisition.options
            task.increment = self.acquisition.calculate_increment()
            task.start()
        else:
            self.execute_stop_tasks_flow()

    # END GLOBAL ACQUISITON METHODS

    # START ACQUISITON EVENTS
    def on_start_tasks_finished(self):
        debug(
            "ℹ️ Finished executing all tasks in the start_tasks list of Acquisition.",
            context=get_context(self),
        )
        return super().on_start_tasks_finished()

    def on_stop_tasks_finished(self):
        debug(
            "ℹ️ Finished executing all tasks in the stop_tasks list of Acquisition.",
            context=get_context(self),
        )

        return super().on_stop_tasks_finished()

    def execute_stop_tasks_flow(self):
        self.tasks_info.show()
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(500, loop.quit)
        loop.exec()
        self.acquisition.run_stop_tasks()

    def on_post_acquisition_finished(self):
        debug(
            "Finished executing all tasks in the Acquisition post_tasks list",
            context="Web.on_post_acquisition_finished",
        )

        super().on_post_acquisition_finished()

        self.__enable_all()

    # END ACQUISITON EVENTS

    # START LOCAL ACQUISITON METHODS
    def __take_screenshot(self):
        if not self.screenshot_directory:
            return

        self.setEnabled(False)
        view = self.ui.tabs.currentWidget()

        # assicura che la cartella esista
        os.makedirs(self.screenshot_directory, exist_ok=True)

        # slot: firma corretta + filtro token (se fai più scatti ravvicinati)
        def on_capture_finished(token, ok, filePath, error):
            if token != getattr(self, "_last_capture_token", None):
                return  # evento di un vecchio scatto, ignora

            try:
                view.captureFinished.disconnect(on_capture_finished)
            except Exception:
                pass

            self.setEnabled(True)

            if ok:
                print(f"[screenshot] saved → {filePath}")
            else:
                print(f"[screenshot] FAILED: {error}")

            self._last_capture_token = None

        # collega PRIMA di chiamare captureVisiblePage
        view.captureFinished.connect(on_capture_finished)

        # (facoltativo) piccola attesa per stabilizzare il layout
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(100, loop.quit)
        loop.exec()

        filename = screenshot_filename(self.screenshot_directory, view.url().host())
        # salva il token per filtrare il callback
        self._last_capture_token = view.captureVisiblePage(filename)

    def __take_screenshot_selected_area(self):
        if self.screenshot_directory is not None:
            self.setEnabled(False)
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(500, loop.quit)
            loop.exec()
            filename = screenshot_filename(
                self.screenshot_directory,
                "selected_" + self.ui.tabs.currentWidget().url().host(),
            )
            select_area = SelectAreaScreenshot(filename, self)
            select_area.finished.connect(self.__enable_all)
            select_area.snip_area()

    def __take_full_page_screenshot(self):
        self.setEnabled(False)
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(500, loop.quit)
        loop.exec()
        TaskFullPageScreenShotWorker().take_screenshot(
            acquisition_directory=self.acquisition_directory,
            current_widget=self.ui.tabs.currentWidget(),
            screenshot_directory=self.screenshot_directory,
        )
        self.setEnabled(True)

    # END LOCAL ACQUISITON METHODS

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
        q = QtCore.QUrl(self.ui.url_line_edit.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.ui.tabs.currentWidget().setUrl(q)

    def __stop_load_url(self):
        self.ui.tabs.currentWidget().stop()

    def __update_urlbar(self, q, browser=None):
        if browser != self.ui.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return

        if q.scheme() == "https":
            # Secure padlock icon
            self.ui.httpsIcon.setPixmap(
                QtGui.QPixmap(":/images/toolbar/images/toolbar/lock-close.png")
            )
        else:
            # Insecure padlock icon
            self.ui.httpsIcon.setPixmap(
                QtGui.QPixmap(":/images/toolbar/images/toolbar/lock-open.png")
            )

        self.ui.url_line_edit.setText(q.toString())
        self.ui.url_line_edit.setCursorPosition(0)

    # END NAVIGATION METHODS

    # START TAB METHODS
    def __add_new_tab(self, qurl=None, label="Blank", page=None):

        if qurl is None:
            qurl = QtCore.QUrl("")

        web_view = SystemWebView()
        user_agent = GeneralController().configuration["user_agent"]

        web_view.setUserAgent(user_agent)

        web_view.urlChanged.connect(
            lambda qurl, browser=web_view: self.__update_urlbar(qurl, browser)
        )

        web_view.downloadStarted.connect(self.__handle_download_item_started)
        web_view.downloadProgress.connect(self.__handle_download_item_progress)
        web_view.downloadFinished.connect(self.__handle_download_item_finished)

        web_view.setUrl(qurl)
        i = self.ui.tabs.addTab(web_view, label)
        self.ui.tabs.setCurrentIndex(i)

        if i == 0:
            self.showMaximized()

        if i == 0:
            self.showMaximized()

    def __tab_open_doubleclick(self, i):
        if i == -1 and self.isEnabled():  # No tab under the click
            self.__add_new_tab()

    def __current_tab_changed(self, i):
        if self.ui.tabs.currentWidget() is not None:
            qurl = self.ui.tabs.currentWidget().url()
            self.__update_urlbar(qurl, self.ui.tabs.currentWidget())
            self.update_title(self.ui.tabs.currentWidget())

    def __close_current_tab(self, i):
        if self.ui.tabs.count() < 2:
            return

        self.ui.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.ui.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return

        # title = self.ui.tabs.currentWidget().page().title()
        # Since 1.3.0 self.setWindowTitle("%s - Freezing Internet Tool" % title)

    # END TAB METHODS

    # START DOWNLOAD METHODS
    def __handle_download_item_started(self, download):
        self._reset_acquisition_indicators(True)

    def __handle_download_item_progress(self, bytes_received, bytes_total):
        if bytes_total > 0:
            download_percentage = int(bytes_received * 100 / bytes_total)
            self.acquisition.progress_bar.setValue(download_percentage)

    def __handle_download_item_finished(self, download):
        filename = download.downloadFileName()
        directory = download.downloadDirectory()
        filename = os.path.join(directory, filename)
        url = download.downloadUrl()

        for index in range(self.ui.tabs.count()):
            if self.ui.tabs.widget(index).url() == url:
                self.ui.tabs.setCurrentIndex(index - 1)
                self.ui.tabs.removeTab(index)

        self.acquisition.status_bar.setText(
            self.__translations["DOWNLOADED"] + ": " + filename
        )
        self.acquisition.progress_bar.setValue(100)
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(2000, loop.quit)
        loop.exec()

        self._reset_acquisition_indicators(False)

    # END DOWNLOAD METHODS

    def __enable_all(self):
        # TODO devo bloccare anche close e minize
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

    def __restore_os_proxy(self) -> bool:
        if self.proxy_manager and self.proxy_state:
            if not hasattr(self.proxy_manager, "restore"):
                return False
            self.proxy_manager.restore(self.proxy_state)
        self.proxy_manager = None
        self.proxy_state = None
        return True

    def __configure_os_proxy(self) -> bool:
        debug("ℹ️ __configure_os_proxy called", context=get_context(self))
        if self.proxy_manager is None:
            self.proxy_manager = get_proxy_manager()
        if self.proxy_manager is None:
            debug("❌ Proxy manager not available", context=get_context(self))
            return False
        if not hasattr(self.proxy_manager, "snapshot") or not hasattr(
            self.proxy_manager, "enable_capture_proxy"
        ):
            debug(
                "❌ Proxy manager missing required methods", context=get_context(self)
            )
            return False

        self.proxy_state = self.proxy_manager.snapshot()
        if self.proxy_state is None:
            debug("❌ Proxy snapshot failed", context=get_context(self))
            self.proxy_manager = None
            return False

        self.proxy_manager.enable_capture_proxy("127.0.0.1", 8080)
        debug("✅ Proxy enabled for capture", context=get_context(self))
        return True

    def __start_mitm_capture(self) -> bool:
        if self.mitm_runner.start_capture():
            debug("✅ Mitm capture started", context=get_context(self))
            return True
        debug("❌ Mitm capture start failed", context=get_context(self))
        return False

    def __stop_mitm_capture(self) -> bool:

        if self.mitm_runner.stop_capture():
            debug("✅ Mitm capture stopped", context=get_context(self))
            return True
        debug("❌ Mitm capture stop failed", context=get_context(self))
        return False

    def closeEvent(self, event):
        # TODO da verificare se va bene così con wizard oppure se sta acquisendo
        self.mitm_runner.stop_by_pid()
        return super().closeEvent(event)
