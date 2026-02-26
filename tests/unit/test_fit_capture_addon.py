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

    capture._savehar = types.SimpleNamespace(export_har=_export_har)
    fake_ctx = types.SimpleNamespace(
        options=types.SimpleNamespace(hardump=str(tmp_path / "out.har")),
        log=types.SimpleNamespace(info=lambda *_a, **_k: None, warn=lambda *_a, **_k: None, error=lambda *_a, **_k: None),
    )
    monkeypatch.setattr("fit_web.mitmproxy.addons.fit_capture.ctx", fake_ctx)
    capture._export_har()
    assert called["path"] == str(tmp_path / "out.har")
    assert called["flows"] == ["flow1"]


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
def test_response_collects_flows_only_when_collecting() -> None:
    capture = FitCapture()
    flow = types.SimpleNamespace(websocket=None)
    capture.response(flow)
    assert capture._flows == []
    capture._collecting = True
    capture.response(flow)
    assert capture._flows == [flow]
