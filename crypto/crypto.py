from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

OEAP = padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None,
)

def load_pem(path, passphrase=None):
    with open(path, 'rb') as f:
        data = f.read()
    return serialization.load_pem_private_key(data, passphrase)

def create_pem():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=3072,
    )

    with open("test.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))


def create_keyfile():
    key = ChaCha20Poly1305.generate_key()
    cert = load_pem("test.pem")
    pub_key = cert.public_key()
    with open("keyfile.key", "+xb") as f:
        f.write(pub_key.encrypt(
            key,
            OEAP
        ))

def decrypt_keyfile():
    cert = load_pem("test.pem")
    priv_key = cert

    with open("keyfile.key", "rb") as f:
        keyfile = f.read()

    return priv_key.decrypt(
        keyfile,
        OEAP
    )


print(decrypt_keyfile())