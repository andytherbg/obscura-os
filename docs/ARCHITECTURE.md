# Obscura OS Architecture

Obscura OS is a Debian 13 live/installable system dedicated to I2P.

## Trust Boundary

The system has two network classes:

- Underlay access: allowed only to the I2P router service account, `i2psvc`.
- User access: allowed only to local loopback services such as the I2P HTTP proxy, HTTPS proxy, router console, IRC tunnel, and eepsite backend.

This is enforced with `nftables`, not by asking each application to behave.

## Default Local Services

| Service | Address |
| --- | --- |
| I2P router console | `127.0.0.1:7657` |
| I2P HTTP proxy | `127.0.0.1:4444` |
| I2P HTTPS proxy | `127.0.0.1:4445` |
| I2P IRC tunnel | `127.0.0.1:6668` |
| Eepsite backend | `127.0.0.1:8080` |

## Desktop

The desktop edition uses XFCE and Firefox ESR. Firefox policies lock the browser to the local I2P proxy and disable telemetry, WebRTC, Firefox studies, Pocket, account sync, and ordinary keyword search.

## Eepsite Hosting

Nginx serves `/var/www/eepsite` on `127.0.0.1:8080`. I2P tunnel publication is managed from the I2P router console.

## Updates

Normal user applications cannot reach Debian repositories while lockdown is active. Production releases should use signed ISO updates or a carefully designed maintenance mode.

