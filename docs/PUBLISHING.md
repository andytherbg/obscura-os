# Publishing Obscura OS on GitHub

## One-Time Setup

Create a public GitHub repository named `obscura-os` under your account.

Then connect and push:

```bash
git remote add origin git@github.com:andytherbg/obscura-os.git
git branch -M main
git push -u origin main
```

## Build a Public ISO

On GitHub:

1. Open `Actions`.
2. Select `Build Obscura OS ISO`.
3. Click `Run workflow`.
4. Download the ISO artifact after the workflow completes.

## Create a Release

Tag locally:

```bash
git tag v0.1.0
git push origin v0.1.0
```

The workflow creates a GitHub Release and uploads:

- `obscura-os-desktop-amd64.iso`
- `obscura-os-desktop-amd64.iso.sha256`

## Recommended Release Warning

Use this wording for early releases:

> Developer preview. Do not rely on this build for high-risk anonymity. The firewall, browser profile, and install path need independent review.

