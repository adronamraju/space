# space

Encrypted Spaces 0.12.3 source code and Apple Silicon Mac installer.

## Contents

- `encrypted/Spaces-0.12.3-source-and-installer.zip.enc`: AES-256-GCM encrypted package, stored with Git LFS.
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
  --input encrypted/Spaces-0.12.3-source-and-installer.zip.enc \
  --output Spaces-0.12.3-source-and-installer.zip
```

The utility verifies authentication before making the decrypted ZIP available. It will not overwrite an existing output file. The package cannot be recovered without its key.

Extract the ZIP, then open `spaces-app/dist/Spaces-0.12.3-arm64.dmg` to install Spaces. The app creates its basic library in `~/Documents/Spaces` on first launch. Each new space gets its own memory, notes, chats, artifacts, and work folders. Existing libraries are retained. Install and sign in to Kiro CLI separately.

## Encryption format

AES-256-GCM with a random 12-byte nonce and a 16-byte authentication tag. Header: ASCII `SPACESENC`, version byte `01`, then the nonce. The complete 22-byte header is authenticated. Ciphertext follows, with the tag at the end. ZIP contents and internal filenames are encrypted; the outer package name and file size remain visible.

## 0.12.3 simpler MCP settings

- GitLab and Atlassian appear as default setup cards with prefilled URLs.
- **Add server** accepts a remote URL, a local command, or complete `mcpServers` JSON.
- **Save server** applies the server and agent access settings immediately. New servers are available to all agents by default; existing permissions are preserved.
- Each saved server has **Check connection**, with sign-in and cancellation controls. The check works without creating a space or chat.
- Detailed configuration is under **Advanced settings**.

After updating, open Settings, select **Set up** or **Edit**, save the server, then select **Check connection**. Existing idle chats reload the new configuration on the next message. Dependencies and account sign-in must exist on the computer running Spaces.

Validation: 105 automated tests, browser checks for preset setup and full JSON import, a live Kiro connection check without a space, and a packaged Electron MCP check. GitLab and Atlassian account sign-in was not tested against live accounts.
