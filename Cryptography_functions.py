from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import os

def derive_key_scrypt(password: str, salt: bytes) -> bytes:
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**20,
        r=8,
        p=1,
        backend=default_backend(),
    )
    key = kdf.derive(password.encode())
    return base64.urlsafe_b64encode(key)

def generate_salt() -> bytes:
    return os.urandom(32)