# space

Encrypted Spaces 0.12.8 source code and Apple Silicon Mac installer.

## Contents

- `encrypted/Spaces-0.12.8-source-and-installer.zip.enc`: AES-256-GCM encrypted package, stored with Git LFS.
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
  --input encrypted/Spaces-0.12.8-source-and-installer.zip.enc \
  --output Spaces-0.12.8-source-and-installer.zip
```

The utility verifies authentication before making the decrypted ZIP available. It will not overwrite an existing output file. The package cannot be recovered without its key.

Extract the ZIP, then open `spaces-app/dist/Spaces-0.12.8-arm64.dmg` to install Spaces. The app creates its basic library in `~/Documents/Spaces` on first launch. Each new space gets its own memory, notes, chats, artifacts, and work folders. Existing libraries are retained. Install and sign in to Kiro CLI separately.

## Encryption format

AES-256-GCM with a random 12-byte nonce and a 16-byte authentication tag. Header: ASCII `SPACESENC`, version byte `01`, then the nonce. The complete 22-byte header is authenticated. Ciphertext follows, with the tag at the end. ZIP contents and internal filenames are encrypted; the outer package name and file size remain visible.

## 0.12.8 Tools in existing chats

- Existing chats start a new Kiro session when their effective MCP servers or tool permissions change. Older sessions without a saved configuration hash refresh once.
- The same local chat retains its visible history, selected model, approval setting, and saved work plans. Unchanged configurations can resume their existing Kiro session.
- The next message includes saved work state and bounded recent conversation text. Full historical model context and earlier image data are not transferred. Pending context survives restart and failed or cancelled turns.
- Use **Details → Refresh tools** in a chat to request a fresh Kiro session manually. Active work must finish first. Server startup or sign-in can still be required.
- Exact per-agent tool grants remain in force. Refresh does not grant additional access.

Validation: 138 automated tests. A test using the packaged app with Kiro CLI 2.25.0 added the official Filesystem MCP server after opening a chat. The chat received a new session, and its agent used the external read tool to retrieve a generated test file. The Refresh tools control was checked in the browser preview. Windows execution has not been tested.

## Build for Windows

After decrypting and extracting the source, install Node.js 22.13 or newer on a Windows PC. In PowerShell, open the `spaces-app` folder and run:

```powershell
npm ci
npm run dist:win -- --x64
```

Use `--arm64` for Windows ARM. The NSIS installer is written to `dist`. Install and sign in to Kiro CLI separately. Windows builds and runtime behavior have not been tested; the bundled installer is for Apple Silicon Macs.
