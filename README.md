# fit-web

Web scraping module for the **FIT Project**, built using [PySide6](https://doc.qt.io/qtforpython/).  
Provides PySide6-based UI flows and utilities to acquire web content (pages and dynamic feeds), integrating with FIT’s shared components.

---

## 🔐 Forensic design note

> **Note (v3):** `sslkey.log` is no longer generated as part of the acquisition artifacts.  
> See `docs/forensics/sslkey_log_forensic_reasoning_EN.md` for the forensic rationale.

---

## 🔗 Related FIT components

This package is designed to work alongside other FIT modules:

- [`fit-scraper`](https://github.com/fit-project/fit-scraper) – Base utilities and orchestration for acquisition

---

## 🐍 Dependencies

Main dependencies:

- Python `>=3.11,<3.13`
- [PySide6](https://pypi.org/project/PySide6/)

See `pyproject.toml` for the full list and version constraints.

---

## 📦 Installation

Install with [Poetry](https://python-poetry.org/):

```bash
poetry install
```

## Contributing
1. Fork this repository.  
2. Create a new branch (`git checkout -b feat/my-feature`).  
3. Commit your changes using [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).  
4. Submit a Pull Request describing your modification.

---
