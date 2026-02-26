from __future__ import annotations

import types
from pathlib import Path

import pytest

from fit_web import web as web_module


class _Toggle:
    def __init__(self) -> None:
        self.enabled: bool | None = None

    def setEnabled(self, value: bool) -> None:
        self.enabled = value


class _ProgressBar:
    def __init__(self) -> None:
        self.values: list[int] = []

    def setValue(self, value: int) -> None:
        self.values.append(value)


class _StatusBar:
    def __init__(self) -> None:
        self.text = ""

    def setText(self, value: str) -> None:
        self.text = value


class _FakeUrl:
    def __init__(self, value: str = "https://example.com/file") -> None:
        self._value = value

    def toString(self) -> str:
        return self._value


class _FakeDownload:
    def __init__(self, filename: str, directory: str, url: _FakeUrl) -> None:
        self._filename = filename
        self._directory = directory
        self._url = url

    def downloadFileName(self) -> str:
        return self._filename

    def downloadDirectory(self) -> str:
        return self._directory

    def downloadUrl(self) -> _FakeUrl:
        return self._url


class _FakeTabWidget:
    def __init__(self, url: _FakeUrl) -> None:
        self._url = url
        self.download_dir: str | None = None

    def url(self) -> _FakeUrl:
        return self._url

    def setDownloadDirectory(self, value: str) -> None:
        self.download_dir = value


class _FakeTabs:
    def __init__(self, widgets: list[object]) -> None:
        self.widgets = widgets
        self.removed_indexes: list[int] = []
        self.current_indexes: list[int] = []

    def count(self) -> int:
        return len(self.widgets)

    def widget(self, index: int):
        return self.widgets[index]

    def setCurrentIndex(self, index: int) -> None:
        self.current_indexes.append(index)

    def removeTab(self, index: int) -> None:
        self.removed_indexes.append(index)


def _build_web_stub():
    web = web_module.Web.__new__(web_module.Web)
    web.ui = types.SimpleNamespace(
        start_acquisition_button=_Toggle(),
        stop_acquisition_button=_Toggle(),
        right_buttons_container=_Toggle(),
        screenshot_visible_area_button=_Toggle(),
        screenshot_selected_area_button=_Toggle(),
        screenshot_full_page_button=_Toggle(),
        back_button=_Toggle(),
        forward_button=_Toggle(),
        reload_button=_Toggle(),
        home_button=_Toggle(),
        url_line_edit=_Toggle(),
        stop_button=_Toggle(),
    )
    web._Scraper__acquisition = types.SimpleNamespace(
        progress_bar=_ProgressBar(),
        status_bar=_StatusBar(),
    )
    web._Web__translations = {"DOWNLOADED": "Downloaded"}
    web._Web__download_progress_debug_last = -1
    web.set_enabled_calls = []
    web.setEnabled = lambda value: web.set_enabled_calls.append(value)
    web._reset_acquisition_indicators_calls = []
    web._reset_acquisition_indicators = (
        lambda value: web._reset_acquisition_indicators_calls.append(value)
    )
    return web


@pytest.mark.unit
def test_enable_all_for_unstarted() -> None:
    web = _build_web_stub()
    web.acquisition_status = web_module.AcquisitionStatus.UNSTARTED
    web._Web__enable_all()
    assert web.ui.screenshot_visible_area_button.enabled is False
    assert web.ui.back_button.enabled is True
    assert web.ui.right_buttons_container.enabled is True
    assert web.ui.start_acquisition_button.enabled is True
    assert web.ui.stop_acquisition_button.enabled is False
    assert web.set_enabled_calls[-1] is True


@pytest.mark.unit
def test_enable_all_for_started() -> None:
    web = _build_web_stub()
    web.acquisition_status = web_module.AcquisitionStatus.STARTED
    web._Web__enable_all()
    assert web.ui.screenshot_visible_area_button.enabled is True
    assert web.ui.right_buttons_container.enabled is False
    assert web.ui.start_acquisition_button.enabled is False
    assert web.ui.stop_acquisition_button.enabled is True
    assert web.set_enabled_calls[-1] is True


@pytest.mark.unit
def test_enable_all_for_stopped() -> None:
    web = _build_web_stub()
    web.acquisition_status = web_module.AcquisitionStatus.STOPPED
    web._Web__enable_all()
    assert web.ui.right_buttons_container.enabled is False
    assert web.ui.start_acquisition_button.enabled is False
    assert web.ui.stop_acquisition_button.enabled is False
    assert web.set_enabled_calls[-1] is False


@pytest.mark.unit
def test_configure_os_proxy_fails_without_manager(monkeypatch: pytest.MonkeyPatch) -> None:
    web = _build_web_stub()
    web.proxy_manager = None
    web.proxy_state = None
    monkeypatch.setattr(web_module, "get_proxy_manager", lambda: None)
    assert web._Web__configure_os_proxy() is False


