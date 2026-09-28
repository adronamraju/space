#!/usr/bin/env python3
"""Encrypt or decrypt a file using a 32-byte hexadecimal key and AES-256-GCM.
Requires Python 3 and the cryptography package. Never overwrites an output file.
Format: SPACESENC + version byte 1 + 12-byte nonce + ciphertext + 16-byte tag.
The complete header is authenticated. A decrypted file is published only after
its authentication tag has been verified.
"""
import argparse
import os
from pathlib import Path
import tempfile
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

MAGIC = b'SPACESENC\x01'
CHUNK = 1024 * 1024

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['encrypt', 'decrypt'])
    parser.add_argument('--key-file', type=Path, required=True)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    key = bytes.fromhex(args.key_file.read_text().strip())
    if len(key) != 32:
        raise ValueError('The key must contain exactly 32 bytes in hexadecimal.')
    if args.output.exists():
        raise FileExistsError('Output already exists; choose a new output path.')
    if args.output.resolve() in (args.input.resolve(), args.key_file.resolve()):
        raise ValueError('Input, output and key must use separate files.')
    fd, temp_name = tempfile.mkstemp(prefix='.spaces-crypto-', dir=args.output.parent)
    try:
        with args.input.open('rb') as source, os.fdopen(fd, 'wb') as target:
            if args.operation == 'encrypt':
                nonce = os.urandom(12)
                header = MAGIC + nonce
                cipher = Cipher(algorithms.AES(key), modes.GCM(nonce)).encryptor()
                cipher.authenticate_additional_data(header)
                target.write(header)
                while data := source.read(CHUNK):
                    target.write(cipher.update(data))
                target.write(cipher.finalize())
                target.write(cipher.tag)
            else:
                length = os.fstat(source.fileno()).st_size
                if length < len(MAGIC) + 12 + 16:
                    raise ValueError('Encrypted file is incomplete.')
                header = source.read(len(MAGIC) + 12)
                if not header.startswith(MAGIC):
                    raise ValueError('Unknown encrypted file format.')
                source.seek(-16, os.SEEK_END)
                tag = source.read(16)
                source.seek(len(header))
                cipher = Cipher(algorithms.AES(key), modes.GCM(header[-12:], tag)).decryptor()
                cipher.authenticate_additional_data(header)
                remaining = length - len(header) - 16
                while remaining:
                    data = source.read(min(CHUNK, remaining))
                    if not data:
                        raise ValueError('Encrypted file is incomplete.')
                    remaining -= len(data)
                    target.write(cipher.update(data))
                target.write(cipher.finalize())
            target.flush()
            os.fsync(target.fileno())
        # Atomic publication with no replacement of an existing output.
        os.link(temp_name, args.output)
    finally:
        os.unlink(temp_name)
    print('Created:', args.output)

if __name__ == '__main__':
    main()
