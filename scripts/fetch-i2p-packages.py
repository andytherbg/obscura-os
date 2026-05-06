#!/usr/bin/env python3
"""Fetch official I2P packages for live-build's local package pool."""

from __future__ import annotations

import gzip
import hashlib
import pathlib
import shutil
import sys
import urllib.request


BASE_URL = "https://deb.i2p.net"
PACKAGES_URL = f"{BASE_URL}/dists/trixie/main/binary-amd64/Packages.gz"
OUTPUT_DIR = pathlib.Path("config/packages.chroot")
PACKAGE_NAMES = ("i2p", "i2p-router", "libjbigi-jni", "i2p-keyring")


def read_packages_index() -> list[dict[str, str]]:
    with urllib.request.urlopen(PACKAGES_URL, timeout=60) as response:
        raw = response.read()

    text = gzip.decompress(raw).decode("utf-8", errors="replace")
    records: list[dict[str, str]] = []

    for block in text.strip().split("\n\n"):
        record: dict[str, str] = {}
        current_key: str | None = None

        for line in block.splitlines():
            if line.startswith(" ") and current_key:
                record[current_key] += "\n" + line
                continue

            if ":" not in line:
                continue

            key, value = line.split(":", 1)
            current_key = key
            record[key] = value.strip()

        if record:
            records.append(record)

    return records


def package_map(records: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    selected: dict[str, dict[str, str]] = {}

    for record in records:
        name = record.get("Package")
        if name in PACKAGE_NAMES:
            selected[name] = record

    missing = sorted(set(PACKAGE_NAMES) - set(selected))
    if missing:
        raise SystemExit(f"Missing I2P packages in official repository: {', '.join(missing)}")

    return selected


def download_package(name: str, record: dict[str, str]) -> pathlib.Path:
    filename = record["Filename"]
    expected_sha256 = record["SHA256"]
    url = f"{BASE_URL}/{filename}"
    destination = OUTPUT_DIR / pathlib.Path(filename).name

    with urllib.request.urlopen(url, timeout=120) as response:
        data = response.read()

    actual_sha256 = hashlib.sha256(data).hexdigest()
    if actual_sha256 != expected_sha256:
        raise SystemExit(
            f"SHA256 mismatch for {name}: expected {expected_sha256}, got {actual_sha256}"
        )

    destination.write_bytes(data)
    return destination


def main() -> int:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    OUTPUT_DIR.mkdir(parents=True)
    packages = package_map(read_packages_index())

    for name in PACKAGE_NAMES:
        path = download_package(name, packages[name])
        print(f"Fetched {name}: {path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
