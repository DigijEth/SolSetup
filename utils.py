# path: utils.py
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt_data(key: bytes, data: bytes) -> bytes:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, data, None)
    return nonce + ct

def decrypt_data(key: bytes, token: bytes) -> bytes:
    aesgcm = AESGCM(key)
    nonce = token[:12]
    ct = token[12:]
    return aesgcm.decrypt(nonce, ct, None)
