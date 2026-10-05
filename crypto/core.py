from pathlib import Path
import click

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


#### INITIALIZATION ####

def create_pem(path, passphrase: str | None = None) -> None:
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


def create_keyfile(cert_file, passphrase=None):
    key = AESGCMSIV.generate_key(bit_length=192)
    cert = load_pem(cert_file, passphrase)
    pub_key = cert.public_key()
    with open("keyfile.key", "+xb") as f:
        f.write(pub_key.encrypt(key, OAEP))

########################

#### CORE FUNCTIONS ####

def load_pem(path, passphrase=None):
    path = Path(path)
    with open(path, "rb") as f: # TODO: Make this a argument
        data = f.read()

    try:
        cert = serialization.load_pem_private_key(data, _to_bytes(passphrase)) # TODO: Add error handling for key serialization
        return cert
    except (TypeError, ValueError) as e:
        if str(e) == "Incorrect password, could not decrypt key":
            print("WEE WOO WEE WOO PASSWORD INCORRECT")
        else:
            print(e)

def load_keyfile(cert_file, passphrase=None):
    with open("keyfile.key", "rb") as f:
        encrypted_keyfile = f.read()

    private_key = load_pem(cert_file, passphrase)
    plain_key = private_key.decrypt(encrypted_keyfile, OAEP) # TODO: Add error handling for decryption

    return plain_key

########################

create_pem("keyfile.pem", "testing")
create_keyfile("keyfile.pem", "testing")
print(load_keyfile("keyfile.pem", "testing"))


