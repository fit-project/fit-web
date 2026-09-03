from __future__ import annotations

import types
from pathlib import Path

import pytest

from fit_web.mitmproxy.addons.fit_capture import FitCapture


@pytest.mark.unit
def test_export_har_uses_configured_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    capture = FitCapture()
    capture._flows = ["flow1"]  # type: ignore[assignment]

    called: dict[str, object] = {}

    def _export_har(flows, path):
        called["flows"] = flows
        called["path"] = path
        Path(path).write_text("har", encoding="utf-8")

    capture._savehar = types.SimpleNamespace(export_har=_export_har)
    fake_ctx = types.SimpleNamespace(
        options=types.SimpleNamespace(hardump=str(tmp_path / "out.har")),
        log=types.SimpleNamespace(info=lambda *_a, **_k: None, warn=lambda *_a, **_k: None, error=lambda *_a, **_k: None),
    )
    monkeypatch.setattr("fit_web.mitmproxy.addons.fit_capture.ctx", fake_ctx)
    capture._export_har()
    assert called["path"] == str(tmp_path / ".out.har.tmp")
    assert called["flows"] == ["flow1"]
    assert (tmp_path / "out.har").exists()


@pytest.mark.unit
def test_export_har_without_path_logs_warning(monkeypatch: pytest.MonkeyPatch) -> None:
    capture = FitCapture()
    warnings: list[str] = []
    fake_ctx = types.SimpleNamespace(
        options=types.SimpleNamespace(hardump=""),
        log=types.SimpleNamespace(
            info=lambda *_a, **_k: None,
            warn=lambda msg: warnings.append(msg),
            error=lambda *_a, **_k: None,
        ),
    )
    monkeypatch.setattr("fit_web.mitmproxy.addons.fit_capture.ctx", fake_ctx)
    capture._har_path = ""
    capture._export_har()
    assert warnings


@pytest.mark.unit
def test_signal_export_writes_matching_status_atomically(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    capture = FitCapture()
    capture._export_status_path = tmp_path / "capture.export-status"
    fake_ctx = types.SimpleNamespace(
        log=types.SimpleNamespace(error=lambda *_a, **_k: None)
    )
    monkeypatch.setattr("fit_web.mitmproxy.addons.fit_capture.ctx", fake_ctx)

    capture._signal_export("request-1", True)

    assert capture._export_status_path.read_text() == "request-1:ok"
    assert not (tmp_path / ".capture.export-status.tmp").exists()


@pytest.mark.unit
def test_response_collects_flows_only_when_collecting() -> None:
    capture = FitCapture()
    flow = types.SimpleNamespace(websocket=None)
    capture.response(flow)
    assert capture._flows == []
    capture._collecting = True
    capture.response(flow)
    assert capture._flows == [flow]
