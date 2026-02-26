from __future__ import annotations

from pathlib import Path

import pytest

from fit_web.mitmproxy.runner import MitmproxyRunner


@pytest.mark.integration
def test_capture_control_file_start_and_stop(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("FIT_USER_APP_PATH", str(tmp_path))
    runner = MitmproxyRunner()
    assert runner.control_file is not None

    assert runner.start_capture() is True
    assert runner.control_file.read_text(encoding="utf-8") == "start"

    assert runner.stop_capture() is True
    assert runner.control_file.read_text(encoding="utf-8") == "stop"


@pytest.mark.integration
def test_runner_without_fit_user_app_path_cannot_write_control(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("FIT_USER_APP_PATH", raising=False)
    runner = MitmproxyRunner()
    assert runner.output_dir is None
    assert runner.start_capture() is False
    assert runner.stop_capture() is False
