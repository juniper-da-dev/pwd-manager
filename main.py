"""
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import os

# Generate a random 32-byte key
key = os.urandom(32)

# Create cipher instance
cipher = ChaCha20Poly1305(key)

# Generate a random 12-byte nonce
nonce = os.urandom(12)

# Plaintext and optional associated data
plaintext = b"Hello, World!"
associated_data = b"metadata"

# Encrypt
ciphertext = cipher.encrypt(nonce, plaintext, associated_data)

# Decrypt
decrypted = cipher.decrypt(nonce, ciphertext, associated_data)
print(decrypted)  # b'Hello, World!'
"""

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305