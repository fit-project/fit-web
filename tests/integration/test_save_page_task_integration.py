from __future__ import annotations

from pathlib import Path

import pytest

from fit_web.tasks.save_page import TaskSavePageWorker


@pytest.mark.integration
def test_get_capture_har_path_uses_fit_user_app_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FIT_USER_APP_PATH", str(tmp_path))
    worker = TaskSavePageWorker()
    path = worker._get_capture_har_path()
    assert path == str(tmp_path / "mitmproxy" / "capture.har")


@pytest.mark.integration
def test_build_wacz_raises_when_har_missing(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    worker = TaskSavePageWorker()
    worker.acquisition_directory = str(tmp_path)
    monkeypatch.setattr(worker, "_get_capture_har_path", lambda: str(tmp_path / "missing.har"))
    with pytest.raises(FileNotFoundError):
        worker._build_wacz()


@pytest.mark.integration
def test_build_wacz_happy_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    worker = TaskSavePageWorker()
    worker.acquisition_directory = str(tmp_path)
    har_path = tmp_path / "capture.har"
    har_path.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(worker, "_get_capture_har_path", lambda: str(har_path))

    created: dict[str, str] = {}

    def _fake_har2warc(_har, warc_path, gzip, filename, rec_title):
        Path(warc_path).write_text("warc", encoding="utf-8")
        created["warc"] = warc_path

    def _fake_create_wacz(warc_path: str, wacz_path: str, disable_post_append: bool = False):
        Path(wacz_path).write_text("wacz", encoding="utf-8")
        created["wacz"] = wacz_path
        return 0

    monkeypatch.setattr("fit_web.tasks.save_page.har2warc", _fake_har2warc)
    monkeypatch.setattr(worker, "_create_wacz", _fake_create_wacz)

    worker._build_wacz()
    final_wacz = tmp_path / "acquisition_page.wacz"
    assert final_wacz.exists()
    assert final_wacz.read_text(encoding="utf-8") == "wacz"
    assert "warc" in created and "wacz" in created
