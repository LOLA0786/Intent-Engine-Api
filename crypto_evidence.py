from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey
)
from cryptography.hazmat.primitives import serialization
import base64

def generate_keypair():
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key()
    return priv, pub

def sign(priv, payload: bytes) -> str:
    return base64.b64encode(priv.sign(payload)).decode()

def verify(pub, payload: bytes, signature: str) -> bool:
    try:
        pub.verify(base64.b64decode(signature), payload)
        return True
    except Exception:
        return False
