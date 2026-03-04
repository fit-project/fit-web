import json

from PySide6 import QtCore, QtGui, QtWidgets


class FindBar(QtWidgets.QFrame):
    def __init__(
        self,
        parent: QtWidgets.QWidget,
        shortcut_owner: QtWidgets.QWidget,
        tabs: QtWidgets.QTabWidget,
    ) -> None:
        super().__init__(parent)
        self.__tabs = tabs
        self.__find_query = ""
        self.__find_total = 0
        self.__find_index = 0

        self.setObjectName("find_bar")
        self.__init_ui()
        self.__init_shortcuts(shortcut_owner)
        parent.installEventFilter(self)
        self.hide()
        self.position_bar()

    def eventFilter(self, watched, event):
        if (
            watched == self.parentWidget()
            and event.type() == QtCore.QEvent.Type.Resize
        ):
            self.position_bar()
        return super().eventFilter(watched, event)

    def __init_ui(self) -> None:
        self.setFixedHeight(44)
        self.setStyleSheet(
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

        bar_layout = QtWidgets.QHBoxLayout(self)
        bar_layout.setContentsMargins(10, 6, 10, 6)
        bar_layout.setSpacing(4)

        self.__find_input = QtWidgets.QLineEdit(self)
        self.__find_input.setObjectName("find_input")
        self.__find_input.setPlaceholderText("Find in page")
        self.__find_input.textChanged.connect(self.__on_find_text_changed)
        self.__find_input.returnPressed.connect(self.__on_find_return_pressed)

        self.__find_counter = QtWidgets.QLabel("0/0", self)
        self.__find_counter.setObjectName("find_counter")
        self.__find_counter.setMinimumWidth(56)
        self.__find_counter.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter
        )

        self.__find_prev_button = QtWidgets.QPushButton("^", self)
        self.__find_prev_button.setObjectName("find_prev")
        self.__find_prev_button.clicked.connect(self.find_previous)

        self.__find_next_button = QtWidgets.QPushButton("v", self)
        self.__find_next_button.setObjectName("find_next")
        self.__find_next_button.clicked.connect(self.find_next)

        self.__find_close_button = QtWidgets.QPushButton("X", self)
        self.__find_close_button.setObjectName("find_close")
        self.__find_close_button.clicked.connect(self.hide_bar)

        separator_left = QtWidgets.QFrame(self)
        separator_left.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        separator_left.setStyleSheet("color: rgb(200, 200, 200);")
        separator_right = QtWidgets.QFrame(self)
        separator_right.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        separator_right.setStyleSheet("color: rgb(200, 200, 200);")

        bar_layout.addWidget(self.__find_input, 1)
        bar_layout.addWidget(separator_left, 0)
        bar_layout.addWidget(self.__find_counter, 0)
        bar_layout.addWidget(self.__find_prev_button, 0)
        bar_layout.addWidget(self.__find_next_button, 0)
        bar_layout.addWidget(separator_right, 0)
        bar_layout.addWidget(self.__find_close_button, 0)

        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 4)
        shadow.setColor(QtGui.QColor(0, 0, 0, 70))
        self.setGraphicsEffect(shadow)

    def __init_shortcuts(self, shortcut_owner: QtWidgets.QWidget) -> None:
        self.__find_shortcut = QtGui.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.Find), shortcut_owner
        )
        self.__find_shortcut.setContext(QtCore.Qt.ShortcutContext.ApplicationShortcut)
        self.__find_shortcut.activated.connect(self.show_bar)

        self.__find_next_shortcut = QtGui.QShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.FindNext), shortcut_owner
        )
        self.__find_next_shortcut.setContext(
            QtCore.Qt.ShortcutContext.ApplicationShortcut
        )
        self.__find_next_shortcut.activated.connect(self.find_next)

        self.__find_prev_shortcut = QtGui.QShortcut(
            QtGui.QKeySequence(
                QtGui.QKeySequence.StandardKey.FindPrevious
            ),
            shortcut_owner,
        )
        self.__find_prev_shortcut.setContext(
            QtCore.Qt.ShortcutContext.ApplicationShortcut
        )
        self.__find_prev_shortcut.activated.connect(self.find_previous)

        self.__find_close_shortcut = QtGui.QShortcut(
            QtGui.QKeySequence(QtCore.Qt.Key.Key_Escape), shortcut_owner
        )
        self.__find_close_shortcut.setContext(
            QtCore.Qt.ShortcutContext.ApplicationShortcut
        )
        self.__find_close_shortcut.activated.connect(self.hide_bar)

    def position_bar(self) -> None:
        parent = self.parentWidget()
        if not parent:
            return
        width = min(max(parent.width() - 40, 420), 620)
        self.setFixedWidth(width)
        x = max(0, (parent.width() - width) // 2)
        y = 10
        self.move(x, y)
        self.raise_()

    def show_bar(self) -> None:
        self.show()
        self.position_bar()
        self.__find_input.setFocus()
        self.__find_input.selectAll()

    def hide_bar(self) -> None:
        self.hide()
        current = self.__tabs.currentWidget()
        if current and hasattr(current, "setFocus"):
            current.setFocus()

    def refresh_for_current_tab(self, _index: int) -> None:
        if not self.isVisible():
            return
        self.__run_find(reset=True, forward=True)

    def __on_find_text_changed(self, _text: str) -> None:
        self.__run_find(reset=True, forward=True)

    def __on_find_return_pressed(self) -> None:
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers & QtCore.Qt.KeyboardModifier.ShiftModifier:
            self.find_previous()
        else:
            self.find_next()

    @staticmethod
    def __js_quote(value: str) -> str:
        escaped = value.replace("\\", "\\\\")
        escaped = escaped.replace("'", "\\'")
        escaped = escaped.replace("\n", "\\n").replace("\r", "\\r")
        return escaped

    def __request_js_result(self, widget, script: str, callback) -> None:
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

    def __set_find_counter(self, index: int, total: int) -> None:
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

    def find_previous(self) -> None:
        self.__run_find(reset=False, forward=False)

    def find_next(self) -> None:
        self.__run_find(reset=False, forward=True)

    def __run_find(self, reset: bool, forward: bool) -> None:
        current = self.__tabs.currentWidget()
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
