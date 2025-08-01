#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: GPL-3.0-only
# -----
######

import time

from fit_common.core import debug, get_context, get_platform, log_exception
from PIL import ImageGrab
from PySide6 import QtCore, QtGui, QtWidgets


# Refer to https://github.com/harupy/snipping-tool
class SnippingWidget(QtWidgets.QWidget):
    is_snipping = False

    def __init__(self, filename, parent=None):
        super(SnippingWidget, self).__init__()
        self.parent = parent
        self.setWindowFlags(
            QtCore.Qt.WindowType.WindowStaysOnTopHint
            | QtCore.Qt.WindowType.FramelessWindowHint
        )

        self.setGeometry(
            0, 0, self.screen().size().width(), self.screen().size().height()
        )
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.onSnippingCompleted = None
        self.scale_factor = self.screen().devicePixelRatio()
        self.filename = filename

    def start(self):
        SnippingWidget.is_snipping = True
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor)
        )
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        if SnippingWidget.is_snipping:
            brush_color = (128, 128, 255, 100)
            lw = 3
            opacity = 0.3
            qp.setPen(QtGui.QPen(QtGui.QColor("red"), lw))
        else:
            brush_color = (0, 0, 0, 0)
            lw = 3
            opacity = 0.1
            qp.setPen(QtGui.QPen(QtGui.QColor("green"), lw))

        self.setWindowOpacity(opacity)
        qp.setBrush(QtGui.QColor(*brush_color))
        rect = QtCore.QRectF(
            self.begin.x(),
            self.begin.y(),
            abs(self.end.x() - self.begin.x()),
            abs(self.end.y() - self.begin.y()),
        )
        qp.drawRect(rect)

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        SnippingWidget.is_snipping = False
        QtWidgets.QApplication.restoreOverrideCursor()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        print(x1, y1, x2, y2)

        x1, y1, x2, y2 = self.apply_scaling_factor(x1, y1, x2, y2)

        self.repaint()
        QtWidgets.QApplication.processEvents()

        img = None

        if x2 - x1 > 1 and y2 - y1 > 1:
            try:

                if get_platform() == "macos":
                    screen = self.screen()
                    pixmap = screen.grabWindow(0)

                    rect = QtCore.QRect(x1, y1, x2 - x1, y2 - y1)
                    cropped = pixmap.copy(rect)

                    cropped.save(self.filename, "PNG")

                else:
                    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            except Exception as e:
                debug(
                    "Screenshot failed",
                    str(e),
                    context=get_context(self),
                )
                log_exception(e, context=get_context(self))
        else:
            debug(
                "Invalid rectangle selected, skipping screenshot",
                context=get_context(self),
            )

        if self.onSnippingCompleted is not None:
            self.onSnippingCompleted(img)

        self.close()

    def apply_scaling_factor(self, x1, y1, x2, y2):
        x1 *= self.scale_factor
        y1 *= self.scale_factor
        x2 *= self.scale_factor
        y2 *= self.scale_factor
        return int(x1), int(y1), int(x2), int(y2)


class SelectAreaScreenshot(QtCore.QObject):
    finished = QtCore.Signal()  # give worker class a finished signal

    def __init__(self, filename, parent=None):
        super(
            SelectAreaScreenshot,
            self,
        ).__init__(parent=parent)
        self.filename = filename
        self.snippingWidget = SnippingWidget(filename=filename, parent=parent)
        self.snippingWidget.onSnippingCompleted = self.__on_snipping_completed

    def __on_snipping_completed(self, frame):
        if frame is None:
            self.__finished()
            return

        try:
            time.sleep(1)
            frame.save(self.filename)
        except Exception as e:
            debug(
                "Failed to save screenshot",
                str(e),
                context=get_context(self),
            )
            log_exception(e, context=get_context(self))

        self.__finished()

    def snip_area(self):
        self.snippingWidget.start()

    def __finished(self):
        self.finished.emit()
        self.deleteLater()
