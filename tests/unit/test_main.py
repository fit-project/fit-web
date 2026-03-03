from __future__ import annotations

import argparse
import types

import pytest

import main as main_module
from fit_bootstrap.signals import BootstrapResult, BootstrapSignal


@pytest.mark.unit
def test_parse_args_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(main_module.sys, "argv", ["main.py"])
    args = main_module.parse_args()
    assert isinstance(args, argparse.Namespace)
    assert args.debug == "none"


@pytest.mark.unit
def test_parse_args_accepts_debug_verbose(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(main_module.sys, "argv", ["main.py", "--debug", "verbose"])
    args = main_module.parse_args()
    assert args.debug == "verbose"


@pytest.mark.unit
def test_log_bootstrap_result_error(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, str] = {}
    monkeypatch.setattr(
        main_module,
        "bootstrap_load_translations",
        lambda: {
            "BOOSTSTRAP_ERROR_DIALOG_TITLE": "Bootstrap Error",
        },
    )
    monkeypatch.setattr(
        main_module,
        "show_dialog",
        lambda _kind, title, message, _details="": captured.update(
            {"title": title, "message": message}
        ),
    )
    result = BootstrapResult(signal=BootstrapSignal.ERROR, code=1, message="boom")
    main_module._log_bootstrap_result(result)
    assert captured["title"] == "Bootstrap Error"
    assert captured["message"] == "boom"


@pytest.mark.unit
def test_main_mitm_launch_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FIT_MITM_LAUNCH", "1")
    monkeypatch.setattr(main_module, "restore_persisted_proxy_state", lambda: True)
    fake_main = types.SimpleNamespace(mitmdump=lambda: 42)
    monkeypatch.setitem(main_module.sys.modules, "mitmproxy.tools.main", fake_main)
    assert main_module.main() == 42
    monkeypatch.delenv("FIT_MITM_LAUNCH", raising=False)


@pytest.mark.unit
def test_main_proxy_restore_watchdog_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FIT_PROXY_RESTORE_WATCHDOG", "1")
    monkeypatch.setenv("FIT_PROXY_RESTORE_PARENT_PID", "321")
    monkeypatch.setattr(main_module, "run_proxy_restore_watchdog", lambda pid: pid + 1)
    assert main_module.main() == 322
    monkeypatch.delenv("FIT_PROXY_RESTORE_WATCHDOG", raising=False)
    monkeypatch.delenv("FIT_PROXY_RESTORE_PARENT_PID", raising=False)


@pytest.mark.unit
def test_main_askpass_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FIT_MITM_LAUNCH", raising=False)
    monkeypatch.setattr(main_module, "get_platform", lambda: "macos")
    monkeypatch.setenv("FIT_ASKPASS_DIALOG", "1")
    monkeypatch.setitem(
        main_module.sys.modules,
        "fit_bootstrap.macos.askpass_dialog",
        types.SimpleNamespace(main=lambda: 7),
    )
    assert main_module.main() == 7
    monkeypatch.delenv("FIT_ASKPASS_DIALOG", raising=False)


@pytest.mark.unit
def test_main_gui_stage_requires_admin(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FIT_MITM_LAUNCH", raising=False)
    monkeypatch.setenv(main_module.STAGE_ENV, main_module.STAGE_GUI)
    monkeypatch.setattr(main_module, "restore_persisted_proxy_state", lambda: True)
    monkeypatch.setattr(main_module, "parse_args", lambda: types.SimpleNamespace(debug="none"))
    monkeypatch.setattr(main_module, "is_admin", lambda: False)
    assert main_module.main() == 1


@pytest.mark.unit
def test_main_gui_stage_runs_gui_when_lock_acquired(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FIT_MITM_LAUNCH", raising=False)
    monkeypatch.setenv(main_module.STAGE_ENV, main_module.STAGE_GUI)
    monkeypatch.setattr(main_module, "restore_persisted_proxy_state", lambda: True)
    monkeypatch.setattr(main_module, "parse_args", lambda: types.SimpleNamespace(debug="none"))
    monkeypatch.setattr(main_module, "is_admin", lambda: True)
    monkeypatch.setattr(main_module, "acquire_app_lock", lambda: True)
    monkeypatch.setattr(main_module, "_run_gui", lambda: 9)
    assert main_module.main() == 9


@pytest.mark.unit
def test_main_non_gui_stops_mitm_on_preflight_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _BootstrapFake:
        def __init__(self, debug_enabled: bool) -> None:
            self.debug_enabled = debug_enabled

        def _dispatch(self, on_signal, argv, stage_env, stage_gui):
            return BootstrapResult(
                signal=BootstrapSignal.ERROR, code=2, message="nope"
            )

    class _MitmRunnerFake:
        def __init__(self) -> None:
            self.stopped = False

        def start(self) -> bool:
            return True

        def stop_by_pid(self) -> bool:
            self.stopped = True
            return True

    runner = _MitmRunnerFake()
    monkeypatch.delenv("FIT_MITM_LAUNCH", raising=False)
    monkeypatch.setenv(main_module.STAGE_ENV, "ENV_STAGE")
    monkeypatch.setattr(main_module, "restore_persisted_proxy_state", lambda: True)
    monkeypatch.setattr(main_module, "parse_args", lambda: types.SimpleNamespace(debug="none"))
    monkeypatch.setattr(main_module, "Bootstrap", _BootstrapFake)
    monkeypatch.setattr(main_module, "MitmproxyRunner", lambda *_args, **_kwargs: runner)
    rc = main_module.main()
    assert rc == 2
    assert runner.stopped is True


@pytest.mark.unit
def test_main_non_gui_returns_one_when_mitm_start_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = types.SimpleNamespace(start=lambda: False)
    monkeypatch.delenv("FIT_MITM_LAUNCH", raising=False)
    monkeypatch.setenv(main_module.STAGE_ENV, "ENV_STAGE")
    monkeypatch.setattr(main_module, "restore_persisted_proxy_state", lambda: True)
    monkeypatch.setattr(
        main_module, "parse_args", lambda: types.SimpleNamespace(debug="none")
    )
    monkeypatch.setattr(main_module, "MitmproxyRunner", lambda *_args, **_kwargs: runner)
    assert main_module.main() == 1


@pytest.mark.unit
def test_show_crash_dialog_restores_persisted_proxy_state(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []
    monkeypatch.setattr(main_module, "restore_persisted_proxy_state", lambda: calls.append("restore") or True)
    monkeypatch.setattr(
        main_module,
        "load_translations",
        lambda: {
            "APPLICATION_ERROR_DIALOG_TITLE": "title",
            "APPLICATION_ERROR_DIALOG_MESSAGE": "message",
        },
    )
    monkeypatch.setattr(main_module, "show_dialog", lambda *args, **kwargs: None)
    main_module.show_crash_dialog("boom")
    assert calls == ["restore"]
