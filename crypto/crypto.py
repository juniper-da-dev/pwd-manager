from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from functools import lru_cache

from crypto.core import load_keyfile

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