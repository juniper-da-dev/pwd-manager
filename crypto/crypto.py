import base64

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from core import get_master_key
import os
from .exceptions import InvalidKey

def derive(master_key, password, provided_salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=provided_salt,
        iterations=100000,
        backend=default_backend(),
    )

    return kdf.derive((master_key + password))

def encrypt(password, text, aad):
    hash_salt = os.urandom(16)
    password = bytes(password, "utf-8")
    master_key = get_master_key()
    derived_key = derive(master_key, password, hash_salt)
    nonce = bytes(os.urandom(12))
    cipher = ChaCha20Poly1305(derived_key)
    text = bytes(text, "utf-8")
    aad = bytes(aad, "utf-8")

    encrypted_text = base64.b64encode(nonce + b"-" + cipher.encrypt(nonce, text, aad) + b"-" + hash_salt)
    return encrypted_text.decode("utf-8")

def decrypt(password, text, aad):
    password = bytes(password, "utf-8")
    text = base64.b64decode(text)
    master_key = get_master_key()
    parts = text.split(b"-")
    nonce = parts[0]
    text = parts[1]
    salt = parts[2]
    derived_key = derive(master_key, password, salt)
    aad = bytes(aad, "utf-8")

    cipher = ChaCha20Poly1305(derived_key)
    try:
        decrypted_text = cipher.decrypt(nonce, text, aad)
    except InvalidTag:
        raise InvalidKey
    return decrypted_text.decode("utf-8")

