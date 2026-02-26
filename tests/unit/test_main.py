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
def test_mac_ok_non_macos(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(main_module, "get_platform", lambda: "linux")
    assert main_module._mac_ok() is True


@pytest.mark.unit
def test_mac_ok_checks_minimum_version(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(main_module, "get_platform", lambda: "macos")
    monkeypatch.setattr(main_module.platform, "mac_ver", lambda: ("11.2", ("", "", ""), ""))
    assert main_module._mac_ok() is False
    monkeypatch.setattr(main_module.platform, "mac_ver", lambda: ("11.3", ("", "", ""), ""))
    assert main_module._mac_ok() is True


@pytest.mark.unit
def test_ensure_macos_or_exit_shows_dialog(monkeypatch: pytest.MonkeyPatch) -> None:
    called: dict[str, str] = {}
    monkeypatch.setattr(main_module, "get_platform", lambda: "linux")
    monkeypatch.setattr(
        main_module,
        "load_translations",
        lambda: {
            "UNSUPPORTED_OS_DIALOG_TITLE": "title",
            "UNSUPPORTED_OS_DIALOG_MESSAGE": "message",
        },
    )
    monkeypatch.setattr(
        main_module,
        "show_dialog",
        lambda _kind, title, message, _details: called.update(
            {"title": title, "message": message}
        ),
    )
    with pytest.raises(SystemExit):
        main_module._ensure_macos_or_exit()
    assert called["title"] == "title"
    assert called["message"] == "message"


@pytest.mark.unit
def test_log_bootstrap_result_admin_denied(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, str] = {}
    monkeypatch.setattr(main_module, "get_platform", lambda: "macos")
    monkeypatch.setattr(
        main_module,
        "bootstrap_load_translations",
        lambda: {
            "BOOSTSTRAP_ERROR_DIALOG_TITLE": "Bootstrap Error",
            "BOOSTSTRAP_ADMIN_DENIED_MESSAGE": "Need {} privileges. Relaunch as {}.",
        },
    )
    monkeypatch.setattr(
        main_module,
        "show_dialog",
        lambda _kind, title, message, _details="": captured.update(
            {"title": title, "message": message}
        ),
    )
    result = BootstrapResult(signal=BootstrapSignal.ADMIN_DENIED, code=1, message="")
    main_module._log_bootstrap_result(result)
    assert captured["title"] == "Bootstrap Error"
    assert "root" in captured["message"]


@pytest.mark.unit
def test_main_mitm_launch_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FIT_MITM_LAUNCH", "1")
    fake_main = types.SimpleNamespace(mitmdump=lambda: 42)
    monkeypatch.setitem(main_module.sys.modules, "mitmproxy.tools.main", fake_main)
    assert main_module.main() == 42
    monkeypatch.delenv("FIT_MITM_LAUNCH", raising=False)


@pytest.mark.unit
def test_main_gui_stage_requires_admin(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FIT_MITM_LAUNCH", raising=False)
    monkeypatch.setenv(main_module.STAGE_ENV, main_module.STAGE_GUI)
    monkeypatch.setattr(main_module, "parse_args", lambda: types.SimpleNamespace(debug="none"))
    monkeypatch.setattr(main_module, "is_admin", lambda: False)
    assert main_module.main() == 1


@pytest.mark.unit
def test_main_gui_stage_runs_gui_when_lock_acquired(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FIT_MITM_LAUNCH", raising=False)
    monkeypatch.setenv(main_module.STAGE_ENV, main_module.STAGE_GUI)
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
                signal=BootstrapSignal.UNSUPPORTED_OS, code=2, message="nope"
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
    monkeypatch.setattr(main_module, "parse_args", lambda: types.SimpleNamespace(debug="none"))
    monkeypatch.setattr(main_module, "Bootstrap", _BootstrapFake)
    monkeypatch.setattr(main_module, "MitmproxyRunner", lambda *_args, **_kwargs: runner)
    rc = main_module.main()
    assert rc == 2
    assert runner.stopped is True
