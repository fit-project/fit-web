import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QLineEdit
)
from PySide6.QtGui import QAction
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

class MiniBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini FIT Browser")
        self.setGeometry(100, 100, 1024, 768)

        # Vista browser
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.setCentralWidget(self.browser)

        # Toolbar
        nav_bar = QToolBar("Navigation")
        self.addToolBar(nav_bar)

        # Pulsanti di navigazione
        back_btn = QAction("←", self)
        back_btn.triggered.connect(self.browser.back)
        nav_bar.addAction(back_btn)

        forward_btn = QAction("→", self)
        forward_btn.triggered.connect(self.browser.forward)
        nav_bar.addAction(forward_btn)

        reload_btn = QAction("⟳", self)
        reload_btn.triggered.connect(self.browser.reload)
        nav_bar.addAction(reload_btn)

        # Campo URL
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url_bar)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def update_url_bar(self, qurl):
        self.url_bar.setText(qurl.toString())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiniBrowser()
    window.show()
    sys.exit(app.exec())
