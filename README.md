# space

Encrypted Spaces 0.12.4 source code and Apple Silicon Mac installer.

## Contents

- `encrypted/Spaces-0.12.4-source-and-installer.zip.enc`: AES-256-GCM encrypted package, stored with Git LFS.
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
  --input encrypted/Spaces-0.12.4-source-and-installer.zip.enc \
  --output Spaces-0.12.4-source-and-installer.zip
```

The utility verifies authentication before making the decrypted ZIP available. It will not overwrite an existing output file. The package cannot be recovered without its key.

Extract the ZIP, then open `spaces-app/dist/Spaces-0.12.4-arm64.dmg` to install Spaces. The app creates its basic library in `~/Documents/Spaces` on first launch. Each new space gets its own memory, notes, chats, artifacts, and work folders. Existing libraries are retained. Install and sign in to Kiro CLI separately.

## Encryption format

AES-256-GCM with a random 12-byte nonce and a 16-byte authentication tag. Header: ASCII `SPACESENC`, version byte `01`, then the nonce. The complete 22-byte header is authenticated. Ciphertext follows, with the tag at the end. ZIP contents and internal filenames are encrypted; the outer package name and file size remain visible.

## 0.12.4 Kiro MCP discovery and CLI setup

- Spaces automatically reads Kiro's global MCP configuration and the selected space's Kiro MCP configuration.
- Settings shows configured servers and their source. There are no built-in GitLab or Atlassian cards.
- **Add server → CLI** runs a `kiro-cli mcp add` command. Form and JSON options register servers through Kiro CLI import.
- **Edit** saves a Kiro server back to its original scope. Existing Spaces-only entries remain available.
- Same-name Spaces entries take precedence. Disabled servers remain disabled. Agent access can be restricted.
- A changed Kiro configuration reloads on the next idle chat connection without creating a new Spaces chat. Active work is retained.

After updating, open Settings. Existing Kiro servers should appear. Use **Refresh** after adding a server from another terminal. Registration does not install every runtime dependency; local commands still need their runtime, and services can require account sign-in.

Validation: 114 automated tests, browser inspection of the vendor-neutral settings and CLI input, real Kiro CLI registration followed by discovery and MCP startup in an isolated workspace, and a packaged Electron MCP check. Personal Kiro settings were not changed by these checks.
