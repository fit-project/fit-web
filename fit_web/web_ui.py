# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'web.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtGui import QBrush, QColor, QCursor, QIcon, QPalette, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class Ui_fit_web(object):
    def setupUi(self, fit_web):
        if not fit_web.objectName():
            fit_web.setObjectName("fit_web")
        fit_web.setEnabled(True)
        fit_web.resize(800, 600)
        fit_web.setMinimumSize(QSize(800, 600))
        palette = QPalette()
        brush = QBrush(QColor(252, 1, 7, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush)
        brush1 = QBrush(QColor(236, 236, 236, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1
        )
        palette.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush1
        )
        fit_web.setPalette(palette)
        self.styleSheet = QWidget(fit_web)
        self.styleSheet.setObjectName("styleSheet")
        self.styleSheet.setStyleSheet(
            "\n"
            "\n"
            "QWidget{\n"
            "	color: rgb(221, 221, 221);\n"
            "	font: 13px;\n"
            "}\n"
            "\n"
            "QMenu {\n"
            "    background-color: rgb(40, 44, 52);\n"
            "	border: 1px solid rgb(44, 49, 58);\n"
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
            "	color: #e06133;\n"
            "	background-color: rgba(33, 37, 43, 180);\n"
            "	border: 1px solid rgb(44, 49, 58);\n"
            "	background-image: none;\n"
            "	background-position: left center;\n"
            "    background-repeat: no-repeat;\n"
            "	border: none;\n"
            "	border-left: 2px solid rgb(224, 97, 51);\n"
            "	text-align: left;\n"
            "	padding-left: 8px;\n"
            "	margin: 0px;\n"
            "}\n"
            "\n"
            "/* Bg App*/\n"
            "#bg_app {	\n"
            "	background-color: rgb(40, 44, 52);\n"
            "	border: 1px solid rgb(44, 49, 58);\n"
            "}\n"
            "\n"
            "/* Title Menu */\n"
            "#title_right_info { font: 13px; }\n"
            "#title_right_info { padding-left: 10px; }\n"
            "\n"
            "/* Content App */\n"
            "#content_top_bg{	\n"
            "	backgroun"
            "d-color: rgb(33, 37, 43);\n"
            "}\n"
            "#content_bottom{\n"
            "	border-top: 3px solid rgb(44, 49, 58);\n"
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
            "	border-radius: 0px;\n"
            "}\n"
            "QScrollBar::handle:horizontal {\n"
            "    background: rgb(52, 59, 72);\n"
            "    min-width: 25px;"
            "\n"
            "	border-radius: 4px\n"
            "}\n"
            "QScrollBar::add-line:horizontal {\n"
            "    border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "    width: 20px;\n"
            "	border-top-right-radius: 4px;\n"
            "    border-bottom-right-radius: 4px;\n"
            "    subcontrol-position: right;\n"
            "    subcontrol-origin: margin;\n"
            "}\n"
            "QScrollBar::sub-line:horizontal {\n"
            "    border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "    width: 20px;\n"
            "	border-top-left-radius: 4px;\n"
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
            "	border: none;\n"
            "    background: rgb(52, 59, 72);\n"
            "    width: 8px;\n"
            "    margin: 21px 0 21px 0;\n"
            "	border-radius: 0px;\n"
            " }\n"
            " QScrollBar::handle:vertical {	\n"
            "	background: rgb(52, 59, 72);\n"
            "    min"
            "-height: 25px;\n"
            "	border-radius: 4px\n"
            " }\n"
            " QScrollBar::add-line:vertical {\n"
            "     border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "     height: 20px;\n"
            "	border-bottom-left-radius: 4px;\n"
            "    border-bottom-right-radius: 4px;\n"
            "     subcontrol-position: bottom;\n"
            "     subcontrol-origin: margin;\n"
            " }\n"
            " QScrollBar::sub-line:vertical {\n"
            "	border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "     height: 20px;\n"
            "	border-top-left-radius: 4px;\n"
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
        self.appMargins = QVBoxLayout(self.styleSheet)
        self.appMargins.setSpacing(0)
        self.appMargins.setObjectName("appMargins")
        self.appMargins.setContentsMargins(10, 10, 10, 10)
        self.bg_app = QFrame(self.styleSheet)
        self.bg_app.setObjectName("bg_app")
        self.bg_app.setStyleSheet("")
        self.bg_app.setFrameShape(QFrame.NoFrame)
        self.bg_app.setFrameShadow(QFrame.Raised)
        self.appLayout = QHBoxLayout(self.bg_app)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName("appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.content_box = QFrame(self.bg_app)
        self.content_box.setObjectName("content_box")
        self.content_box.setFrameShape(QFrame.NoFrame)
        self.content_box.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.content_box)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.content_top_bg = QFrame(self.content_box)
        self.content_top_bg.setObjectName("content_top_bg")
        self.content_top_bg.setMinimumSize(QSize(0, 50))
        self.content_top_bg.setMaximumSize(QSize(16777215, 50))
        self.content_top_bg.setFrameShape(QFrame.NoFrame)
        self.content_top_bg.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.content_top_bg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.left_box = QFrame(self.content_top_bg)
        self.left_box.setObjectName("left_box")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.left_box.sizePolicy().hasHeightForWidth())
        self.left_box.setSizePolicy(sizePolicy)
        self.left_box.setFrameShape(QFrame.NoFrame)
        self.left_box.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.left_box)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.logo_container = QFrame(self.left_box)
        self.logo_container.setObjectName("logo_container")
        self.logo_container.setMinimumSize(QSize(60, 0))
        self.logo_container.setMaximumSize(QSize(60, 16777215))
        self.horizontalLayout_8 = QHBoxLayout(self.logo_container)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.top_logo = QLabel(self.logo_container)
        self.top_logo.setObjectName("top_logo")
        self.top_logo.setMinimumSize(QSize(42, 42))
        self.top_logo.setMaximumSize(QSize(42, 42))
        self.top_logo.setPixmap(QPixmap(":/images/images/logo-42x42.png"))

        self.horizontalLayout_8.addWidget(self.top_logo)

        self.horizontalLayout_3.addWidget(self.logo_container)

        self.title_right_info = QLabel(self.left_box)
        self.title_right_info.setObjectName("title_right_info")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.title_right_info.sizePolicy().hasHeightForWidth()
        )
        self.title_right_info.setSizePolicy(sizePolicy1)
        self.title_right_info.setMaximumSize(QSize(16777215, 45))
        self.title_right_info.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )

        self.horizontalLayout_3.addWidget(self.title_right_info)

        self.horizontalLayout.addWidget(self.left_box)

        self.right_buttons_container = QFrame(self.content_top_bg)
        self.right_buttons_container.setObjectName("right_buttons_container")
        self.right_buttons_container.setMinimumSize(QSize(0, 28))
        self.right_buttons_container.setStyleSheet("font-size:18px;")
        self.right_buttons_container.setFrameShape(QFrame.NoFrame)
        self.right_buttons_container.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.right_buttons_container)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verify_timestamp_button = QPushButton(self.right_buttons_container)
        self.verify_timestamp_button.setObjectName("verify_timestamp_button")
        self.verify_timestamp_button.setMinimumSize(QSize(28, 28))
        self.verify_timestamp_button.setMaximumSize(QSize(28, 28))
        self.verify_timestamp_button.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor)
        )
        self.verify_timestamp_button.setStyleSheet("QToolTip {font:13px;}")
        icon = QIcon()
        icon.addFile(
            ":/images/wizard/images/wizard/verify_timestamp-disabled.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.verify_timestamp_button.setIcon(icon)
        self.verify_timestamp_button.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.verify_timestamp_button)

        self.verify_pec_button = QPushButton(self.right_buttons_container)
        self.verify_pec_button.setObjectName("verify_pec_button")
        self.verify_pec_button.setMinimumSize(QSize(28, 28))
        self.verify_pec_button.setMaximumSize(QSize(28, 28))
        self.verify_pec_button.setStyleSheet("QToolTip {font:13px;}")
        icon1 = QIcon()
        icon1.addFile(
            ":/images/wizard/images/wizard/verify_pec-disabled.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.verify_pec_button.setIcon(icon1)
        self.verify_pec_button.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.verify_pec_button)

        self.case_button = QPushButton(self.right_buttons_container)
        self.case_button.setObjectName("case_button")
        self.case_button.setEnabled(True)
        self.case_button.setMinimumSize(QSize(28, 28))
        self.case_button.setMaximumSize(QSize(28, 28))
        self.case_button.setStyleSheet("QToolTip {font:13px;}")
        icon2 = QIcon()
        icon2.addFile(
            ":/icons/icons/icon_case.png", QSize(), QIcon.Mode.Normal, QIcon.State.On
        )
        icon2.addFile(
            ":/icons/icons/icon_case-disabled.png",
            QSize(),
            QIcon.Mode.Disabled,
            QIcon.State.On,
        )
        self.case_button.setIcon(icon2)
        self.case_button.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.case_button)

        self.line = QFrame(self.right_buttons_container)
        self.line.setObjectName("line")
        self.line.setMinimumSize(QSize(0, 40))
        self.line.setMaximumSize(QSize(16777215, 40))
        self.line.setStyleSheet("background-color: rgb(40, 44, 52);")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_2.addWidget(self.line)

        self.configuration_button = QPushButton(self.right_buttons_container)
        self.configuration_button.setObjectName("configuration_button")
        self.configuration_button.setMinimumSize(QSize(28, 28))
        self.configuration_button.setMaximumSize(QSize(28, 28))
        self.configuration_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.configuration_button.setStyleSheet("QToolTip {font:13px;}")
        icon3 = QIcon()
        icon3.addFile(
            ":/icons/icons/icon_settings.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.On,
        )
        icon3.addFile(
            ":/icons/icons/icon_settings-disabled.png",
            QSize(),
            QIcon.Mode.Disabled,
            QIcon.State.On,
        )
        self.configuration_button.setIcon(icon3)
        self.configuration_button.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.configuration_button)

        self.minimize_button = QPushButton(self.right_buttons_container)
        self.minimize_button.setObjectName("minimize_button")
        self.minimize_button.setMinimumSize(QSize(28, 28))
        self.minimize_button.setMaximumSize(QSize(28, 28))
        self.minimize_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon4 = QIcon()
        icon4.addFile(
            ":/icons/icons/icon_minimize.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.On,
        )
        icon4.addFile(
            ":/icons/icons/icon_minimize-disabled.png",
            QSize(),
            QIcon.Mode.Disabled,
            QIcon.State.On,
        )
        self.minimize_button.setIcon(icon4)
        self.minimize_button.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.minimize_button)

        self.close_button = QPushButton(self.right_buttons_container)
        self.close_button.setObjectName("close_button")
        self.close_button.setEnabled(True)
        self.close_button.setMinimumSize(QSize(28, 28))
        self.close_button.setMaximumSize(QSize(28, 28))
        self.close_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon5 = QIcon()
        icon5.addFile(
            ":/icons/icons/icon_close.png", QSize(), QIcon.Mode.Normal, QIcon.State.On
        )
        icon5.addFile(
            ":/icons/icons/icon_close-disabled.png",
            QSize(),
            QIcon.Mode.Disabled,
            QIcon.State.On,
        )
        self.close_button.setIcon(icon5)
        self.close_button.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.close_button)

        self.horizontalLayout.addWidget(self.right_buttons_container, 0, Qt.AlignRight)

        self.verticalLayout_2.addWidget(self.content_top_bg)

        self.content_tool_bar = QFrame(self.content_box)
        self.content_tool_bar.setObjectName("content_tool_bar")
        self.content_tool_bar.setEnabled(True)
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.content_tool_bar.sizePolicy().hasHeightForWidth()
        )
        self.content_tool_bar.setSizePolicy(sizePolicy2)
        self.content_tool_bar.setMinimumSize(QSize(0, 50))
        self.content_tool_bar.setMaximumSize(QSize(16777215, 50))
        self.content_tool_bar.setStyleSheet(
            "border-top: 2px solid rgb(44, 49, 58);\n"
            "background-color: rgb(33, 37, 43);\n"
            ""
        )
        self.content_tool_bar_layout = QVBoxLayout(self.content_tool_bar)
        self.content_tool_bar_layout.setSpacing(0)
        self.content_tool_bar_layout.setObjectName("content_tool_bar_layout")
        self.content_tool_bar_layout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.content_tool_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.toolbar_container = QFrame(self.content_tool_bar)
        self.toolbar_container.setObjectName("toolbar_container")
        self.toolbar_container.setMinimumSize(QSize(0, 50))
        self.toolbar_container.setMaximumSize(QSize(16777215, 50))
        self.toolbar_container.setStyleSheet(
            "QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
            "QPushButton:hover { background-color: rgba(255, 255, 255, 0.5); border-style: solid; border-radius: 4px; }\n"
            "QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }"
        )
        self.toolbar_container.setLineWidth(0)
        self.tool_bar_container_layout = QHBoxLayout(self.toolbar_container)
        self.tool_bar_container_layout.setSpacing(0)
        self.tool_bar_container_layout.setObjectName("tool_bar_container_layout")
        self.tool_bar_container_layout.setContentsMargins(0, 0, 0, 0)
        self.toolbar_left = QHBoxLayout()
        self.toolbar_left.setSpacing(30)
        self.toolbar_left.setObjectName("toolbar_left")
        self.toolbar_left.setContentsMargins(20, -1, 20, -1)
        self.back_button = QPushButton(self.toolbar_container)
        self.back_button.setObjectName("back_button")
        self.back_button.setEnabled(True)
        self.back_button.setMinimumSize(QSize(25, 25))
        self.back_button.setMaximumSize(QSize(25, 25))
        self.back_button.setStyleSheet("")
        icon6 = QIcon()
        icon6.addFile(
            ":/images/toolbar/images/toolbar/back.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.On,
        )
        icon6.addFile(
            ":/images/toolbar/images/toolbar/back-disabled.png",
            QSize(),
            QIcon.Mode.Disabled,
            QIcon.State.On,
        )
        self.back_button.setIcon(icon6)
        self.back_button.setIconSize(QSize(25, 25))

        self.toolbar_left.addWidget(self.back_button)

        self.forward_button = QPushButton(self.toolbar_container)
        self.forward_button.setObjectName("forward_button")
        self.forward_button.setMaximumSize(QSize(25, 25))
        icon7 = QIcon()
        icon7.addFile(
            ":/images/toolbar/images/toolbar/forward.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.On,
        )
        icon7.addFile(
            ":/images/toolbar/images/toolbar/forward-disabled.png",
            QSize(),
            QIcon.Mode.Disabled,
            QIcon.State.On,
        )
        self.forward_button.setIcon(icon7)
        self.forward_button.setIconSize(QSize(25, 25))

        self.toolbar_left.addWidget(self.forward_button)

        self.reload_button = QPushButton(self.toolbar_container)
        self.reload_button.setObjectName("reload_button")
        self.reload_button.setEnabled(True)
        self.reload_button.setMinimumSize(QSize(25, 25))
        self.reload_button.setMaximumSize(QSize(25, 25))
        icon8 = QIcon()
        icon8.addFile(
            ":/images/toolbar/images/toolbar/reload.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.On,
        )
        icon8.addFile(
            ":/images/toolbar/images/toolbar/reload-disabled.png",
            QSize(),
            QIcon.Mode.Disabled,
            QIcon.State.On,
        )
        self.reload_button.setIcon(icon8)
        self.reload_button.setIconSize(QSize(25, 25))

        self.toolbar_left.addWidget(self.reload_button)

        self.home_button = QPushButton(self.toolbar_container)
        self.home_button.setObjectName("home_button")
        self.home_button.setEnabled(True)
        self.home_button.setMaximumSize(QSize(25, 25))
        icon9 = QIcon()
        icon9.addFile(
            ":/images/toolbar/images/toolbar/home.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.On,
        )
        icon9.addFile(
            ":/images/toolbar/images/toolbar/home-disabled.png",
            QSize(),
            QIcon.Mode.Disabled,
            QIcon.State.On,
        )
        self.home_button.setIcon(icon9)
        self.home_button.setIconSize(QSize(25, 25))

        self.toolbar_left.addWidget(self.home_button)

        self.tool_bar_container_layout.addLayout(self.toolbar_left)

        self.tool_bar_center = QHBoxLayout()
        self.tool_bar_center.setSpacing(20)
        self.tool_bar_center.setObjectName("tool_bar_center")
        self.tool_bar_center.setContentsMargins(0, -1, -1, -1)
        self.separator_url_bar_left = QFrame(self.toolbar_container)
        self.separator_url_bar_left.setObjectName("separator_url_bar_left")
        self.separator_url_bar_left.setMinimumSize(QSize(0, 0))
        self.separator_url_bar_left.setMaximumSize(QSize(16777215, 40))
        self.separator_url_bar_left.setStyleSheet("background-color: rgb(44, 49, 58);")
        self.separator_url_bar_left.setFrameShadow(QFrame.Plain)
        self.separator_url_bar_left.setLineWidth(2)
        self.separator_url_bar_left.setMidLineWidth(0)
        self.separator_url_bar_left.setFrameShape(QFrame.Shape.VLine)

        self.tool_bar_center.addWidget(self.separator_url_bar_left)

        self.httpsIcon = QLabel(self.toolbar_container)
        self.httpsIcon.setObjectName("httpsIcon")
        self.httpsIcon.setMinimumSize(QSize(17, 17))
        self.httpsIcon.setMaximumSize(QSize(16, 16))
        self.httpsIcon.setLineWidth(0)
        self.httpsIcon.setPixmap(
            QPixmap(":/images/toolbar/images/toolbar/lock-open.png")
        )
        self.httpsIcon.setScaledContents(False)

        self.tool_bar_center.addWidget(self.httpsIcon)

        self.url_line_edit = QLineEdit(self.toolbar_container)
        self.url_line_edit.setObjectName("url_line_edit")
        self.url_line_edit.setMinimumSize(QSize(0, 30))
        self.url_line_edit.setMaximumSize(QSize(16777215, 30))

        self.tool_bar_center.addWidget(self.url_line_edit)

        self.stop_button = QPushButton(self.toolbar_container)
        self.stop_button.setObjectName("stop_button")
        self.stop_button.setMaximumSize(QSize(25, 25))
        icon10 = QIcon()
        icon10.addFile(
            ":/images/toolbar/images/toolbar/close.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.On,
        )
        icon10.addFile(
            ":/images/toolbar/images/toolbar/close-disabled.png",
            QSize(),
            QIcon.Mode.Disabled,
            QIcon.State.On,
        )
        self.stop_button.setIcon(icon10)
        self.stop_button.setIconSize(QSize(25, 25))

        self.tool_bar_center.addWidget(self.stop_button)

        self.separator_url_bar_right = QFrame(self.toolbar_container)
        self.separator_url_bar_right.setObjectName("separator_url_bar_right")
        self.separator_url_bar_right.setMinimumSize(QSize(0, 0))
        self.separator_url_bar_right.setMaximumSize(QSize(16777215, 40))
        self.separator_url_bar_right.setStyleSheet("background-color: rgb(44, 49, 58);")
        self.separator_url_bar_right.setLineWidth(2)
        self.separator_url_bar_right.setMidLineWidth(0)
        self.separator_url_bar_right.setFrameShape(QFrame.Shape.VLine)
        self.separator_url_bar_right.setFrameShadow(QFrame.Shadow.Sunken)

        self.tool_bar_center.addWidget(self.separator_url_bar_right)

        self.tool_bar_container_layout.addLayout(self.tool_bar_center)

        self.tool_bar_right = QHBoxLayout()
        self.tool_bar_right.setSpacing(30)
        self.tool_bar_right.setObjectName("tool_bar_right")
        self.tool_bar_right.setContentsMargins(20, -1, 20, -1)
        self.start_acquisition_button = QPushButton(self.toolbar_container)
        self.start_acquisition_button.setObjectName("start_acquisition_button")
        self.start_acquisition_button.setEnabled(True)
        self.start_acquisition_button.setMaximumSize(QSize(25, 25))
        icon11 = QIcon()
        icon11.addFile(
            ":/images/toolbar/images/toolbar/start.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.On,
        )
        icon11.addFile(
            ":/images/toolbar/images/toolbar/start-disabled.png",
            QSize(),
            QIcon.Mode.Disabled,
            QIcon.State.On,
        )
        self.start_acquisition_button.setIcon(icon11)
        self.start_acquisition_button.setIconSize(QSize(25, 25))

        self.tool_bar_right.addWidget(self.start_acquisition_button)

        self.stop_acquisition_button = QPushButton(self.toolbar_container)
        self.stop_acquisition_button.setObjectName("stop_acquisition_button")
        self.stop_acquisition_button.setEnabled(False)
        self.stop_acquisition_button.setMaximumSize(QSize(25, 25))
        icon12 = QIcon()
        icon12.addFile(
            ":/images/toolbar/images/toolbar/stop.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.On,
        )
        icon12.addFile(
            ":/images/toolbar/images/toolbar/stop-disabled.png",
            QSize(),
            QIcon.Mode.Disabled,
            QIcon.State.On,
        )
        self.stop_acquisition_button.setIcon(icon12)
        self.stop_acquisition_button.setIconSize(QSize(25, 25))

        self.tool_bar_right.addWidget(self.stop_acquisition_button)

        self.separator_screen_shot = QFrame(self.toolbar_container)
        self.separator_screen_shot.setObjectName("separator_screen_shot")
        self.separator_screen_shot.setMinimumSize(QSize(0, 40))
        self.separator_screen_shot.setMaximumSize(QSize(16777215, 40))
        self.separator_screen_shot.setStyleSheet("background-color: rgb(44, 49, 58);")
        self.separator_screen_shot.setLineWidth(2)
        self.separator_screen_shot.setFrameShape(QFrame.Shape.VLine)
        self.separator_screen_shot.setFrameShadow(QFrame.Shadow.Sunken)

        self.tool_bar_right.addWidget(self.separator_screen_shot)

        self.screenshot_visible_area_button = QPushButton(self.toolbar_container)
        self.screenshot_visible_area_button.setObjectName(
            "screenshot_visible_area_button"
        )
        self.screenshot_visible_area_button.setEnabled(False)
        self.screenshot_visible_area_button.setMaximumSize(QSize(25, 25))
        icon13 = QIcon()
        icon13.addFile(
            ":/images/toolbar/images/toolbar/camera.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.On,
        )
        icon13.addFile(
            ":/images/toolbar/images/toolbar/camera-disabled.png",
            QSize(),
            QIcon.Mode.Disabled,
            QIcon.State.On,
        )
        self.screenshot_visible_area_button.setIcon(icon13)
        self.screenshot_visible_area_button.setIconSize(QSize(25, 25))

        self.tool_bar_right.addWidget(self.screenshot_visible_area_button)

        self.screenshot_selected_area_button = QPushButton(self.toolbar_container)
        self.screenshot_selected_area_button.setObjectName(
            "screenshot_selected_area_button"
        )
        self.screenshot_selected_area_button.setEnabled(False)
        self.screenshot_selected_area_button.setMaximumSize(QSize(25, 25))
        icon14 = QIcon()
        icon14.addFile(
            ":/images/toolbar/images/toolbar/select.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.On,
        )
        icon14.addFile(
            ":/images/toolbar/images/toolbar/select-disabled.png",
            QSize(),
            QIcon.Mode.Disabled,
            QIcon.State.On,
        )
        self.screenshot_selected_area_button.setIcon(icon14)
        self.screenshot_selected_area_button.setIconSize(QSize(25, 25))

        self.tool_bar_right.addWidget(self.screenshot_selected_area_button)

        self.screenshot_full_page_button = QPushButton(self.toolbar_container)
        self.screenshot_full_page_button.setObjectName("screenshot_full_page_button")
        self.screenshot_full_page_button.setEnabled(False)
        self.screenshot_full_page_button.setMinimumSize(QSize(25, 25))
        self.screenshot_full_page_button.setMaximumSize(QSize(25, 25))
        icon15 = QIcon()
        icon15.addFile(
            ":/images/toolbar/images/toolbar/scroll.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.On,
        )
        icon15.addFile(
            ":/images/toolbar/images/toolbar/scroll-disabled.png",
            QSize(),
            QIcon.Mode.Disabled,
            QIcon.State.On,
        )
        self.screenshot_full_page_button.setIcon(icon15)
        self.screenshot_full_page_button.setIconSize(QSize(25, 25))

        self.tool_bar_right.addWidget(self.screenshot_full_page_button)

        self.tool_bar_container_layout.addLayout(self.tool_bar_right)

        self.content_tool_bar_layout.addWidget(self.toolbar_container)

        self.verticalLayout_2.addWidget(self.content_tool_bar)

        self.content_bottom = QFrame(self.content_box)
        self.content_bottom.setObjectName("content_bottom")
        self.content_bottom.setMaximumSize(QSize(16777215, 16777215))
        self.content_bottom.setFrameShape(QFrame.NoFrame)
        self.content_bottom.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.content_bottom)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QFrame(self.content_bottom)
        self.content.setObjectName("content")
        self.content.setEnabled(True)
        self.content.setStyleSheet("")
        self.content.setFrameShape(QFrame.NoFrame)
        self.content.setFrameShadow(QFrame.Raised)
        self.contentTabsLayout = QHBoxLayout(self.content)
        self.contentTabsLayout.setSpacing(0)
        self.contentTabsLayout.setObjectName("contentTabsLayout")
        self.contentTabsLayout.setSizeConstraint(QLayout.SetNoConstraint)
        self.contentTabsLayout.setContentsMargins(0, 0, 0, 0)
        self.tabs = QTabWidget(self.content)
        self.tabs.setObjectName("tabs")
        self.tabs.setLayoutDirection(Qt.LeftToRight)
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
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setTabShape(QTabWidget.Rounded)
        self.tabs.setElideMode(Qt.ElideLeft)
        self.tabs.setDocumentMode(False)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(False)
        self.tabs.setTabBarAutoHide(True)
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.tabs.addTab(self.tab, "")

        self.contentTabsLayout.addWidget(self.tabs)

        self.verticalLayout_6.addWidget(self.content)

        self.bottom_bar = QFrame(self.content_bottom)
        self.bottom_bar.setObjectName("bottom_bar")
        self.bottom_bar.setMinimumSize(QSize(0, 42))
        self.bottom_bar.setMaximumSize(QSize(16777215, 42))
        self.bottom_bar.setFrameShape(QFrame.NoFrame)
        self.bottom_bar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottom_bar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.credits_label = QLabel(self.bottom_bar)
        self.credits_label.setObjectName("credits_label")
        self.credits_label.setMaximumSize(QSize(120, 16))
        self.credits_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )

        self.horizontalLayout_5.addWidget(self.credits_label)

        self.bottom_bar_left_spacer = QSpacerItem(
            20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_5.addItem(self.bottom_bar_left_spacer)

        self.progress_bar = QProgressBar(self.bottom_bar)
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setMinimumSize(QSize(200, 0))
        self.progress_bar.setMaximumSize(QSize(200, 20))
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
        self.progress_bar.setValue(24)

        self.horizontalLayout_5.addWidget(self.progress_bar)

        self.bottom_bar_central_spacer = QSpacerItem(
            20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_5.addItem(self.bottom_bar_central_spacer)

        self.status_message = QLabel(self.bottom_bar)
        self.status_message.setObjectName("status_message")
        self.status_message.setMinimumSize(QSize(300, 0))
        self.status_message.setStyleSheet("font-size:14px;\n" "color:#ffffff;")

        self.horizontalLayout_5.addWidget(self.status_message)

        self.bottom_bar_right_spacer = QSpacerItem(
            20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_5.addItem(self.bottom_bar_right_spacer)

        self.version = QLabel(self.bottom_bar)
        self.version.setObjectName("version")
        self.version.setMaximumSize(QSize(120, 16777215))
        self.version.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.version)

        self.frame_size_grip = QFrame(self.bottom_bar)
        self.frame_size_grip.setObjectName("frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_5.addWidget(self.frame_size_grip)

        self.verticalLayout_6.addWidget(self.bottom_bar)

        self.verticalLayout_2.addWidget(self.content_bottom)

        self.appLayout.addWidget(self.content_box)

        self.appMargins.addWidget(self.bg_app)

        fit_web.setCentralWidget(self.styleSheet)

        self.retranslateUi(fit_web)

        self.tabs.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(fit_web)

    # setupUi

    def retranslateUi(self, fit_web):
        fit_web.setWindowTitle(
            QCoreApplication.translate("fit_web", "FIT Web Scraper", None)
        )
        self.top_logo.setText("")
        self.title_right_info.setText(
            QCoreApplication.translate("fit_web", "Web Scraper", None)
        )
        # if QT_CONFIG(tooltip)
        self.verify_timestamp_button.setToolTip(
            QCoreApplication.translate("fit_web", "Verify timestamp", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.verify_timestamp_button.setText("")
        # if QT_CONFIG(tooltip)
        self.verify_pec_button.setToolTip(
            QCoreApplication.translate("fit_web", "Verify PEC", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.verify_pec_button.setText("")
        # if QT_CONFIG(tooltip)
        self.case_button.setToolTip(
            QCoreApplication.translate("fit_web", "Case info", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.case_button.setText("")
        # if QT_CONFIG(tooltip)
        self.configuration_button.setToolTip(
            QCoreApplication.translate("fit_web", "Configuration", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.configuration_button.setText("")
        # if QT_CONFIG(tooltip)
        self.minimize_button.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.minimize_button.setText("")
        # if QT_CONFIG(tooltip)
        self.close_button.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.close_button.setText("")
        # if QT_CONFIG(tooltip)
        self.back_button.setToolTip(
            QCoreApplication.translate("fit_web", "Back to previous page", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.back_button.setText("")
        # if QT_CONFIG(tooltip)
        self.forward_button.setToolTip(
            QCoreApplication.translate("fit_web", "Forward to next page", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.forward_button.setText("")
        # if QT_CONFIG(tooltip)
        self.reload_button.setToolTip(
            QCoreApplication.translate("fit_web", "Reload page", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.reload_button.setText("")
        # if QT_CONFIG(tooltip)
        self.home_button.setToolTip(
            QCoreApplication.translate("fit_web", "Go home", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.home_button.setText("")
        self.httpsIcon.setText("")
        # if QT_CONFIG(tooltip)
        self.stop_button.setToolTip(
            QCoreApplication.translate("fit_web", "Stop loading current page", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.stop_button.setText("")
        # if QT_CONFIG(tooltip)
        self.start_acquisition_button.setToolTip(
            QCoreApplication.translate("fit_web", "Start acquisition", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.start_acquisition_button.setStatusTip("")
        # endif // QT_CONFIG(statustip)
        self.start_acquisition_button.setText("")
        # if QT_CONFIG(tooltip)
        self.stop_acquisition_button.setToolTip(
            QCoreApplication.translate("fit_web", "Stop acquisition", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.stop_acquisition_button.setStatusTip("")
        # endif // QT_CONFIG(statustip)
        self.stop_acquisition_button.setText("")
        # if QT_CONFIG(tooltip)
        self.screenshot_visible_area_button.setToolTip(
            QCoreApplication.translate(
                "fit_web", "Take a screenshot on view area", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.screenshot_visible_area_button.setText("")
        # if QT_CONFIG(tooltip)
        self.screenshot_selected_area_button.setToolTip(
            QCoreApplication.translate(
                "fit_web", "Take a screenshot on the selected area", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.screenshot_selected_area_button.setStatusTip("")
        # endif // QT_CONFIG(statustip)
        self.screenshot_selected_area_button.setText("")
        # if QT_CONFIG(tooltip)
        self.screenshot_full_page_button.setToolTip(
            QCoreApplication.translate("fit_web", "Take a full page screenshot", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.screenshot_full_page_button.setText("")
        self.tabs.setTabText(
            self.tabs.indexOf(self.tab),
            QCoreApplication.translate("fit_web", "Tab1", None),
        )
        self.credits_label.setText(
            QCoreApplication.translate("fit_web", "By: fit-project.org", None)
        )
        self.status_message.setText(
            QCoreApplication.translate("fit_web", "status message", None)
        )
        self.version.setText(QCoreApplication.translate("fit_web", "v1.0.3", None))

    # retranslateUi
