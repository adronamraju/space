# space

Encrypted Spaces 0.13.0 source code and Apple Silicon Mac installer.

## Contents

- `encrypted/Spaces-0.13.0-source-and-installer.zip.enc`: AES-256-GCM encrypted package, stored with Git LFS.
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
  --input encrypted/Spaces-0.13.0-source-and-installer.zip.enc \
  --output Spaces-0.13.0-source-and-installer.zip
```

The utility verifies authentication before making the decrypted ZIP available. It will not overwrite an existing output file. The package cannot be recovered without its key.

Extract the ZIP, then open `spaces-app/dist/Spaces-0.13.0-arm64.dmg` to install Spaces. The app creates its basic library in `~/Documents/Spaces` on first launch. Each new space gets its own memory, notes, chats, artifacts, and work folders. Existing libraries are retained. Install and sign in to Kiro CLI separately.

## Encryption format

AES-256-GCM with a random 12-byte nonce and a 16-byte authentication tag. Header: ASCII `SPACESENC`, version byte `01`, then the nonce. The complete 22-byte header is authenticated. Ciphertext follows, with the tag at the end. ZIP contents and internal filenames are encrypted; the outer package name and file size remain visible.

## 0.13.0 Product Owner review views

- Add the briefing-led Overview, attention items, recent outputs, and saved work layout.
- Add a searchable artifact table with author and type filters.
- Open saved discovery, backlog, delivery, briefing, and meeting reviews as full pages with evidence and related work.
- Add full-page priority comparison with the existing saved proposal editor.
- Add a workflow picker in chat, including six Product Owner workflows.
- Add a Kiro Spec review panel for checks, open questions, and story mappings.
- Review the selected revision and complete description before creating a Jira story.
- Resolve Jira availability through the backend, including inherited Kiro MCP servers and per-agent access.
- Preserve existing libraries and retain MCP-aware role delegation from 0.12.13.

Validation: 171 automated tests passed. The running Electron app was checked using an isolated test library. Packaged view files match the source, the DMG checksum is valid, and the encrypted archive was decrypted and compared with the source ZIP. No company Jira writes were performed. The Mac installer is not developer-signed or notarized. Windows runtime behavior remains untested.

These are working desktop views. No sample project data is installed. Older prose-only chats are not automatically converted into review records; run a workflow to create a structured review.

## Build for Windows

After decrypting and extracting the source, install Node.js 22.13 or newer on a Windows PC. In PowerShell, open the `spaces-app` folder and run:

```powershell
npm ci
npm run dist:win -- --x64
```

Use `--arm64` for Windows ARM. The NSIS installer is written to `dist`. Install and sign in to Kiro CLI separately. Windows builds and runtime behavior have not been tested; the bundled installer is for Apple Silicon Macs.
