from __future__ import annotations

import pytest

from fit_web.widgets.find_bar import FindBar


@pytest.mark.unit
def test_find_bar_js_quote_escapes_special_characters() -> None:
    escaped = FindBar._FindBar__js_quote("a'b\\c\n")
    assert escaped == "a\\'b\\\\c\\n"
