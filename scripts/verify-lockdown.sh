#!/usr/bin/env bash
set -euo pipefail

echo "[obscura] checking nftables rules"
nft list ruleset | grep -q "table inet obscura"
nft list ruleset | grep -q 'meta skuid "i2psvc" tcp accept'
nft list ruleset | grep -q 'udp dport 53 drop'

echo "[obscura] checking IPv6 sysctl"
sysctl net.ipv6.conf.all.disable_ipv6 | grep -q '= 1'

echo "[obscura] checking Firefox policy"
test -f /usr/lib/firefox-esr/distribution/policies.json
grep -q '127.0.0.1' /usr/lib/firefox-esr/distribution/policies.json
grep -q '4444' /usr/lib/firefox-esr/distribution/policies.json

echo "[obscura] lockdown checks passed"

