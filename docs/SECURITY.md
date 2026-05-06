# Security Notes

Obscura OS is designed to reduce accidental clearnet leaks. It is not a guarantee of anonymity against malware, browser exploits, physical compromise, unsafe downloads, or user mistakes.

## Current Controls

- `nftables` default-deny input, forward, and output.
- Only `i2psvc` can initiate outbound TCP/UDP traffic.
- Direct DNS is blocked.
- IPv6 is disabled.
- AppArmor is enabled.
- Browser policy locks Firefox ESR to I2P proxy ports.
- MAC randomization is enabled through NetworkManager.
- Nginx eepsite backend listens only on loopback.

## Audit Priorities

1. Confirm Java I2P runs under the intended service account on every boot path.
2. Confirm live-build package scripts do not re-enable unwanted services.
3. Test browser DNS and WebRTC behavior.
4. Test installed-system behavior, not only live boot behavior.
5. Verify no package manager GUI or updater can bypass the network policy.
6. Review I2P outproxy defaults and disable them in the shipped profile.

## Manual Leak Tests

From a normal user:

```bash
curl https://example.com
dig example.com
nc -vz 1.1.1.1 443
```

These should fail.

From the I2P service user:

```bash
sudo -u i2psvc curl --connect-timeout 5 https://i2p.net/
```

This may succeed because the I2P router account is allowed underlay access.
