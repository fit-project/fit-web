import sys

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)

view = QWebEngineView()
view.setUrl("https://www.w3schools.com/html/mov_bbb.mp4")  # MP4 H.264
view.setWindowTitle("Test codec H.264 - PySide6")
view.resize(800, 600)
view.show()

sys.exit(app.exec())
