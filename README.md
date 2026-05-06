# Obscura OS

Obscura OS is a Debian-based live/installable operating system designed for one purpose: running as a full-time I2P node and user environment where ordinary applications cannot access the clearnet directly.

The design goal is simple:

- The I2P router may reach the public internet as the underlay it needs to participate in the I2P network.
- User applications are confined to local I2P services and proxies.
- DNS, direct browser traffic, Tor, outproxies, and ordinary clearnet workflows are blocked by default.

> Status: early public build system. Treat generated images as developer previews until the firewall, browser profile, and install path have been independently audited.

## Editions

- `desktop`: XFCE, Firefox ESR locked to I2P proxy, Java I2P, I2PSnark, local eepsite hosting, HexChat.
- `core`: planned headless node image.

## Quick Build

Build on Debian 13 "trixie" or in a clean Debian VM:

```bash
sudo apt update
sudo apt install live-build debootstrap squashfs-tools xorriso isolinux syslinux-common grub-pc-bin grub-efi-amd64-bin mtools
sudo ./scripts/build-iso.sh
```

The ISO will be created in the repository root as a `*.iso` file.

## GitHub Release Builds

This repository includes a GitHub Actions workflow at `.github/workflows/build-iso.yml`.

When pushed to GitHub:

1. Open the repository on GitHub.
2. Go to **Actions**.
3. Run **Build Obscura OS ISO** manually, or push a tag like `v0.1.0`.
4. Download the ISO from the workflow artifacts.
5. For tags, the workflow also creates a GitHub Release and attaches the ISO plus checksums.

## Security Model

Obscura OS uses `nftables` default-deny outbound filtering. Only the dedicated `i2psvc` account is allowed to initiate outbound TCP/UDP connections. User applications must use local I2P services:

- I2P router console: `http://127.0.0.1:7657/`
- I2P HTTP proxy: `127.0.0.1:4444`
- I2P HTTPS proxy: `127.0.0.1:4445`
- I2P IRC tunnel: `127.0.0.1:6668`
- Local eepsite backend: `127.0.0.1:8080`

IPv6 and DNS are blocked by default in the live image.

## Important Limitations

- I2P itself requires underlay network access to other I2P routers. Obscura OS therefore allows only the I2P service user to use the underlay.
- Debian package updates are not enabled as a normal desktop workflow in lockdown mode. Use signed ISO updates or a deliberately audited maintenance mode.
- No anonymity system can protect against unsafe user behavior, browser exploits, malicious downloads, or application misconfiguration.

## Repository Layout

```text
config/                  live-build configuration
config/includes.chroot/  files copied into the live system
config/package-lists/    Debian package lists
scripts/                 build and verification helpers
docs/                    architecture and operating notes
.github/workflows/       ISO build and release automation
```

## Branding

Name: **Obscura OS**

Tagline: **Live Inside I2P**

Obscura OS is intended to feel calm, serious, and infrastructure-minded: a private network appliance that ordinary people can boot, run, and contribute back to I2P.
