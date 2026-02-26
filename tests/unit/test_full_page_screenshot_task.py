from __future__ import annotations

import os

import pytest

from fit_web.tasks.full_page_screenshot import screenshot_filename


@pytest.mark.unit
def test_screenshot_filename_uses_prefix_and_extension(tmp_path) -> None:
    path = screenshot_filename(str(tmp_path), "full_page_test")
    assert str(tmp_path) in path
    assert os.path.basename(path).startswith("full_page_test_")
    assert path.endswith(".png")


@pytest.mark.unit
def test_screenshot_filename_allows_custom_extension(tmp_path) -> None:
    path = screenshot_filename(str(tmp_path), "capture", ".jpg")
    assert path.endswith(".jpg")
