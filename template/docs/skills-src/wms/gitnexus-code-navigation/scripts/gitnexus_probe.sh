#!/usr/bin/env bash
set -euo pipefail

if ! command -v npx >/dev/null 2>&1; then
  echo "[ERROR] npx is required to run GitNexus."
  exit 1
fi

status_output="$(npx gitnexus status 2>&1 || true)"
printf '%s\n' "${status_output}"

if printf '%s' "${status_output}" | grep -Eqi 'stale|not indexed|run: .*analyze'; then
  echo "[WARN] GitNexus index is not ready. Run: npx gitnexus analyze"
fi
