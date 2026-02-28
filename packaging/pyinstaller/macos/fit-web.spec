import os
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

SPEC_DIR = Path(globals().get("SPECPATH", Path.cwd())).resolve()
REPO_ROOT = SPEC_DIR.parent.parent.parent

version_value = os.environ.get("FIT_BUILD_VERSION")
if not version_value:
    raise RuntimeError(
        "FIT_BUILD_VERSION is required (example: FIT_BUILD_VERSION=1.0.0)."
    )
version_file_path = REPO_ROOT / "_version.py"
version_file_path.write_text(f'__version__ = "{version_value}"\n', encoding="utf-8")

datas = [(str(REPO_ROOT / "icon.ico"), ".")]
datas += collect_data_files("fit_web", includes=["lang/*.json", "ui/**/*"])
datas.append(
    (
        str(REPO_ROOT / "fit_web" / "mitmproxy" / "addons" / "fit_capture.py"),
        "fit_web/mitmproxy/addons",
    )
)
datas += collect_data_files("fit_assets")
datas += collect_data_files("fit_common", includes=["lang/*.json"])
datas += collect_data_files("fit_cases", includes=["lang/*.json"])
datas += collect_data_files("fit_configurations", includes=["lang/*.json"])
datas += collect_data_files("fit_acquisition", includes=["lang/*.json"])
datas += collect_data_files("fit_scraper", includes=["lang/*.json"])
datas += collect_data_files("fit_bootstrap", includes=["lang/*.json"])
datas += collect_data_files("fit_verify_pdf_timestamp", includes=["lang/*.json"])
datas += collect_data_files("fit_verify_pec", includes=["lang/*.json"])
datas += collect_data_files("fit_bootstrap", includes=["macos/askpass.sh"])
datas += collect_data_files("fit_bootstrap", includes=["ffmpeg_binaries/macos_arm64/ffmpeg"])
datas += collect_data_files("whois", includes=["data/public_suffix_list.dat"])
datas.append((str(version_file_path), "."))

hiddenimports = []
hiddenimports += collect_submodules("fit_configurations.view.tabs")
hiddenimports += collect_submodules("fit_acquisition.tasks")
hiddenimports += collect_submodules("fit_web.tasks")
hiddenimports += collect_submodules("xhtml2pdf")
hiddenimports += collect_submodules("fit_bootstrap")
hiddenimports += collect_submodules("fit_verify_pec")
hiddenimports += collect_submodules("fit_verify_pdf_timestamp")
hiddenimports += collect_submodules("wacz")
hiddenimports += [
    "fit_web.mitmproxy.addons.fit_capture",
    "fit_webview_bridge",
    "fit_bootstrap.macos.askpass_dialog",
    "fit_bootstrap.macos.ui_askpass_dialog",
]

a = Analysis(
    [str(REPO_ROOT / "main.py")],
    pathex=[str(REPO_ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[str(REPO_ROOT / "packaging" / "pyinstaller" / "hooks")],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="fit-web",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[str(REPO_ROOT / "icon.ico")],
)
app = BUNDLE(
    exe,
    name="FitWeb.app",
    icon=str(REPO_ROOT / "packaging" / "icon.icns"),
    bundle_identifier="org.fit-project.fit.web",
    version=version_value,
)

if version_file_path.exists():
    try:
        version_file_path.unlink()
    except OSError:
        pass
