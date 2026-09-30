from cryptography import x509


import nacl.utils
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

from exceptions import InvalidKey

OEAP = padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None
)

def load_pem(path, passphrase=None):
    with open(path, 'rb') as f:
        data = f.read()
    return (
        serialization.load_pem_private_key(data, passphrase),
        x509.load_pem_x509_certificate(data)
    )
