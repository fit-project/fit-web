from __future__ import annotations

import pytest

from fit_web.web import Web


@pytest.mark.unit
def test_js_quote_escapes_special_characters() -> None:
    escaped = Web._Web__js_quote("a'b\\c\n")
    assert escaped == "a\\'b\\\\c\\n"
