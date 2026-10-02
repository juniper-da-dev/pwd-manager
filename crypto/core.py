from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

OEAP = padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None,
)

#### INITIALIZATION ####

def create_pem():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=3072,
    )

    with open("test.pem", "wb") as f: # TODO: Make this into a argument or deprecate it altogether
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    assert isinstance(private_key, rsa.RSAPrivateKey)


def create_keyfile():
    key = ChaCha20Poly1305.generate_key()
    cert = load_pem("test.pem")
    pub_key = cert.public_key()
    with open("keyfile.key", "+xb") as f:
        f.write(pub_key.encrypt(key, OEAP))

########################

#### CORE FUNCTIONS ####

def load_pem(path, passphrase=None):
    with open(path, "rb") as f: # TODO: Make this into a argument
        data = f.read()
    cert = serialization.load_pem_private_key(data, passphrase) # TODO: Add error handling for key serialization

    assert isinstance(cert, rsa.RSAPrivateKey)
    assert isinstance(cert.public_key(), rsa.RSAPublicKey)

    return cert

def load_keyfile():
    with open("keyfile.key", "rb") as f:
        encrypted_keyfile = f.read()

    private_key = load_pem("test.pem")
    plain_key = private_key.decrypt(encrypted_keyfile, OEAP) # TODO: Add error handling for decryption

    return plain_key

########################

