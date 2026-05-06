#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "Please run with sudo: sudo ./scripts/build-iso.sh" >&2
  exit 1
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

lb clean

lb config \
  --mode debian \
  --distribution trixie \
  --archive-areas "main contrib non-free-firmware" \
  --architectures amd64 \
  --mirror-bootstrap "http://deb.debian.org/debian/" \
  --mirror-chroot "http://deb.debian.org/debian/" \
  --mirror-binary "http://deb.debian.org/debian/" \
  --security false \
  --binary-images iso-hybrid \
  --debian-installer live \
  --bootappend-live "boot=live components quiet apparmor=1 security=apparmor"

lb build 2>&1 | tee obscura-build.log

ISO="$(find . -maxdepth 1 -name 'live-image-*.iso' -o -name 'live-image-*.hybrid.iso' | head -n 1)"
if [[ -n "${ISO}" && -f "${ISO}" ]]; then
  OUT="obscura-os-desktop-amd64.iso"
  mv -f "${ISO}" "${OUT}"
  sha256sum "${OUT}" > "${OUT}.sha256"
  echo "Built ${OUT}"
  cat "${OUT}.sha256"
else
  echo "Build completed, but no ISO was found." >&2
  exit 1
fi
