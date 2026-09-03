import json

from fit_web.tasks.save_page import TaskSavePageWorker


def test_sanitize_har_normalizes_origin_request_url(tmp_path):
    source = tmp_path / "capture.har"
    target = tmp_path / "capture.sanitized.har"
    source.write_text(
        json.dumps(
            {
                "log": {
                    "entries": [
                        {"request": {"url": "https://example.com?query=value"}}
                    ]
                }
            }
        ),
        encoding="utf-8",
    )

    replacements = TaskSavePageWorker._sanitize_har_for_warc(source, target)

    data = json.loads(target.read_text(encoding="utf-8"))
    assert data["log"]["entries"][0]["request"]["url"] == (
        "https://example.com/?query=value"
    )
    assert replacements == 1


def test_normalize_http_url_preserves_existing_path():
    assert TaskSavePageWorker._normalize_http_url("https://example.com/page") == (
        "https://example.com/page"
    )


def test_build_wacz_retries_without_seed_when_seed_is_missing(tmp_path, monkeypatch):
    har = tmp_path / "capture.har"
    har.write_text('{"log":{"entries":[]}}', encoding="utf-8")
    acquisition = tmp_path / "acquisition"
    acquisition.mkdir()
    worker = TaskSavePageWorker()
    worker.options = {
        "acquisition_directory": str(acquisition),
        "url": "https://example.com/page",
    }
    worker.acquisition_directory = str(acquisition)
    monkeypatch.setattr(worker, "_get_capture_har_path", lambda: str(har))
    monkeypatch.setattr(worker, "_sanitize_har_for_warc", lambda *_args: 0)
    monkeypatch.setattr("fit_web.tasks.save_page.har2warc", lambda *_args, **_kwargs: None)

    calls = []

    def create_wacz(_warc, output, **kwargs):
        calls.append(kwargs)
        if kwargs.get("page_url"):
            raise ValueError("ts None not found in index with https://example.com/page")
        open(output, "wb").close()
        return 0

    monkeypatch.setattr(worker, "_create_wacz", create_wacz)

    worker._build_wacz()

    assert calls == [
        {"page_url": "https://example.com/page"},
        {},
    ]
    assert (acquisition / "acquisition_page.wacz").exists()
