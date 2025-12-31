import os
import json
import base64
from datetime import datetime

CURRENT_KEY_VERSION = os.getenv("UAAL_KEY_VERSION", "v1")

def sign(message: bytes) -> dict:
    provider = os.getenv("UAAL_KEY_PROVIDER", "local")

    if provider == "aws":
        import boto3
        kms = boto3.client("kms")
        resp = kms.sign(
            KeyId=os.getenv("UAAL_KMS_KEY_ID"),
            Message=message,
            SigningAlgorithm="RSASSA_PSS_SHA_256",
            MessageType="RAW"
        )
        return {
            "provider": "aws",
            "key_version": CURRENT_KEY_VERSION,
            "signature": base64.b64encode(resp["Signature"]).decode()
        }

    # local fallback
    import nacl.signing
    key = nacl.signing.SigningKey.generate()
    signed = key.sign(message)
    return {
        "provider": "local",
        "key_version": CURRENT_KEY_VERSION,
        "signature": base64.b64encode(signed.signature).decode()
    }
