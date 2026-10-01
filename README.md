# space

Encrypted Spaces 0.12.10 source code and Apple Silicon Mac installer.

## Contents

- `encrypted/Spaces-0.12.10-source-and-installer.zip.enc`: AES-256-GCM encrypted package, stored with Git LFS.
- `encrypted/verification.json`: file size and SHA-256 checksums.
- `tools/archive-crypto.py`: local encryption and decryption utility.

The package includes source code, the latest installer, agent prompts, bundled skills, and the library initialization code. It does not include personal chats, project data, MCP credentials, Kiro sign-in, or the encryption key.

## Download

Install Git LFS, then clone this repository:

```sh
git clone https://github.com/adronamraju/space.git
cd space
git lfs pull
```

Check that the downloaded encrypted file has the size and SHA-256 checksum recorded in `encrypted/verification.json`.

## Decrypt

You need the original 256-bit hexadecimal key file. Obtain it separately from the package owner. Never commit or upload it to this repository.

The utility requires Python 3 and the `cryptography` package:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install cryptography
.venv/bin/python tools/archive-crypto.py decrypt \
  --key-file /path/to/encryption-key.hex \
  --input encrypted/Spaces-0.12.10-source-and-installer.zip.enc \
  --output Spaces-0.12.10-source-and-installer.zip
```

The utility verifies authentication before making the decrypted ZIP available. It will not overwrite an existing output file. The package cannot be recovered without its key.

Extract the ZIP, then open `spaces-app/dist/Spaces-0.12.10-arm64.dmg` to install Spaces. The app creates its basic library in `~/Documents/Spaces` on first launch. Each new space gets its own memory, notes, chats, artifacts, and work folders. Existing libraries are retained. Install and sign in to Kiro CLI separately.

## Encryption format

AES-256-GCM with a random 12-byte nonce and a 16-byte authentication tag. Header: ASCII `SPACESENC`, version byte `01`, then the nonce. The complete 22-byte header is authenticated. Ciphertext follows, with the tag at the end. ZIP contents and internal filenames are encrypted; the outer package name and file size remain visible.

## 0.12.10 Desktop PATH recovery

- On macOS and Linux, read the interactive login shell's PATH once, with a two-second limit. Ignore startup chatter and import only PATH. Cache failures and fall back to common tool locations.
- Include pyenv, asdf, mise, Cargo, local-bin, and Homebrew locations. Preserve the app's existing PATH priority and per-process environment values.
- Use the same environment for Kiro lookup, version/sign-in checks, ACP chats, MCP discovery, and MCP installation. Restart Spaces after changing login shell PATH settings.
- Windows uses its native PATH and does not run a Unix shell.
- Retain existing exact-ID access defaults, migrations, and custom restrictions. The separate Space guide wildcard change described on the other computer is a local configuration edit, not a universal migration.

Validation: 149 automated tests. New tests use a minimal desktop PATH, real zsh startup with fixture uvx/npx launchers, Kiro lookup and subprocess checks, fallback behavior, and preservation of custom access. The packaged app was tested with the official Filesystem MCP server using a minimal PATH. Atlassian access on another computer and Windows runtime behavior have not been verified here.

## Build for Windows

After decrypting and extracting the source, install Node.js 22.13 or newer on a Windows PC. In PowerShell, open the `spaces-app` folder and run:

```powershell
npm ci
npm run dist:win -- --x64
```

Use `--arm64` for Windows ARM. The NSIS installer is written to `dist`. Install and sign in to Kiro CLI separately. Windows builds and runtime behavior have not been tested; the bundled installer is for Apple Silicon Macs.
