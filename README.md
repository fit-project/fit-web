# fit-web

Web scraping module for the **FIT Project**, built using [PySide6](https://doc.qt.io/qtforpython/).  
Provides PySide6-based UI flows and utilities to acquire web content (pages and dynamic feeds), integrating with FIT’s shared components.

---

## Release target

Current target: **`v1.0.0`**.

Scope of this first release:
- Support **only macOS** (not Windows/Linux yet).
- Publish a stable CI pipeline focused first on the **test chain** (`unit`, `contract`, `integration`, `e2e`).
- Use this validated baseline to open a dedicated development branch for future Windows/Linux support.

Roadmap:
- planned backend expansion to Windows and Linux

---

## Platform support

- Supported OS for `v1.0.0`: **macOS 11.3+**
- Not supported in `v1.0.0`: Windows, Linux

At runtime, the app enforces this constraint from `main.py` and exits on unsupported platforms.

---

## 🔐 Forensic design note

> **Note (v3):** `sslkey.log` is no longer generated as part of the acquisition artifacts.  
> See `docs/forensics/sslkey_log_forensic_reasoning_EN.md` for the forensic rationale.

---

## Dependencies

Main dependencies are:

- **Python** >=3.12,<3.14
- **Poetry** (recommended for development)
- [`fit-bootstrap`](https://github.com/fit-project/fit-bootstrap)  – preparing and validating the OS environment
- [`fit-scraper`](https://github.com/fit-project/fit-scraper) – Base utilities and orchestration for acquisition
- [`fit_verify_pdf_timestamp`](https://github.com/fit-project/fit-verify-pdf-timestamp) – Verifying the timestamp applied to the PDF report
- [`fit_verify_pec`](https://github.com/fit-project/fit_verify_pec) – Verifying the PEC applied sent during the acquisition process
- [`fit-webview-bridge`](https://github.com/fit-project/fit-webview-bridge) – OS native webview

See `pyproject.toml` for full details.

`fit-web` also depends on these FIT modules in the full ecosystem workflow:
- `fit-acquisition`
- `fit-assets`
- `fit-bootstrap`
- `fit-cases`
- `fit-common`
- `fit-configurations`
- `fit-scraper`
- `fit-verify-pdf-timestamp`
- `fit-verify-pec`
- `fit-webview-bridge`

Each module above has its own dedicated CI pipeline.
---

## Local checks (same as CI)

Run these commands before opening a PR, so failures are caught locally first.

### What each tool does
- `pytest`: runs automated tests (`unit`, `contract`, `integration` and `e2e` suites).
- `ruff`: checks code style and common static issues (lint).
- `mypy`: performs static type checking on annotated Python code.
- `bandit`: scans source code for common security anti-patterns.
- `pip-audit`: checks installed dependencies for known CVEs.

### 1) Base setup
```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install . pytest ruff mypy "bandit[toml]" pip-audit
python -m pip install --upgrade "setuptools"
```

### 2) Test suite
```bash
export QT_QPA_PLATFORM=offscreen

# unit tests
pytest -m unit -q tests

# contract tests
pytest -m contract -q tests

# integration tests
pytest -m integration -q tests

# end-to-end smoke tests
pytest -m e2e -q tests
```

CI priority for `v1.0.0` is this test chain.

### 3) Quality and security checks
```bash
ruff check fit_web tests
mypy fit_web
bandit -c pyproject.toml -r fit_web -q -ll -ii
PIPAPI_PYTHON_LOCATION="$(python -c 'import sys; print(sys.executable)')" \
  python -m pip_audit --progress-spinner off \
  --ignore-vuln CVE-2026-27205 \
  --ignore-vuln PYSEC-2024-60
```

Note: `pip-audit` may print skip messages for each package below because they are local packages and are not published on PyPI.
- `fit-acquisition`
- `fit-assets`
- `fit-bootstrap`
- `fit-cases`
- `fit-common`
- `fit-configurations`
- `fit-scraper`
- `fit-verify-pdf-timestamp`
- `fit-verify-pec`
- `fit-web`
 
Temporary security exceptions used by the command above:
- `CVE-2026-27205` (`flask`): currently blocked by `mitmproxy 12.2.1`, which requires `flask <= 3.1.2`.
- `PYSEC-2024-60` (`idna`): currently blocked by `wacz 0.5.0` -> `cdxj-indexer` requiring `idna < 3.0`.

---

## Installation

``` bash
    python3.12 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install poetry
    poetry lock
    poetry install
    poetry run python main.py
```

Note: for `v1.0.0`, installation and execution are supported only on macOS.

---

## Contributing
1. Fork this repository.  
2. Create a new branch (`git checkout -b feat/my-feature`).  
3. Commit your changes using [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).  
4. Submit a Pull Request describing your modification.
