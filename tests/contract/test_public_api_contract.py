from __future__ import annotations

import inspect

import pytest

from fit_web.os_proxy_setup import ProxyState
from fit_web.web import Web


@pytest.mark.contract
def test_proxy_state_contract_fields_are_stable() -> None:
    fields = list(ProxyState.__dataclass_fields__.keys())  # type: ignore[attr-defined]
    assert fields == [
        "web_enabled",
        "web_host",
        "web_port",
        "secure_enabled",
        "secure_host",
        "secure_port",
        "auto_enabled",
        "auto_url",
        "bypass_domains",
    ]


@pytest.mark.contract
def test_web_contract_exposes_core_workflow_methods() -> None:
    required = [
        "execute_stop_tasks_flow",
        "on_post_acquisition_finished",
        "on_start_tasks_finished",
        "on_stop_tasks_finished",
    ]
    for method_name in required:
        assert callable(getattr(Web, method_name, None)), method_name


@pytest.mark.contract
def test_web_constructor_accepts_optional_wizard_parameter() -> None:
    signature = inspect.signature(Web.__init__)
    assert "wizard" in signature.parameters
    assert signature.parameters["wizard"].default is None
