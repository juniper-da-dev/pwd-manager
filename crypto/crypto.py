from cryptography import x509
from

import nacl.utils
from nacl.secret import SecretBox, Aead
from nacl.pwhash import argon2id

from crypto.exceptions import InvalidKey

if __name__ == "__main__":
    def create_key():
        passphrase = nacl.utils.random(nacl.secret.Aead.KEY_SIZE)

        if not passphrase or len(passphrase) <=6:
            raise InvalidKey("Passphrase must be at least 6 characters long")
        key = argon2id.kdf(
            size=nacl.secret.Aead.KEY_SIZE,
            password=passphrase,
            salt=nacl.utils.random(argon2id.SALTBYTES)
        )
        try:
            with open("keyfile.key", "xb") as f:
                f.write(key)
        except FileExistsError:
            raise FileExistsError("Key file already exists")