@pytest.mark.unit
def test_configure_os_proxy_fails_when_snapshot_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    web = _build_web_stub()
    manager = types.SimpleNamespace(
        snapshot=lambda: None,
        enable_capture_proxy=lambda host, port: None,
    )
    web.proxy_manager = manager
    web.proxy_state = None
    assert web._Web__configure_os_proxy() is False
    assert web.proxy_manager is None


@pytest.mark.unit
def test_configure_os_proxy_fails_when_port_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    web = _build_web_stub()
    manager = types.SimpleNamespace(
        snapshot=lambda: object(),
        enable_capture_proxy=lambda host, port: None,
    )
    web.proxy_manager = manager
    web.proxy_state = None
    monkeypatch.delenv("FIT_MITM_PORT", raising=False)
    assert web._Web__configure_os_proxy() is False


@pytest.mark.unit
def test_configure_os_proxy_fails_when_port_invalid(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    web = _build_web_stub()
    manager = types.SimpleNamespace(
        snapshot=lambda: object(),
        enable_capture_proxy=lambda host, port: None,
    )
    web.proxy_manager = manager
    web.proxy_state = None
    monkeypatch.setenv("FIT_MITM_PORT", "abc")
    assert web._Web__configure_os_proxy() is False


@pytest.mark.unit
def test_configure_os_proxy_success(monkeypatch: pytest.MonkeyPatch) -> None:
    web = _build_web_stub()
    called: dict[str, object] = {}
    snapshot_state = object()

    def _enable_capture_proxy(host: str, port: int) -> None:
        called["host"] = host
        called["port"] = port

    manager = types.SimpleNamespace(
        snapshot=lambda: snapshot_state,
        enable_capture_proxy=_enable_capture_proxy,
    )
    web.proxy_manager = manager
    web.proxy_state = None
    monkeypatch.setenv("FIT_MITM_PORT", "9090")
    assert web._Web__configure_os_proxy() is True
    assert web.proxy_state is snapshot_state
    assert called == {"host": "127.0.0.1", "port": 9090}


@pytest.mark.unit
def test_restore_os_proxy_calls_restore_and_resets_state() -> None:
    web = _build_web_stub()
    called: list[object] = []
    state = object()
    web.proxy_state = state
    web.proxy_manager = types.SimpleNamespace(restore=lambda s: called.append(s))
    assert web._Web__restore_os_proxy() is True
    assert called == [state]
    assert web.proxy_manager is None
    assert web.proxy_state is None


@pytest.mark.unit
def test_restore_os_proxy_fails_without_restore_method() -> None:
    web = _build_web_stub()
    web.proxy_state = object()
    web.proxy_manager = object()
    assert web._Web__restore_os_proxy() is False


@pytest.mark.unit
def test_start_stop_mitm_capture_wrappers() -> None:
    web = _build_web_stub()
    web.mitm_runner = types.SimpleNamespace(
        start_capture=lambda: True,
        stop_capture=lambda: True,
    )
    assert web._Web__start_mitm_capture() is True
    assert web._Web__stop_mitm_capture() is True


@pytest.mark.unit
def test_download_item_started_resets_indicators() -> None:
    web = _build_web_stub()
    web._Web__handle_download_item_started("file.pdf", "/tmp")
    assert web._reset_acquisition_indicators_calls == [True]
    assert web._Web__download_progress_debug_last == -1


@pytest.mark.unit
def test_download_item_progress_sets_progress_bar_value() -> None:
    web = _build_web_stub()
    web._Web__handle_download_item_progress(25, 100)
    assert web.acquisition.progress_bar.values[-1] == 25
    assert web._Web__download_progress_debug_last == 25


@pytest.mark.unit
def test_download_item_progress_unknown_total() -> None:
    web = _build_web_stub()
    web._Web__handle_download_item_progress(11, 0)
    assert web._Web__download_progress_debug_last == -2


@pytest.mark.unit
def test_handle_download_item_finished_updates_status_and_closes_tab(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    web = _build_web_stub()
    url = _FakeUrl("https://example.com/download")
    tabs = _FakeTabs([_FakeTabWidget(url)])
    web.ui.tabs = tabs

    monkeypatch.setattr(web_module.QtCore.QEventLoop, "exec", lambda self: 0)
    monkeypatch.setattr(web_module.QtCore.QTimer, "singleShot", lambda _ms, fn: fn())

    download = _FakeDownload("out.pdf", str(tmp_path), url)
    web._Web__handle_download_item_finished(download)
    assert tabs.removed_indexes == [0]
    assert web.acquisition.progress_bar.values[-1] == 100
    assert "Downloaded:" in web.acquisition.status_bar.text
    assert web._reset_acquisition_indicators_calls[-1] is False


@pytest.mark.unit
def test_restore_default_download_directory() -> None:
    web = _build_web_stub()
    web._Web__default_download_directory = "/tmp/downloads"
    tabs = _FakeTabs([_FakeTabWidget(_FakeUrl()), object(), _FakeTabWidget(_FakeUrl())])
    web.ui.tabs = tabs
    web._Web__restore_default_download_directory()
    assert tabs.widgets[0].download_dir == "/tmp/downloads"
    assert tabs.widgets[2].download_dir == "/tmp/downloads"
