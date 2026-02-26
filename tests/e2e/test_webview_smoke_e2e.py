from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
from PySide6 import QtCore


@pytest.mark.e2e
@pytest.mark.skipif(sys.platform != "darwin", reason="macOS-only test")
def test_system_webview_loads_local_page(qapp, tmp_path: Path) -> None:
    if os.environ.get("QT_QPA_PLATFORM") == "offscreen":
        pytest.skip("SystemWebView requires native macOS windowing")

    bridge = pytest.importorskip("fit_webview_bridge")
    SystemWebView = bridge.SystemWebView

    html_path = tmp_path / "smoke.html"
    html_path.write_text("<html><body><h1>FIT Web Smoke</h1></body></html>")

    view = SystemWebView()
    view.setMinimumSize(900, 600)
    loaded = {"ok": False}

    loop = QtCore.QEventLoop()
    timeout = {"fired": False}

    def on_timeout() -> None:
        timeout["fired"] = True
        loop.quit()

    timer = QtCore.QTimer()
    timer.setSingleShot(True)
    timer.timeout.connect(on_timeout)
    timer.start(10000)

    def on_load_finished(ok: bool) -> None:
        loaded["ok"] = bool(ok)
        loop.quit()

    if hasattr(view, "loadFinished"):
        view.loadFinished.connect(on_load_finished)
    else:
        pytest.skip("SystemWebView does not expose loadFinished")

    view.setUrl(html_path.as_uri())
    view.show()
    loop.exec()
    view.close()

    assert timeout["fired"] is False
    assert loaded["ok"] is True
