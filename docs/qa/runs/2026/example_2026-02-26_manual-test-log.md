# Manual Test Run Log - fit-web

- Run ID: `2026-02-26_manual-test`
- Build/Tag:
- Date: `2026-02-26`
- Tester:
- Environment:

## Results

| Test ID | Result | Notes |
|---------|--------|-------|
| MTP-001 | PASS   | App starts correctly, case selection dialog works, navigation (back/forward/reload/home) works on `https://example.com`. |
| MTP-002 | PASS   | Start/stop acquisition completed successfully, acquisition folder created with expected outputs. |
| MTP-003 | FAIL   | Clicking **Verify timestamp** raised a missing resource error in bundle (`fit_verify_pdf_timestamp/lang/en.json`). |

## Issues Found

1. Missing bundled language resources for verify modules:
   - `fit_verify_pdf_timestamp/lang/en.json`
   - `fit_verify_pec/lang/en.json`
   Impact: opening verification dialogs caused runtime crashes in the frozen app.
2. Missing `fit_bootstrap/macos/askpass.sh` in early bundle iteration.
   Impact: elevation flow failed with `sudo: no askpass program specified`.

## Retest

- Retest Build/Tag: `v1.0.0-rc2`
- Retest Date: `2026-02-26`
- Retest Outcome:
  - MTP-003: PASS after rebuilding bundle with missing language files included in PyInstaller datas.
  - No crash observed when opening **Verify timestamp** and **Verify PEC** dialogs.

## Final Assessment

- Release readiness: `READY FOR RELEASE CANDIDATE`
- Blocking issues: `NONE`
