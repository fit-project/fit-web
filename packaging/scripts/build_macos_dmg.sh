#!/usr/bin/env bash
set -euo pipefail

if [[ "${OSTYPE:-}" != darwin* ]]; then
  echo "This script must run on macOS."
  exit 1
fi

APP_PATH="${1:-dist/FitWeb.app}"
VERSION="${2:-}"
OUT_DIR="${3:-dist/dmg}"

if [[ -z "${VERSION}" ]]; then
  VERSION="$(python - <<'PY'
from fit_common.core import get_version
print(get_version())
PY
)"
fi

if [[ ! -d "${APP_PATH}" ]]; then
  echo "App bundle not found: ${APP_PATH}"
  exit 1
fi

ARCH="$(uname -m)"
DMG_NAME="fit-web-portable-${VERSION}-macos-${ARCH}.dmg"
DMG_PATH="${OUT_DIR}/${DMG_NAME}"
RW_DMG_PATH="${OUT_DIR}/fit-web-rw-${VERSION}.dmg"
VOL_NAME="FitWeb"
MOUNT_POINT="/Volumes/${VOL_NAME}"

APP_SIZE_KB="$(du -sk "${APP_PATH}" | awk '{print $1}')"
# Add generous overhead to avoid "No space left on device" during copy.
DMG_SIZE_MB="$(( (APP_SIZE_KB / 1024) + 300 ))"

DEV_NODE=""
cleanup() {
  if [[ -n "${DEV_NODE}" ]]; then
    hdiutil detach "${DEV_NODE}" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

mkdir -p "${OUT_DIR}"

if [[ -f "${DMG_PATH}" ]]; then
  rm -f "${DMG_PATH}"
fi

if [[ -f "${RW_DMG_PATH}" ]]; then
  rm -f "${RW_DMG_PATH}"
fi

hdiutil create \
  -size "${DMG_SIZE_MB}m" \
  -fs HFS+ \
  -volname "${VOL_NAME}" \
  -ov \
  "${RW_DMG_PATH}"

if [[ -d "${MOUNT_POINT}" ]]; then
  hdiutil detach "${MOUNT_POINT}" >/dev/null 2>&1 || true
fi

DEV_NODE="$(hdiutil attach -readwrite -noverify -noautoopen "${RW_DMG_PATH}" | awk '/\/Volumes\// {print $1; exit}')"
if [[ -z "${DEV_NODE}" ]]; then
  echo "Failed to attach temporary DMG."
  exit 1
fi

ditto "${APP_PATH}" "${MOUNT_POINT}/FitWeb.app"
ln -s /Applications "${MOUNT_POINT}/Applications" || true
sync
hdiutil detach "${DEV_NODE}"
DEV_NODE=""

hdiutil convert "${RW_DMG_PATH}" \
  -ov \
  -format UDZO \
  -o "${DMG_PATH}"

rm -f "${RW_DMG_PATH}"

echo "Created DMG: ${DMG_PATH}"
