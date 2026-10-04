from pathlib import Path
import argparse

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV

OAEP = padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None,
)

def _to_bytes(text):
    return None if text is None else text.encode("utf-8")

arg = argparse.ArgumentParser(description="Cryptography core module.")

#### INITIALIZATION ####

def create_pem(path: Path, passphrase: str | None = None) -> None:
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=3072,
    )

    if passphrase:
        private_bytes = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.BestAvailableEncryption(_to_bytes(passphrase)),
                )
    else:
        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    
    with open(path, "wb") as f: # TODO: Make this into a argument or deprecate it altogether
        f.write(private_bytes)


    assert isinstance(private_key, rsa.RSAPrivateKey)


def create_keyfile(cert_file, passphrase=None):
    key = AESGCMSIV.generate_key(bit_length=192)
    cert = load_pem(cert_file)
    pub_key = cert.public_key()
    with open("keyfile.key", "+xb") as f:
        f.write(pub_key.encrypt(key, OAEP))

########################

#### CORE FUNCTIONS ####

def load_pem(path, passphrase=None):
    with open(path, "rb") as f: # TODO: Make this a argument
        data = f.read()

    cert = serialization.load_pem_private_key(data, passphrase) # TODO: Add error handling for key serialization

    assert isinstance(cert, rsa.RSAPrivateKey)
    assert isinstance(cert.public_key(), rsa.RSAPublicKey)

    return cert

def load_keyfile():
    with open("keyfile.key", "rb") as f:
        encrypted_keyfile = f.read()

    private_key = load_pem("test.pem")
    plain_key = private_key.decrypt(encrypted_keyfile, OAEP) # TODO: Add error handling for decryption

    return plain_key

########################

if open("keyfile.key", "rb").read():
    pass
else:
    print("Please run 'python core/core.py --create-keyfile --pem <keyfile>' first.")
    raise SystemExit

