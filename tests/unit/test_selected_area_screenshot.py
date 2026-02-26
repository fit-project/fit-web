from __future__ import annotations

import pytest

from fit_web.selected_area_screenshot import SnippingWidget


@pytest.mark.unit
def test_apply_scaling_factor_uses_widget_scale_factor(
    qapp, monkeypatch: pytest.MonkeyPatch
) -> None:
    widget = SnippingWidget(filename="dummy.png")
    monkeypatch.setattr(widget, "scale_factor", 2.0)
    assert widget.apply_scaling_factor(1, 2, 3, 4) == (2, 4, 6, 8)
