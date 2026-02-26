from __future__ import annotations

import pytest

from fit_web import lang as lang_module


@pytest.mark.unit
def test_load_translations_uses_selected_language() -> None:
    translations = lang_module.load_translations("it")
    assert (
        translations["UNSUPPORTED_OS_DIALOG_TITLE"] == "FIT Web Errore OS"
    )


@pytest.mark.unit
def test_load_translations_falls_back_to_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(lang_module, "DEFAULT_LANG", "en")
    translations = lang_module.load_translations("zz")
    assert translations["UNSUPPORTED_OS_DIALOG_TITLE"] == "FIT Web OS Error"


@pytest.mark.unit
def test_load_translations_uses_system_language_when_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(lang_module, "get_system_lang", lambda: "en")
    translations = lang_module.load_translations()
    assert "SAVE_PAGE" in translations
