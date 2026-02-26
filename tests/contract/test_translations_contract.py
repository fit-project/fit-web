from __future__ import annotations

import json
from pathlib import Path

import pytest


@pytest.mark.contract
def test_language_files_define_required_keys() -> None:
    lang_dir = Path(__file__).resolve().parents[2] / "fit_web" / "lang"
    en = json.loads((lang_dir / "en.json").read_text(encoding="utf-8"))
    it = json.loads((lang_dir / "it.json").read_text(encoding="utf-8"))

    required_keys = {
        "SAVE_PAGE",
        "SAVE_PAGE_STARTED",
        "SAVE_PAGE_COMPLETED",
        "FULL_PAGE_SCREENSHOT",
        "FULL_PAGE_SCREENSHOT_ERROR_MESSAGE",
        "OS_PROXY_CONFIG_ERROR_TITLE",
        "OS_PROXY_CONFIG_ERROR_MESSAGE",
        "MITM_PROXY_ERROR_TITLE",
        "MITM_PROXY_ERROR_MESSAGE",
        "UNSUPPORTED_OS_DIALOG_TITLE",
        "UNSUPPORTED_OS_DIALOG_MESSAGE",
        "OS_VERSION_ERROR_DIALOG_TITLE",
        "MACOS_VERSION_ERROR_DIALOG_MESSAGE",
        "APPLICATION_ERROR_DIALOG_TITLE",
        "APPLICATION_ERROR_DIALOG_MESSAGE",
    }

    assert required_keys.issubset(en.keys())
    assert required_keys.issubset(it.keys())
