import base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization


def generate_keypair():
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    return private_key, public_key


def sign_signal(private_key, payload: bytes) -> str:
    signature = private_key.sign(payload)
    return base64.b64encode(signature).decode()


def verify_signal(public_key, payload: bytes, signature: str) -> bool:
    try:
        public_key.verify(base64.b64decode(signature), payload)
        return True
    except Exception:
        return False
