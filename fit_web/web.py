# !/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: LGPL-3.0-or-later
# -----
######

import atexit
import json
import logging
import os

from fit_acquisition.class_names import class_names
from fit_acquisition.logger_names import LoggerName
from fit_bootstrap.constants import FIT_MITM_PORT
from fit_common.core import AcquisitionType, debug, get_context, get_version
from fit_common.gui.error import Error
from fit_common.gui.ui_translation import translate_ui
from fit_configurations.controller.tabs.general.general import GeneralController
from fit_scraper.scraper import AcquisitionStatus, Scraper
from fit_verify_pdf_timestamp.view.verify_pdf_timestamp import (
    VerifyPDFTimestamp as VerifyPDFTimestampView,
)
from fit_verify_pec.view.verify_pec import VerifyPec as VerifyPecView
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
        logger = logging.getLogger(LoggerName.SCRAPER_WEB.value)
        packages = ["fit_web.tasks"]

        super().__init__(logger, AcquisitionType.WEB, packages, wizard)

        if self.has_valid_case:

            class_names.register("SAVE_PAGE", "TaskSavePage")
            class_names.register("FULL_PAGE_SCREENSHOT", "TaskFullPageScreenShot")

            self.acquisition.start_tasks = [
                class_names.PACKETCAPTURE,
                class_names.SCREENRECORDER,
            ]
            self.acquisition.stop_tasks = [
                class_names.WHOIS,
                class_names.NSLOOKUP,
                class_names.HEADERS,
                # class_names.SSLKEYLOG, # Removed since v3. See `docs/forensics/sslkey_log_forensic_reasoning_EN.md` for the forensic rationale
                class_names.SSLCERTIFICATE,
                class_names.TRACEROUTE,
                class_names.PACKETCAPTURE,
                class_names.SAVE_PAGE,
                class_names.SCREENRECORDER,
            ]

            self.acquisition.external_tasks = [class_names.FULL_PAGE_SCREENSHOT]

            self.mitm_runner = MitmproxyRunner(self)
            self.proxy_manager = get_proxy_manager()
            self.proxy_state: ProxyState | None = None
            self.__download_progress_debug_last = -1
            self.__default_download_directory = os.path.join(
                os.path.expanduser("~"), "Downloads"
            )
            atexit.register(self.__restore_os_proxy)

            self.__translations = load_translations()
            self.__find_bar = None
            self.__find_input = None
            self.__find_counter = None
            self.__find_prev_button = None
            self.__find_next_button = None
            self.__find_close_button = None
            self.__find_query = ""
            self.__find_total = 0
            self.__find_index = 0
            self.__init_ui()
            self.__enable_all()
            self.__add_new_tab(
                QtCore.QUrl(GeneralController().configuration["home_page_url"]),
                "Homepage",
            )

            if os.environ.get("FIT_EXECUTION_ENV", "") == "LOCAL_PC":
                self.__show_http_https_disclaimer()

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

        # VERIFY TIMESTAMP BUTTON
        self.ui.verify_timestamp_button.clicked.connect(self.__verify_timestamp)
        if self.wizard is not None:
            self.ui.verify_timestamp_button.hide()

        # VERIFY PEC BUTTON
        self.ui.verify_pec_button.clicked.connect(self.__verify_pec)
        if self.wizard is not None:
            self.ui.verify_pec_button.hide()

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
        self.ui.screenshot_visible_area_button.clicked.connect(
            self.__take_screenshot_visible_area
        )
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
        self.ui.tabs.currentChanged.connect(self.__refresh_find_for_current_tab)

        self.__init_find_bar()
        self.__init_find_shortcuts()

        translate_ui(self.__translations, self)

    def eventFilter(self, watched, event):
        if (
            watched == self.ui.content_bottom
            and event.type() == QtCore.QEvent.Type.Resize
        ):
            self.__position_find_bar()
        return super().eventFilter(watched, event)

    def __init_find_bar(self):
        self.__find_bar = QtWidgets.QFrame(self.ui.content_bottom)
        self.__find_bar.setObjectName("find_bar")
        self.__find_bar.setFixedHeight(44)
        self.__find_bar.setStyleSheet(
            "QFrame#find_bar {"
            "  background-color: rgb(236, 236, 236);"
            "  border: 1px solid rgb(190, 190, 190);"
            "  border-radius: 10px;"
            "}"
            "QLineEdit#find_input {"
            "  border: none;"
            "  background: transparent;"
            "  color: rgb(30, 30, 30);"
            "  font-size: 14px;"
            "  padding: 0 8px;"
            "}"
            "QLabel#find_counter {"
            "  color: rgb(70, 70, 70);"
            "  font-size: 14px;"
            "}"
            "QPushButton#find_prev, QPushButton#find_next, QPushButton#find_close {"
            "  border: none;"
            "  border-radius: 6px;"
            "  background: transparent;"
            "  color: rgb(60, 60, 60);"
            "  min-width: 30px;"
            "  min-height: 30px;"
            "}"
            "QPushButton#find_prev:hover, QPushButton#find_next:hover, QPushButton#find_close:hover {"
            "  background: rgb(215, 215, 215);"
            "}"
        )

        bar_layout = QtWidgets.QHBoxLayout(self.__find_bar)
        bar_layout.setContentsMargins(10, 6, 10, 6)
        bar_layout.setSpacing(4)

        self.__find_input = QtWidgets.QLineEdit(self.__find_bar)
        self.__find_input.setObjectName("find_input")
        self.__find_input.setPlaceholderText("Find in page")
        self.__find_input.textChanged.connect(self.__on_find_text_changed)
        self.__find_input.returnPressed.connect(self.__on_find_return_pressed)

        self.__find_counter = QtWidgets.QLabel("0/0", self.__find_bar)
        self.__find_counter.setObjectName("find_counter")
        self.__find_counter.setMinimumWidth(56)
        self.__find_counter.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter
        )

        self.__find_prev_button = QtWidgets.QPushButton("^", self.__find_bar)
        self.__find_prev_button.setObjectName("find_prev")
        self.__find_prev_button.clicked.connect(self.__find_previous)

        self.__find_next_button = QtWidgets.QPushButton("v", self.__find_bar)
        self.__find_next_button.setObjectName("find_next")
        self.__find_next_button.clicked.connect(self.__find_next)

        self.__find_close_button = QtWidgets.QPushButton("X", self.__find_bar)
        self.__find_close_button.setObjectName("find_close")
        self.__find_close_button.clicked.connect(self.__hide_find_bar)

        separator_left = QtWidgets.QFrame(self.__find_bar)
        separator_left.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        separator_left.setStyleSheet("color: rgb(200, 200, 200);")
        separator_right = QtWidgets.QFrame(self.__find_bar)
        separator_right.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        separator_right.setStyleSheet("color: rgb(200, 200, 200);")

        bar_layout.addWidget(self.__find_input, 1)
        bar_layout.addWidget(separator_left, 0)
        bar_layout.addWidget(self.__find_counter, 0)
        bar_layout.addWidget(self.__find_prev_button, 0)
        bar_layout.addWidget(self.__find_next_button, 0)
        bar_layout.addWidget(separator_right, 0)
        bar_layout.addWidget(self.__find_close_button, 0)

        shadow = QtWidgets.QGraphicsDropShadowEffect(self.__find_bar)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 4)
        shadow.setColor(QtGui.QColor(0, 0, 0, 70))
        self.__find_bar.setGraphicsEffect(shadow)

        self.ui.content_bottom.installEventFilter(self)
        self.__find_bar.hide()
        self.__position_find_bar()

    def __init_find_shortcuts(self):
        self.__find_shortcut = QtGui.QShortcut(QtGui.QKeySequence.Find, self)
        self.__find_shortcut.setContext(QtCore.Qt.ShortcutContext.ApplicationShortcut)
        self.__find_shortcut.activated.connect(self.__show_find_bar)

        self.__find_next_shortcut = QtGui.QShortcut(QtGui.QKeySequence.FindNext, self)
        self.__find_next_shortcut.setContext(
            QtCore.Qt.ShortcutContext.ApplicationShortcut
        )
        self.__find_next_shortcut.activated.connect(self.__find_next)

        self.__find_prev_shortcut = QtGui.QShortcut(
            QtGui.QKeySequence.FindPrevious, self
        )
        self.__find_prev_shortcut.setContext(
            QtCore.Qt.ShortcutContext.ApplicationShortcut
        )
        self.__find_prev_shortcut.activated.connect(self.__find_previous)

        self.__find_close_shortcut = QtGui.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.Key.Key_Escape), self
        )
        self.__find_close_shortcut.setContext(
            QtCore.Qt.ShortcutContext.ApplicationShortcut
        )
        self.__find_close_shortcut.activated.connect(self.__hide_find_bar)

    def __position_find_bar(self):
        if not self.__find_bar:
            return
        parent = self.ui.content_bottom
        width = min(max(parent.width() - 40, 420), 620)
        self.__find_bar.setFixedWidth(width)
        x = max(0, (parent.width() - width) // 2)
        y = 10
        self.__find_bar.move(x, y)
        self.__find_bar.raise_()

    def __show_find_bar(self):
        if not self.__find_bar:
            return
        self.__find_bar.show()
        self.__position_find_bar()
        self.__find_input.setFocus()
        self.__find_input.selectAll()

    def __hide_find_bar(self):
        if not self.__find_bar:
            return
        self.__find_bar.hide()
        current = self.ui.tabs.currentWidget()
        if current and hasattr(current, "setFocus"):
            current.setFocus()

    def __refresh_find_for_current_tab(self, _index):
        if not self.__find_bar or not self.__find_bar.isVisible():
            return
        self.__run_find(reset=True, forward=True)

    def __on_find_text_changed(self, _text):
        self.__run_find(reset=True, forward=True)

    def __on_find_return_pressed(self):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers & QtCore.Qt.KeyboardModifier.ShiftModifier:
            self.__find_previous()
        else:
            self.__find_next()

    @staticmethod
    def __js_quote(value):
        escaped = value.replace("\\", "\\\\")
        escaped = escaped.replace("'", "\\'")
        escaped = escaped.replace("\n", "\\n").replace("\r", "\\r")
        return escaped

    def __request_js_result(self, widget, script, callback):
        token = widget.evaluateJavaScriptWithResult(script)

        def on_javascript_result(result, got_token, error):
            if got_token != token:
                return
            try:
                widget.javaScriptResult.disconnect(on_javascript_result)
            except (TypeError, RuntimeError):
                pass
            callback(result, error)

        widget.javaScriptResult.connect(on_javascript_result)

    def __set_find_counter(self, index, total):
        self.__find_index = max(0, int(index))
        self.__find_total = max(0, int(total))
        self.__find_counter.setText(f"{self.__find_index}/{self.__find_total}")
        if self.__find_total == 0:
            self.__find_counter.setStyleSheet(
                "color: rgb(170, 60, 60); font-size: 14px;"
            )
            self.__find_input.setStyleSheet(
                "border: 1px solid rgb(210, 120, 120);"
                "background: rgb(255, 245, 245);"
                "color: rgb(30, 30, 30);"
                "font-size: 14px;"
                "padding: 0 8px;"
                "border-radius: 6px;"
            )
        else:
            self.__find_counter.setStyleSheet(
                "color: rgb(70, 70, 70); font-size: 14px;"
            )
            self.__find_input.setStyleSheet(
                "border: none;"
                "background: transparent;"
                "color: rgb(30, 30, 30);"
                "font-size: 14px;"
                "padding: 0 8px;"
            )

    def __find_previous(self):
        self.__run_find(reset=False, forward=False)

    def __find_next(self):
        self.__run_find(reset=False, forward=True)

    def __run_find(self, reset, forward):
        current = self.ui.tabs.currentWidget()
        if not current or not hasattr(current, "evaluateJavaScriptWithResult"):
            self.__set_find_counter(0, 0)
            return

        term = self.__find_input.text()
        if not term:
            self.__find_query = ""
            self.__set_find_counter(0, 0)
            return

        escaped = self.__js_quote(term)
        query_changed = term != self.__find_query

        if reset or query_changed:
            script = (
                "(() => {"
                f"  const q = '{escaped}';"
                "  const body = document.body ? document.body.innerText : '';"
                "  const esc = q.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&');"
                "  let total = 0;"
                "  try { total = (body.match(new RegExp(esc, 'gi')) || []).length; } catch (_) {}"
                "  const found = window.find(q, false, false, true, false, false, false);"
                "  return JSON.stringify({ found: !!found, total });"
                "})()"
            )

            def on_reset_result(result, error):
                if error:
                    self.__set_find_counter(0, 0)
                    return
                try:
                    payload = (
                        result
                        if isinstance(result, dict)
                        else json.loads(result or "{}")
                    )
                except Exception:
                    payload = {"found": False, "total": 0}

                total = int(payload.get("total", 0) or 0)
                found = bool(payload.get("found", False))
                self.__find_query = term
                self.__set_find_counter(1 if found and total > 0 else 0, total)

            self.__request_js_result(current, script, on_reset_result)
            return

        script = (
            "(() => "
            f"window.find('{escaped}', false, {'false' if forward else 'true'}, true, false, false, false)"
            ")()"
        )

        def on_step_result(result, error):
            if error:
                return
            found = str(result).lower() == "true" or result is True
            if not found or self.__find_total <= 0:
                if not found:
                    self.__set_find_counter(0, self.__find_total)
                return
            if forward:
                next_index = (self.__find_index % self.__find_total) + 1
            else:
                next_index = (
                    (self.__find_index - 2 + self.__find_total) % self.__find_total
                ) + 1
            self.__set_find_counter(next_index, self.__find_total)

        self.__request_js_result(current, script, on_step_result)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def move_window(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    # START GLOBAL ACQUISITON METHODS
    def __execute_start_tasks_flow(self):
        self.setEnabled(False)
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(400, loop.quit)
        loop.exec()
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
                        self.setEnabled(True)
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
                        self.setEnabled(True)
                        return

                    # Give mitm a brief head start to pick up the "start" control signal.
                    loop = QtCore.QEventLoop()
                    QtCore.QTimer.singleShot(600, loop.quit)
                    loop.exec()

                    current_widget = self.ui.tabs.currentWidget()
                    if current_widget and hasattr(current_widget, "clearWebsiteData"):
                        try:
                            current_widget.clearWebsiteData()
                            debug(
                                "ℹ️ cleared webview website data before capture reload",
                                context=get_context(self),
                            )
                            loop = QtCore.QEventLoop()
                            QtCore.QTimer.singleShot(400, loop.quit)
                            loop.exec()
                        except Exception as exc:
                            debug(
                                f"❌ clearWebsiteData failed: {exc}",
                                context=get_context(self),
                            )

                    # Reload here so mitm can attach to the page that initiates acquisition traffic.
                    self.__reload()

                    super().execute_start_tasks_flow()

                    self.__enable_all()
                else:
                    debug(
                        "❌ Failed to create downloads directory",
                        context=get_context(self),
                    )
                    self.setEnabled(True)
            else:
                debug(
                    "❌ Failed to create screenshot directory",
                    context=get_context(self),
                )
                self.setEnabled(True)
        else:
            debug(
                "❌ Failed to create acquisition directory", context=get_context(self)
            )
            self.setEnabled(True)

    def __show_http_https_disclaimer(self) -> bool:
        title = self.__translations["HTTP_HTTPS_DISCLAIMER_TITLE"]
        message = self.__translations["HTTP_HTTPS_DISCLAIMER_MESSAGE"]
        error_dialog = Error(
            QtWidgets.QMessageBox.Icon.Warning,
            title,
            message,
            "",
        )
        error_dialog.exec()

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
        self.__restore_default_download_directory()

        self.__enable_all()

    # END ACQUISITON EVENTS

    # START LOCAL ACQUISITON METHODS
    def __take_screenshot_visible_area(self):
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

        filename = screenshot_filename(
            self.screenshot_directory, "visible_area_" + view.url().host()
        )
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
                "selected_area_" + self.ui.tabs.currentWidget().url().host(),
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

    def __restore_default_download_directory(self):
        for index in range(self.ui.tabs.count()):
            widget = self.ui.tabs.widget(index)
            if widget and hasattr(widget, "setDownloadDirectory"):
                widget.setDownloadDirectory(self.__default_download_directory)
        debug(
            f"ℹ️ restored default download directory={self.__default_download_directory}",
            context=get_context(self),
        )

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

        if hasattr(web_view, "navigationDisplayUrlChanged"):
            web_view.navigationDisplayUrlChanged.connect(
                lambda qurl, browser=web_view: self.__update_urlbar(qurl, browser)
            )
        else:
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
    def __handle_download_item_started(
        self, suggested_filename="", destination_path=""
    ):
        self.__download_progress_debug_last = -1
        # macOS bridge emits (suggestedFilename, destinationPath) as strings.
        # Keep this defensive to avoid runtime crashes on unexpected payloads.
        if hasattr(suggested_filename, "downloadFileName"):
            file_name = suggested_filename.downloadFileName()
        else:
            file_name = str(suggested_filename or "")
        if hasattr(destination_path, "downloadDirectory"):
            destination = destination_path.downloadDirectory()
        else:
            destination = str(destination_path or "")
        debug(
            "ℹ️ download started " f"file={file_name} " f"destination={destination}",
            context=get_context(self),
        )
        self._reset_acquisition_indicators(True)

    def __handle_download_item_progress(self, bytes_received, bytes_total):
        if bytes_total > 0:
            download_percentage = int(bytes_received * 100 / bytes_total)
            if download_percentage != self.__download_progress_debug_last:
                debug(
                    "ℹ️ download progress "
                    f"{download_percentage}% "
                    f"({bytes_received}/{bytes_total} bytes)",
                    context=get_context(self),
                )
                self.__download_progress_debug_last = download_percentage
            self.acquisition.progress_bar.setValue(download_percentage)
        else:
            if self.__download_progress_debug_last != -2:
                debug(
                    f"ℹ️ download progress unknown total bytes_received={bytes_received}",
                    context=get_context(self),
                )
                self.__download_progress_debug_last = -2

    def __handle_download_item_finished(self, download):
        filename_only = download.downloadFileName()
        directory = download.downloadDirectory()
        filename = os.path.join(directory, filename_only)
        url = download.downloadUrl()
        debug(
            "ℹ️ download finished " f"file={filename} " f"url={url.toString()}",
            context=get_context(self),
        )

        for index in range(self.ui.tabs.count()):
            if self.ui.tabs.widget(index).url() == url:
                debug(
                    f"ℹ️ closing download tab index={index}",
                    context=get_context(self),
                )
                self.ui.tabs.setCurrentIndex(index - 1)
                self.ui.tabs.removeTab(index)
                break

        self.acquisition.status_bar.setText(
            self.__translations["DOWNLOADED"] + ": " + filename
        )
        self.acquisition.progress_bar.setValue(100)
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(2000, loop.quit)
        loop.exec()

        self._reset_acquisition_indicators(False)
        debug("ℹ️ download UI indicators reset", context=get_context(self))

    # END DOWNLOAD METHODS

    def __enable_all(self):
        if self.acquisition_status in (
            AcquisitionStatus.UNSTARTED,
            AcquisitionStatus.FINISHED,
        ):
            self.__enable_screenshot_buttons(False)
            self.__enable_navigation_buttons(True)
            self.__enable_right_buttons_container(True)
            self.setEnabled(True)
        elif self.acquisition_status == AcquisitionStatus.STARTED:
            self.__enable_screenshot_buttons(True)
            self.__enable_navigation_buttons(True)
            self.__enable_right_buttons_container(False)
            self.setEnabled(True)
        elif self.acquisition_status == AcquisitionStatus.STOPPED:
            self.__enable_right_buttons_container(False)
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

    def __enable_right_buttons_container(self, enable):
        self.ui.right_buttons_container.setEnabled(enable)

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

        mitm_port = os.environ.get(FIT_MITM_PORT)
        if not mitm_port:
            debug(
                f"❌ {FIT_MITM_PORT} env not set; skipping OS proxy",
                context=get_context(self),
            )
            return False
        debug(
            f"mitm_port env={os.environ.get(FIT_MITM_PORT)} resolved={mitm_port}",
            context=get_context(self),
        )
        try:
            port_value = int(mitm_port)
        except ValueError:
            debug(
                f"❌ Invalid {FIT_MITM_PORT} value: {mitm_port}",
                context=get_context(self),
            )
            return False
        self.proxy_manager.enable_capture_proxy("127.0.0.1", port_value)
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

    def __verify_timestamp(self):
        verify_timestamp = VerifyPDFTimestampView(self.wizard)
        verify_timestamp.show()

    def __verify_pec(self):
        verify_pec = VerifyPecView(self.wizard)
        verify_pec.show()

    def closeEvent(self, event):
        if self.can_close() and self.wizard is None:
            self.mitm_runner.stop_by_pid()
        return super().closeEvent(event)
