# Manual Test Plan - fit-web

## Scope

This checklist is used for:
- release validation (for example `v1.0.0`)
- regression testing after changes
- manual validation of new features

## Test Environment

- Build type: local bundle or CI release package
- Network: internet connection available
- Test case available in FIT (valid case selected at startup)

## OS-specific Prerequisites

### macOS

**Installation / Setup**
1. Download the `.dmg` file from GitHub, or build it locally.
2. Open the `.dmg` file, then drag and drop `FitWeb.app` into the Applications folder.
3. Eject (unmount) and close the `.dmg`.

**Cleanup / Clean State**
1. Remove any existing `mitmproxy` certificate from system keychain/trust store.
2. Delete the `~/Library/Application Support/FIT` directory from the user profile.

### Windows

**Installation / Setup**
1. Use packaged installer/portable distribution for Windows.

**Cleanup / Clean State**
1. Remove any existing `mitmproxy` certificate from Windows certificate store.
2. Delete the `%LOCALAPPDATA%\\FIT` directory from the user profile.

### Linux

**Installation / Setup**
1. Use packaged installer/portable distribution for Linux.

**Cleanup / Clean State**
1. Remove any existing `mitmproxy` certificate from Linux trust store.
2. Delete the `~/.local/share/FIT` directory from the user profile.

## Common Functional Tests

### MTP-000 - Startup without FIT network connectivity

**Goal**
- Verify that the app does not start without FIT network connectivity and exits after error acknowledgment.

**Steps**
1. Disconnect the workstation from the FIT network (or simulate FIT network unavailability).
2. Launch the app from the standard installation path for the current OS.
3. Wait for startup checks to complete.
4. In the connectivity error popup, click **OK**.

**Expected result**
- The app does not proceed to normal startup flow.
- An error popup is shown indicating FIT network connectivity is required.
- After clicking **OK**, the app closes.

### MTP-MAC-001 - Gatekeeper and quarantine removal on first launch

**Goal**
- Verify first-launch behavior when the app is quarantined and confirm unblocking flow.

**Steps**
1. Install `FitWeb.app` from `.dmg` on a clean macOS environment.
2. Ensure app quarantine attribute is present (fresh download path / first launch).
3. Launch `FitWeb.app` the first time.
4. If blocked by Gatekeeper, perform the expected unblocking flow from macOS security settings.
5. Re-launch the app.

**Expected result**
- On first launch, macOS may block the app due to Gatekeeper/quarantine.
- After unblocking/removing quarantine, the app launches correctly.
- Subsequent launches are not blocked again by the same Gatekeeper warning.

### MTP-MAC-002 - Screen recording permission flow

**Goal**
- Verify that screen recording permission is requested and required behavior is clear to the user.

**Steps**
1. Start from clean macOS privacy permissions (screen recording not granted for `FitWeb.app`).
2. Launch the app and trigger a workflow that requires screen recording access.
3. Observe permission request and grant screen recording permission in System Settings if prompted.
4. Re-launch the app if macOS requires restart of the app after permission grant.
5. Repeat the same workflow.

**Expected result**
- The app clearly prompts for screen recording permission when needed.
- Without permission, user receives a clear error/instruction and the feature cannot continue.
- After granting permission (and relaunching if required), the feature works as expected.

### MTP-001 - MITMPROXY certificate installation flow

**Goal**
- Verify certificate installation error handling and successful bootstrap behavior.

**Steps**
1. Launch the app from the standard installation path for the current OS with clean state (certificate removed).
2. At the first MITMPROXY certificate prompt, click **Cancel**.
3. Re-launch the app and repeat certificate installation with an invalid password.
4. Re-launch the app, enter the correct admin password at the first prompt, then click **Cancel** on the second trust-related password prompt.
5. Re-launch the app and complete both password prompts with valid credentials.

**Expected result**
- Case 1 (**Cancel** at first prompt): an error popup is shown stating FIT cannot run without the certificate.
- Case 2 (invalid password): the initial MITMPROXY certificate installation popup is shown again.
- Case 3 (**Cancel** at second trust prompt): an error popup is shown again stating FIT cannot run without the certificate.
- Case 4 (successful installation): bootstrap completes and `Select a valid case` prompt is shown.

### MTP-002 - Root privileges prompt flow

**Goal**
- Verify root privileges prompt behavior and bootstrap blocking conditions.

