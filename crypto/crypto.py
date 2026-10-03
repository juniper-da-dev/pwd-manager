import os
import sys

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from functools import lru_cache

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core import load_keyfile

#### CORE FUNCTIONS/VARIABLES ####

OEAP = padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None,
)

@lru_cache(maxsize=1)
def get_cipher():
    print("Loading Keyfile...")

    key = load_keyfile()
    return ChaCha20Poly1305(key)

##################################

def encrypt(text, aad=None):
    nonce = os.urandom(12)
    cipher = get_cipher()
    aad = bytes(aad, encoding="utf-8") if aad is not None else None

    encrypted_msg = cipher.encrypt(nonce, bytes(text, encoding="utf-8"), aad)

    return encrypted_msg + nonce

def decrypt(text, aad=None):
    nonce = text[-12:]
    text = text[:-12]
    aad = bytes(aad, encoding="utf-8") if aad is not None else None
    cipher = get_cipher()

    return cipher.decrypt(nonce, text, aad)

etext = encrypt("Hello World")
utext = decrypt(etext)

print(etext)
print(utext)