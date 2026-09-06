import base64

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from core import get_master_key
import os

from exceptions import InvalidKey


def encrypt(text, aad):
    key = get_master_key()
    nonce = bytes(os.urandom(12))
    cipher = ChaCha20Poly1305(key)
    text = bytes(text, "utf-8")
    aad = bytes(aad, "utf-8")

    encrypted_text = base64.b64encode(nonce + cipher.encrypt(nonce, text, aad))
    return encrypted_text

def decrypt(text, aad):
    text = base64.b64decode(text)
    key = get_master_key()
    nonce = bytes(text[:12])
    text = bytes(text[12:])
    aad = bytes(aad, "utf-8")

    cipher = ChaCha20Poly1305(key)
    try:
        decrypted_text = cipher.decrypt(nonce, text, aad)
    except InvalidTag:
        raise InvalidKey
    return decrypted_text.decode("utf-8")