**Steps**
1. Launch the app from the standard installation path for the current OS.
2. At the root privileges prompt, click **Cancel**.
3. Re-launch the app and enter an invalid password in the root privileges prompt.
4. Re-launch the app and enter the correct root password.

**Expected result**
- Case 1 (**Cancel**): an error popup is shown stating FIT cannot run without root privileges.
- Case 2 (invalid password): the initial root privileges popup is shown again.
- Case 3 (valid password): `Select a valid case` prompt is shown.


### MTP-003 - Update Release Version

**Goal**
- Verify that the update flow works correctly.

**Steps**
1. Create a “fake” new release version (for example, from installed version 1.0.0 to fake version 1.0.1).
2. Launch the app from the standard installation path for the current OS.
3. Verify that a popup appears informing the user that a new version is available, with two options:  **Continue** or **Update**
4. First, choose **Continue**. Wait for the root privileges prompt, enter the password, select a case, and open FitWeb. Then close the app.
5. Re-launch the app, choose **Update**, wait for the download to complete, then click **Ok**

**Expected result**
- Case 1 (**Continue**): once FitWeb is open, check the current release shown in the bottom-right corner.
- Case 2 (**Update** + **Ok**): after installation is complete, wait for the root privileges prompt, enter the password, select a case, and open FitWeb. Check that the release in the bottom-right corner has changed.

### MTP-004 - App startup and basic navigation

**Goal**
- Verify that the app starts correctly and web navigation works after bootstrap.

**Steps**
1. Launch the app from the standard installation path for the current OS.
2. Complete bootstrap requirements and select a valid case when prompted.
3. Verify that, at first home page load, an acquisition warning popup is shown (FIT may capture HTTP/HTTPS traffic generated by other open windows/apps and they should be closed if not relevant).
4. Close the warning popup.
5. Open a website from the URL bar (for example `https://example.com`).
6. Use `back`, `forward`, `reload`, and `home`.

**Expected result**
- App starts without crashes.
- Main window is visible and interactive.
- Acquisition warning popup is shown on home page load with network traffic capture warning.
- Navigation buttons work as expected.

### MTP-005 - Acquisition start/stop baseline flow

**Goal**
- Verify core acquisition flow and artifact generation.

**Steps**
1. Open a target website.
2. Click **Start acquisition**.
3. Browse at least 2-3 pages on the same domain.
4. Click **Stop acquisition**.
5. Wait for post-acquisition tasks to complete.
6. Open the generated acquisition folder.

**Expected result**
- Start/stop flow completes without blocking errors.
- Acquisition folder is created under the selected case.
- Expected the below baseline artifacts are present check each one if is correct:
    - acquisition_page.png
    - acquisition_page.wacz
    - acquisition_report.pdf
    - acquisition_video.mp4
    - acquisition.hash
    - acquisition.log
    - acquisition.pcap
    - caseinfo.json
    - headers.txt
    - nslookup.txt
    - screenshot.zip
    - system_info.txt
    - timestamp.tsr
    - traceroute.txt
    - tsa.crt
    - whois.txt

### MTP-005 - Verify timestamp and PEC dialogs load correctly

**Goal**
- Ensure bundled modules `fit-verify-pdf-timestamp` and `fit-verify-pec` load in the app.

**Steps**
1. Open fit-web.
2. Click **Verify timestamp**.
3. Close dialog.
4. Click **Verify PEC**.
5. Close dialog.

**Expected result**
- Both dialogs open correctly.
- No missing-resource errors (for example missing `lang/*.json`).
- No runtime crash when opening/closing dialogs.

## macOS-Specific Functional Tests



## Execution Matrix

Mark each common test as executed on each OS.

| Test ID | macOS | Windows | Linux | Notes |
| --- | --- | --- | --- | --- |
| MTP-000 |  |  |  |  |
| MTP-001 |  |  |  |  |
| MTP-002 |  |  |  |  |
| MTP-003 |  |  |  |  |
| MTP-004 |  |  |  |  |
| MTP-005 |  |  |  |  |

## macOS-Specific Execution Matrix

Mark each macOS-only test as executed.

| Test ID | macOS | Notes |
| --- | --- | --- |
| MTP-MAC-001 |  |  |
| MTP-MAC-002 |  |  |

## Test Execution Log

Use this section to record each run:

- Build/Tag:
- Date:
- Tester:
- Result: PASS / FAIL
- Notes / Issues:
