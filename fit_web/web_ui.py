#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# -----
# Copyright (c) 2023 FIT-Project
# SPDX-License-Identifier: LGPL-3.0-or-later
# -----
######


from PySide6 import QtCore, QtGui, QtWidgets

from fit_web.lang import load_translations
from fit_common.core.utils import get_version


class Ui_fit_web(object):
    def setupUi(self, fit_web):
        fit_web.setObjectName("fit_web")
        fit_web.setEnabled(True)
        fit_web.resize(800, 600)
        fit_web.setMinimumSize(QtCore.QSize(800, 600))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(252, 1, 7))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(236, 236, 236))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, brush
        )
        brush = QtGui.QBrush(QtGui.QColor(236, 236, 236))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, brush
        )
        fit_web.setPalette(palette)
        self.styleSheet = QtWidgets.QWidget(parent=fit_web)
        self.styleSheet.setStyleSheet(
            "\n"
            "\n"
            "QWidget{\n"
            "    color: rgb(221, 221, 221);\n"
            "    font: 13px;\n"
            "}\n"
            "\n"
            "QMenu {\n"
            "    background-color: rgb(40, 44, 52);\n"
            "    border: 1px solid rgb(44, 49, 58);\n"
            "}\n"
            "\n"
            "\n"
            "QMenu::item {\n"
            "    background-color: transparent;\n"
            "}\n"
            "\n"
            "QMenu::item:selected {\n"
            "    background-color: rgba(255, 255, 255, 0.3);\n"
            "}\n"
            "\n"
            "/* Tooltip */\n"
            "QToolTip {\n"
            "    color: #e06133;\n"
            "    background-color: rgba(33, 37, 43, 180);\n"
            "    border: 1px solid rgb(44, 49, 58);\n"
            "    background-image: none;\n"
            "    background-position: left center;\n"
            "    background-repeat: no-repeat;\n"
            "    border: none;\n"
            "    border-left: 2px solid rgb(224, 97, 51);\n"
            "    text-align: left;\n"
            "    padding-left: 8px;\n"
            "    margin: 0px;\n"
            "}\n"
            "\n"
            "/* Bg App*/\n"
            "#bg_app {    \n"
            "    background-color: rgb(40, 44, 52);\n"
            "    border: 1px solid rgb(44, 49, 58);\n"
            "}\n"
            "\n"
            "/* Title Menu */\n"
            "#title_right_info { font: 13px; }\n"
            "#title_right_info { padding-left: 10px; }\n"
            "\n"
            "/* Content App */\n"
            "#content_top_bg{    \n"
            "    background-color: rgb(33, 37, 43);\n"
            "}\n"
            "#content_bottom{\n"
            "    border-top: 3px solid rgb(44, 49, 58);\n"
            "}\n"
            "\n"
            "/* Top Buttons */\n"
            "#right_buttons_container .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
            "#right_buttons_container .QPushButton:hover { background-color: rgb(44, 49, 57); border-style: solid; border-radius: 4px; }\n"
            "#right_buttons_container .QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }\n"
            "\n"
            "/* Bottom Bar */\n"
            "#bottom_bar { background-color: rgb(44, 49, 58); }\n"
            "#bottom_bar QLabel { font-size: 11px; color: rgb(113, 126, 149); padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }\n"
            "\n"
            "\n"
            "/* ScrollBars */\n"
            "QScrollBar:horizontal {\n"
            "    border: none;\n"
            "    background: rgb(52, 59, 72);\n"
            "    height: 8px;\n"
            "    margin: 0px 21px 0 21px;\n"
            "    border-radius: 0px;\n"
            "}\n"
            "QScrollBar::handle:horizontal {\n"
            "    background: rgb(52, 59, 72);\n"
            "    min-width: 25px;\n"
            "    border-radius: 4px\n"
            "}\n"
            "QScrollBar::add-line:horizontal {\n"
            "    border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "    width: 20px;\n"
            "    border-top-right-radius: 4px;\n"
            "    border-bottom-right-radius: 4px;\n"
            "    subcontrol-position: right;\n"
            "    subcontrol-origin: margin;\n"
            "}\n"
            "QScrollBar::sub-line:horizontal {\n"
            "    border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "    width: 20px;\n"
            "    border-top-left-radius: 4px;\n"
            "    border-bottom-left-radius: 4px;\n"
            "    subcontrol-position: left;\n"
            "    subcontrol-origin: margin;\n"
            "}\n"
            "QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal{\n"
            "     background: none;\n"
            "}\n"
            "QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal{\n"
            "     background: none;\n"
            "}\n"
            " QScrollBar:vertical {\n"
            "    border: none;\n"
            "    background: rgb(52, 59, 72);\n"
            "    width: 8px;\n"
            "    margin: 21px 0 21px 0;\n"
            "    border-radius: 0px;\n"
            " }\n"
            " QScrollBar::handle:vertical {    \n"
            "    background: rgb(52, 59, 72);\n"
            "    min-height: 25px;\n"
            "    border-radius: 4px\n"
            " }\n"
            " QScrollBar::add-line:vertical {\n"
            "     border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "     height: 20px;\n"
            "    border-bottom-left-radius: 4px;\n"
            "    border-bottom-right-radius: 4px;\n"
            "     subcontrol-position: bottom;\n"
            "     subcontrol-origin: margin;\n"
            " }\n"
            " QScrollBar::sub-line:vertical {\n"
            "    border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "     height: 20px;\n"
            "    border-top-left-radius: 4px;\n"
            "    border-top-right-radius: 4px;\n"
            "     subcontrol-position: top;\n"
            "     subcontrol-origin: margin;\n"
            " }\n"
            " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
            "     background: none;\n"
            " }\n"
            "\n"
            " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
            "     background: none;\n"
            " }\n"
            ""
        )
        self.styleSheet.setObjectName("styleSheet")
        self.appMargins = QtWidgets.QVBoxLayout(self.styleSheet)
        self.appMargins.setContentsMargins(10, 10, 10, 10)
        self.appMargins.setSpacing(0)
        self.appMargins.setObjectName("appMargins")
        self.bg_app = QtWidgets.QFrame(parent=self.styleSheet)
        self.bg_app.setStyleSheet("")
        self.bg_app.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.bg_app.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.bg_app.setObjectName("bg_app")
        self.appLayout = QtWidgets.QHBoxLayout(self.bg_app)
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName("appLayout")
        self.content_box = QtWidgets.QFrame(parent=self.bg_app)
        self.content_box.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.content_box.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.content_box.setObjectName("content_box")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.content_box)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.content_top_bg = QtWidgets.QFrame(parent=self.content_box)
        self.content_top_bg.setMinimumSize(QtCore.QSize(0, 50))
        self.content_top_bg.setMaximumSize(QtCore.QSize(16777215, 50))
        self.content_top_bg.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.content_top_bg.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.content_top_bg.setObjectName("content_top_bg")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.content_top_bg)
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.left_box = QtWidgets.QFrame(parent=self.content_top_bg)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.left_box.sizePolicy().hasHeightForWidth())
        self.left_box.setSizePolicy(sizePolicy)
        self.left_box.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.left_box.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.left_box.setObjectName("left_box")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.left_box)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.logo_container = QtWidgets.QFrame(parent=self.left_box)
        self.logo_container.setMinimumSize(QtCore.QSize(60, 0))
        self.logo_container.setMaximumSize(QtCore.QSize(60, 16777215))
        self.logo_container.setObjectName("logo_container")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.logo_container)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.top_logo = QtWidgets.QLabel(parent=self.logo_container)
        self.top_logo.setMinimumSize(QtCore.QSize(42, 42))
        self.top_logo.setMaximumSize(QtCore.QSize(42, 42))
        self.top_logo.setText("")
        self.top_logo.setPixmap(QtGui.QPixmap(":/images/images/logo-42x42.png"))
        self.top_logo.setObjectName("top_logo")
        self.horizontalLayout_8.addWidget(self.top_logo)
        self.horizontalLayout_3.addWidget(self.logo_container)
        self.title_right_info = QtWidgets.QLabel(parent=self.left_box)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.title_right_info.sizePolicy().hasHeightForWidth()
        )
        self.title_right_info.setSizePolicy(sizePolicy)
        self.title_right_info.setMaximumSize(QtCore.QSize(16777215, 45))
        self.title_right_info.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.title_right_info.setObjectName("title_right_info")
        self.horizontalLayout_3.addWidget(self.title_right_info)
        self.horizontalLayout.addWidget(self.left_box)
        self.right_buttons_container = QtWidgets.QFrame(parent=self.content_top_bg)
        self.right_buttons_container.setMinimumSize(QtCore.QSize(0, 28))
        self.right_buttons_container.setStyleSheet("font-size:18px;")
        self.right_buttons_container.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.right_buttons_container.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.right_buttons_container.setObjectName("right_buttons_container")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.right_buttons_container)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.case_button = QtWidgets.QPushButton(parent=self.right_buttons_container)
        self.case_button.setEnabled(True)
        self.case_button.setMinimumSize(QtCore.QSize(28, 28))
        self.case_button.setMaximumSize(QtCore.QSize(28, 28))
        self.case_button.setStyleSheet("QToolTip {font:13px;}")
        self.case_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/icon_case.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/icon_case-disabled.png"),
            QtGui.QIcon.Mode.Disabled,
            QtGui.QIcon.State.On,
        )
        self.case_button.setIcon(icon)
        self.case_button.setIconSize(QtCore.QSize(20, 20))
        self.case_button.setObjectName("case_button")
        self.horizontalLayout_2.addWidget(self.case_button)
        self.line = QtWidgets.QFrame(parent=self.right_buttons_container)
        self.line.setMinimumSize(QtCore.QSize(0, 40))
        self.line.setMaximumSize(QtCore.QSize(16777215, 40))
        self.line.setStyleSheet("background-color: rgb(40, 44, 52);")
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.configuration_button = QtWidgets.QPushButton(
            parent=self.right_buttons_container
        )
        self.configuration_button.setMinimumSize(QtCore.QSize(28, 28))
        self.configuration_button.setMaximumSize(QtCore.QSize(28, 28))
        self.configuration_button.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.configuration_button.setStyleSheet("QToolTip {font:13px;}")
        self.configuration_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/icons/icon_settings.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/icons/icon_settings-disabled.png"),
            QtGui.QIcon.Mode.Disabled,
            QtGui.QIcon.State.On,
        )
        self.configuration_button.setIcon(icon1)
        self.configuration_button.setIconSize(QtCore.QSize(20, 20))
        self.configuration_button.setObjectName("configuration_button")
        self.horizontalLayout_2.addWidget(self.configuration_button)
        self.minimize_button = QtWidgets.QPushButton(
            parent=self.right_buttons_container
        )
        self.minimize_button.setMinimumSize(QtCore.QSize(28, 28))
        self.minimize_button.setMaximumSize(QtCore.QSize(28, 28))
        self.minimize_button.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.minimize_button.setToolTip("")
        self.minimize_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/icons/icon_minimize.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/icons/icon_minimize-disabled.png"),
            QtGui.QIcon.Mode.Disabled,
            QtGui.QIcon.State.On,
        )
        self.minimize_button.setIcon(icon2)
        self.minimize_button.setIconSize(QtCore.QSize(20, 20))
        self.minimize_button.setObjectName("minimize_button")
        self.horizontalLayout_2.addWidget(self.minimize_button)
        self.close_button = QtWidgets.QPushButton(parent=self.right_buttons_container)
        self.close_button.setEnabled(True)
        self.close_button.setMinimumSize(QtCore.QSize(28, 28))
        self.close_button.setMaximumSize(QtCore.QSize(28, 28))
        self.close_button.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.close_button.setToolTip("")
        self.close_button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/icons/icon_close.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/icons/icon_close-disabled.png"),
            QtGui.QIcon.Mode.Disabled,
            QtGui.QIcon.State.On,
        )
        self.close_button.setIcon(icon3)
        self.close_button.setIconSize(QtCore.QSize(20, 20))
        self.close_button.setObjectName("close_button")
        self.horizontalLayout_2.addWidget(self.close_button)
        self.horizontalLayout.addWidget(
            self.right_buttons_container, 0, QtCore.Qt.AlignmentFlag.AlignRight
        )
        self.verticalLayout_2.addWidget(self.content_top_bg)
        self.content_tool_bar = QtWidgets.QFrame(parent=self.content_box)
        self.content_tool_bar.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.content_tool_bar.sizePolicy().hasHeightForWidth()
        )
        self.content_tool_bar.setSizePolicy(sizePolicy)
        self.content_tool_bar.setMinimumSize(QtCore.QSize(0, 50))
        self.content_tool_bar.setMaximumSize(QtCore.QSize(16777215, 50))
        self.content_tool_bar.setStyleSheet(
            "border-top: 2px solid rgb(44, 49, 58);\n"
            "background-color: rgb(33, 37, 43);\n"
            ""
        )
        self.content_tool_bar.setObjectName("content_tool_bar")
        self.content_tool_bar_layout = QtWidgets.QVBoxLayout(self.content_tool_bar)
        self.content_tool_bar_layout.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetMinAndMaxSize
        )
        self.content_tool_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.content_tool_bar_layout.setSpacing(0)
        self.content_tool_bar_layout.setObjectName("content_tool_bar_layout")
        self.toolbar_container = QtWidgets.QFrame(parent=self.content_tool_bar)
        self.toolbar_container.setMinimumSize(QtCore.QSize(0, 50))
        self.toolbar_container.setMaximumSize(QtCore.QSize(16777215, 50))
        self.toolbar_container.setStyleSheet(
            "QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
            "QPushButton:hover { background-color: rgba(255, 255, 255, 0.5); border-style: solid; border-radius: 4px; }\n"
            "QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }"
        )
        self.toolbar_container.setLineWidth(0)
        self.toolbar_container.setObjectName("toolbar_container")
        self.tool_bar_container_layout = QtWidgets.QHBoxLayout(self.toolbar_container)
        self.tool_bar_container_layout.setContentsMargins(0, 0, 0, 0)
        self.tool_bar_container_layout.setSpacing(0)
        self.tool_bar_container_layout.setObjectName("tool_bar_container_layout")
        self.toolbar_left = QtWidgets.QHBoxLayout()
        self.toolbar_left.setContentsMargins(20, -1, 20, -1)
        self.toolbar_left.setSpacing(30)
        self.toolbar_left.setObjectName("toolbar_left")
        self.back_button = QtWidgets.QPushButton(parent=self.toolbar_container)
        self.back_button.setEnabled(True)
        self.back_button.setMinimumSize(QtCore.QSize(25, 25))
        self.back_button.setMaximumSize(QtCore.QSize(25, 25))
        self.back_button.setStyleSheet("")
        self.back_button.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/back.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        icon4.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/back-disabled.png"),
            QtGui.QIcon.Mode.Disabled,
            QtGui.QIcon.State.On,
        )
        self.back_button.setIcon(icon4)
        self.back_button.setIconSize(QtCore.QSize(25, 25))
        self.back_button.setObjectName("back_button")
        self.toolbar_left.addWidget(self.back_button)
        self.forward_button = QtWidgets.QPushButton(parent=self.toolbar_container)
        self.forward_button.setMaximumSize(QtCore.QSize(25, 25))
        self.forward_button.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/forward.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        icon5.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/forward-disabled.png"),
            QtGui.QIcon.Mode.Disabled,
            QtGui.QIcon.State.On,
        )
        self.forward_button.setIcon(icon5)
        self.forward_button.setIconSize(QtCore.QSize(25, 25))
        self.forward_button.setObjectName("forward_button")
        self.toolbar_left.addWidget(self.forward_button)
        self.reload_button = QtWidgets.QPushButton(parent=self.toolbar_container)
        self.reload_button.setEnabled(True)
        self.reload_button.setMinimumSize(QtCore.QSize(25, 25))
        self.reload_button.setMaximumSize(QtCore.QSize(25, 25))
        self.reload_button.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/reload.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        icon6.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/reload-disabled.png"),
            QtGui.QIcon.Mode.Disabled,
            QtGui.QIcon.State.On,
        )
        self.reload_button.setIcon(icon6)
        self.reload_button.setIconSize(QtCore.QSize(25, 25))
        self.reload_button.setObjectName("reload_button")
        self.toolbar_left.addWidget(self.reload_button)
        self.home_button = QtWidgets.QPushButton(parent=self.toolbar_container)
        self.home_button.setEnabled(True)
        self.home_button.setMaximumSize(QtCore.QSize(25, 25))
        self.home_button.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/home.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        icon7.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/home-disabled.png"),
            QtGui.QIcon.Mode.Disabled,
            QtGui.QIcon.State.On,
        )
        self.home_button.setIcon(icon7)
        self.home_button.setIconSize(QtCore.QSize(25, 25))
        self.home_button.setObjectName("home_button")
        self.toolbar_left.addWidget(self.home_button)
        self.tool_bar_container_layout.addLayout(self.toolbar_left)
        self.tool_bar_center = QtWidgets.QHBoxLayout()
        self.tool_bar_center.setContentsMargins(0, -1, -1, -1)
        self.tool_bar_center.setSpacing(20)
        self.tool_bar_center.setObjectName("tool_bar_center")
        self.separator_url_bar_left = QtWidgets.QFrame(parent=self.toolbar_container)
        self.separator_url_bar_left.setMinimumSize(QtCore.QSize(0, 0))
        self.separator_url_bar_left.setMaximumSize(QtCore.QSize(16777215, 40))
        self.separator_url_bar_left.setStyleSheet("background-color: rgb(44, 49, 58);")
        self.separator_url_bar_left.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.separator_url_bar_left.setLineWidth(2)
        self.separator_url_bar_left.setMidLineWidth(0)
        self.separator_url_bar_left.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.separator_url_bar_left.setObjectName("separator_url_bar_left")
        self.tool_bar_center.addWidget(self.separator_url_bar_left)
        self.httpsIcon = QtWidgets.QLabel(parent=self.toolbar_container)
        self.httpsIcon.setMinimumSize(QtCore.QSize(17, 17))
        self.httpsIcon.setMaximumSize(QtCore.QSize(16, 16))
        self.httpsIcon.setLineWidth(0)
        self.httpsIcon.setText("")
        self.httpsIcon.setPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/lock-open.png")
        )
        self.httpsIcon.setScaledContents(False)
        self.httpsIcon.setObjectName("httpsIcon")
        self.tool_bar_center.addWidget(self.httpsIcon)
        self.url_line_edit = QtWidgets.QLineEdit(parent=self.toolbar_container)
        self.url_line_edit.setMinimumSize(QtCore.QSize(0, 30))
        self.url_line_edit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.url_line_edit.setObjectName("url_line_edit")
        self.tool_bar_center.addWidget(self.url_line_edit)
        self.stop_button = QtWidgets.QPushButton(parent=self.toolbar_container)
        self.stop_button.setMaximumSize(QtCore.QSize(25, 25))
        self.stop_button.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/close.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        icon8.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/close-disabled.png"),
            QtGui.QIcon.Mode.Disabled,
            QtGui.QIcon.State.On,
        )
        self.stop_button.setIcon(icon8)
        self.stop_button.setIconSize(QtCore.QSize(25, 25))
        self.stop_button.setObjectName("stop_button")
        self.tool_bar_center.addWidget(self.stop_button)
        self.separator_url_bar_right = QtWidgets.QFrame(parent=self.toolbar_container)
        self.separator_url_bar_right.setMinimumSize(QtCore.QSize(0, 0))
        self.separator_url_bar_right.setMaximumSize(QtCore.QSize(16777215, 40))
        self.separator_url_bar_right.setStyleSheet("background-color: rgb(44, 49, 58);")
        self.separator_url_bar_right.setLineWidth(2)
        self.separator_url_bar_right.setMidLineWidth(0)
        self.separator_url_bar_right.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.separator_url_bar_right.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.separator_url_bar_right.setObjectName("separator_url_bar_right")
        self.tool_bar_center.addWidget(self.separator_url_bar_right)
        self.tool_bar_container_layout.addLayout(self.tool_bar_center)
        self.tool_bar_right = QtWidgets.QHBoxLayout()
        self.tool_bar_right.setContentsMargins(20, -1, 20, -1)
        self.tool_bar_right.setSpacing(30)
        self.tool_bar_right.setObjectName("tool_bar_right")
        self.start_acquisition_button = QtWidgets.QPushButton(
            parent=self.toolbar_container
        )
        self.start_acquisition_button.setEnabled(True)
        self.start_acquisition_button.setMaximumSize(QtCore.QSize(25, 25))
        self.start_acquisition_button.setStatusTip("")
        self.start_acquisition_button.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/start.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        icon9.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/start-disabled.png"),
            QtGui.QIcon.Mode.Disabled,
            QtGui.QIcon.State.On,
        )
        self.start_acquisition_button.setIcon(icon9)
        self.start_acquisition_button.setIconSize(QtCore.QSize(25, 25))
        self.start_acquisition_button.setObjectName("start_acquisition_button")
        self.tool_bar_right.addWidget(self.start_acquisition_button)
        self.stop_acquisition_button = QtWidgets.QPushButton(
            parent=self.toolbar_container
        )
        self.stop_acquisition_button.setEnabled(False)
        self.stop_acquisition_button.setMaximumSize(QtCore.QSize(25, 25))
        self.stop_acquisition_button.setStatusTip("")
        self.stop_acquisition_button.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/stop.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        icon10.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/stop-disabled.png"),
            QtGui.QIcon.Mode.Disabled,
            QtGui.QIcon.State.On,
        )
        self.stop_acquisition_button.setIcon(icon10)
        self.stop_acquisition_button.setIconSize(QtCore.QSize(25, 25))
        self.stop_acquisition_button.setObjectName("stop_acquisition_button")
        self.tool_bar_right.addWidget(self.stop_acquisition_button)
        self.separator_screen_shot = QtWidgets.QFrame(parent=self.toolbar_container)
        self.separator_screen_shot.setMinimumSize(QtCore.QSize(0, 40))
        self.separator_screen_shot.setMaximumSize(QtCore.QSize(16777215, 40))
        self.separator_screen_shot.setStyleSheet("background-color: rgb(44, 49, 58);")
        self.separator_screen_shot.setLineWidth(2)
        self.separator_screen_shot.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.separator_screen_shot.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.separator_screen_shot.setObjectName("separator_screen_shot")
        self.tool_bar_right.addWidget(self.separator_screen_shot)
        self.screenshot_visible_area_button = QtWidgets.QPushButton(
            parent=self.toolbar_container
        )
        self.screenshot_visible_area_button.setEnabled(False)
        self.screenshot_visible_area_button.setMaximumSize(QtCore.QSize(25, 25))
        self.screenshot_visible_area_button.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/camera.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        icon11.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/camera-disabled.png"),
            QtGui.QIcon.Mode.Disabled,
            QtGui.QIcon.State.On,
        )
        self.screenshot_visible_area_button.setIcon(icon11)
        self.screenshot_visible_area_button.setIconSize(QtCore.QSize(25, 25))
        self.screenshot_visible_area_button.setObjectName(
            "screenshot_visible_area_button"
        )
        self.tool_bar_right.addWidget(self.screenshot_visible_area_button)
        self.screenshot_selected_area_button = QtWidgets.QPushButton(
            parent=self.toolbar_container
        )
        self.screenshot_selected_area_button.setEnabled(False)
        self.screenshot_selected_area_button.setMaximumSize(QtCore.QSize(25, 25))
        self.screenshot_selected_area_button.setStatusTip("")
        self.screenshot_selected_area_button.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/select.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        icon12.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/select-disabled.png"),
            QtGui.QIcon.Mode.Disabled,
            QtGui.QIcon.State.On,
        )
        self.screenshot_selected_area_button.setIcon(icon12)
        self.screenshot_selected_area_button.setIconSize(QtCore.QSize(25, 25))
        self.screenshot_selected_area_button.setObjectName(
            "screenshot_selected_area_button"
        )
        self.tool_bar_right.addWidget(self.screenshot_selected_area_button)
        self.screenshot_full_page_button = QtWidgets.QPushButton(
            parent=self.toolbar_container
        )
        self.screenshot_full_page_button.setEnabled(False)
        self.screenshot_full_page_button.setMinimumSize(QtCore.QSize(25, 25))
        self.screenshot_full_page_button.setMaximumSize(QtCore.QSize(25, 25))
        self.screenshot_full_page_button.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/scroll.png"),
            QtGui.QIcon.Mode.Normal,
            QtGui.QIcon.State.On,
        )
        icon13.addPixmap(
            QtGui.QPixmap(":/images/toolbar/images/toolbar/scroll-disabled.png"),
            QtGui.QIcon.Mode.Disabled,
            QtGui.QIcon.State.On,
        )
        self.screenshot_full_page_button.setIcon(icon13)
        self.screenshot_full_page_button.setIconSize(QtCore.QSize(25, 25))
        self.screenshot_full_page_button.setObjectName("screenshot_full_page_button")
        self.tool_bar_right.addWidget(self.screenshot_full_page_button)
        self.tool_bar_container_layout.addLayout(self.tool_bar_right)
        self.content_tool_bar_layout.addWidget(self.toolbar_container)
        self.verticalLayout_2.addWidget(self.content_tool_bar)
        self.content_bottom = QtWidgets.QFrame(parent=self.content_box)
        self.content_bottom.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.content_bottom.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.content_bottom.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.content_bottom.setObjectName("content_bottom")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.content_bottom)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.content = QtWidgets.QFrame(parent=self.content_bottom)
        self.content.setEnabled(True)
        self.content.setStyleSheet("")
        self.content.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.content.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.content.setObjectName("content")
        self.contentTabsLayout = QtWidgets.QHBoxLayout(self.content)
        self.contentTabsLayout.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetNoConstraint
        )
        self.contentTabsLayout.setContentsMargins(0, 0, 0, 0)
        self.contentTabsLayout.setSpacing(0)
        self.contentTabsLayout.setObjectName("contentTabsLayout")
        self.tabs = QtWidgets.QTabWidget(parent=self.content)
        self.tabs.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tabs.setAutoFillBackground(False)
        self.tabs.setStyleSheet(
            "\n"
            "QTabWidget::tab-bar {alignment: left; background: #0B6C87; color:#ffffff;}\n"
            "QTabBar::tab {\n"
            "    background: rgb(33, 37, 43);\n"
            "    border: 2px solid rgb(33, 37, 43);\n"
            "    border-top-left-radius: 4px;\n"
            "    border-top-right-radius: 4px;\n"
            "    min-width: 8ex;\n"
            "    padding: 4px;\n"
            "}\n"
            "\n"
            "QTabBar::tab:selected, QTabBar::tab:hover {\n"
            "    background: rgb(44, 49, 58);\n"
            "}\n"
            "\n"
            "QTabBar::tab:selected {\n"
            "    border-color: rgb(44, 49, 58);\n"
            "}\n"
            "\n"
            "QTabBar::tab:!selected {\n"
            "    margin-top: 2px; /* make non-selected tabs look smaller */\n"
            "}"
        )
        self.tabs.setTabPosition(QtWidgets.QTabWidget.TabPosition.North)
        self.tabs.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.tabs.setElideMode(QtCore.Qt.TextElideMode.ElideLeft)
        self.tabs.setDocumentMode(False)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(False)
        self.tabs.setTabBarAutoHide(True)
        self.tabs.setObjectName("tabs")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabs.addTab(self.tab, "")
        self.contentTabsLayout.addWidget(self.tabs)
        self.verticalLayout_6.addWidget(self.content)
        self.bottom_bar = QtWidgets.QFrame(parent=self.content_bottom)
        self.bottom_bar.setMinimumSize(QtCore.QSize(0, 42))
        self.bottom_bar.setMaximumSize(QtCore.QSize(16777215, 42))
        self.bottom_bar.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.bottom_bar.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.bottom_bar.setObjectName("bottom_bar")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.bottom_bar)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.credits_label = QtWidgets.QLabel(parent=self.bottom_bar)
        self.credits_label.setMaximumSize(QtCore.QSize(120, 16))
        self.credits_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading
            | QtCore.Qt.AlignmentFlag.AlignLeft
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.credits_label.setObjectName("credits_label")
        self.horizontalLayout_5.addWidget(self.credits_label)
        spacerItem = QtWidgets.QSpacerItem(
            20,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout_5.addItem(spacerItem)
        self.progress_bar = QtWidgets.QProgressBar(parent=self.bottom_bar)
        self.progress_bar.setMinimumSize(QtCore.QSize(200, 0))
        self.progress_bar.setMaximumSize(QtCore.QSize(200, 20))
        self.progress_bar.setStyleSheet(
            "QProgressBar\n"
            "{\n"
            "    color: #ffffff;\n"
            "    border-style: outset;\n"
            "border-width: 2px;\n"
            "    border-radius: 5px;\n"
            "    text-align: left;\n"
            "}\n"
            "QProgressBar::chunk\n"
            "{\n"
            "    background-color:#e06133;\n"
            "}"
        )
        self.progress_bar.setProperty("value", 24)
        self.progress_bar.setObjectName("progress_bar")
        self.horizontalLayout_5.addWidget(self.progress_bar)
        spacerItem1 = QtWidgets.QSpacerItem(
            20,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout_5.addItem(spacerItem1)
        self.status_message = QtWidgets.QLabel(parent=self.bottom_bar)
        self.status_message.setMinimumSize(QtCore.QSize(300, 0))
        self.status_message.setStyleSheet("font-size:14px;\n" "color:#ffffff;")
        self.status_message.setObjectName("status_message")
        self.horizontalLayout_5.addWidget(self.status_message)
        spacerItem2 = QtWidgets.QSpacerItem(
            20,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout_5.addItem(spacerItem2)
        self.version = QtWidgets.QLabel(parent=self.bottom_bar)
        self.version.setMaximumSize(QtCore.QSize(120, 16777215))
        self.version.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight
            | QtCore.Qt.AlignmentFlag.AlignTrailing
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.version.setObjectName("version")
        self.horizontalLayout_5.addWidget(self.version)
        self.frame_size_grip = QtWidgets.QFrame(parent=self.bottom_bar)
        self.frame_size_grip.setMinimumSize(QtCore.QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QtCore.QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_size_grip.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_size_grip.setObjectName("frame_size_grip")
        self.horizontalLayout_5.addWidget(self.frame_size_grip)
        self.verticalLayout_6.addWidget(self.bottom_bar)
        self.verticalLayout_2.addWidget(self.content_bottom)
        self.appLayout.addWidget(self.content_box)
        self.appMargins.addWidget(self.bg_app)
        fit_web.setCentralWidget(self.styleSheet)

        self.retranslateUi(fit_web)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(fit_web)

    def retranslateUi(self, fit_web):
        _translate = QtCore.QCoreApplication.translate
        fit_web.setWindowTitle(_translate("fit_web", "FIT Web Scraper"))
        self.title_right_info.setText(_translate("fit_web", "Web Scraper"))
        self.case_button.setToolTip(_translate("fit_web", "Case info"))
        self.configuration_button.setToolTip(_translate("fit_web", "Configuration"))
        self.back_button.setToolTip(_translate("fit_web", "Back to previous page"))
        self.forward_button.setToolTip(_translate("fit_web", "Forward to next page"))
        self.reload_button.setToolTip(_translate("fit_web", "Reload page"))
        self.home_button.setToolTip(_translate("fit_web", "Go home"))
        self.stop_button.setToolTip(_translate("fit_web", "Stop loading current page"))
        self.start_acquisition_button.setToolTip(
            _translate("fit_web", "Start acquisition")
        )
        self.stop_acquisition_button.setToolTip(
            _translate("fit_web", "Stop acquisition")
        )
        self.screenshot_visible_area_button.setToolTip(
            _translate("fit_web", "Take a screenshot on view area")
        )
        self.screenshot_selected_area_button.setToolTip(
            _translate("fit_web", "Take a screenshot on the selected area")
        )
        self.screenshot_full_page_button.setToolTip(
            _translate("fit_web", "Take a full page screenshot")
        )
        self.tabs.setTabText(self.tabs.indexOf(self.tab), _translate("fit_web", "Tab1"))
        self.credits_label.setText(_translate("fit_web", "By: fit-project.org"))
        self.status_message.setText(_translate("fit_web", "status message"))
        self.version.setText(_translate("fit_web", "v1.0.3"))
