import os
import sys

from cryptography.exceptions import InvalidTag, InvalidKey
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from functools import lru_cache

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core import load_keyfile

#### CORE/HELPER FUNCTIONS/VARIABLES ####

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

def _to_bytes(text):
    return None if text is None else text.encode("utf-8")

#########################################

def encrypt(text, aad=None):
    nonce = os.urandom(12)
    cipher = get_cipher()

    encrypted_msg = cipher.encrypt(nonce, text.encode('utf-8'), _to_bytes(aad))

    return encrypted_msg + nonce

def decrypt(text, aad=None):
    nonce = text[-12:]
    text = text[:-12]
    cipher = get_cipher()

    try:
        decrypted_msg = cipher.decrypt(nonce, text, _to_bytes(aad))
    except InvalidTag:
        raise InvalidKey

    return decrypted_msg

etext = encrypt("Hello World")
utext = decrypt(etext)

print(etext)
print(utext)
