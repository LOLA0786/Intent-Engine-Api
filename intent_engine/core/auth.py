import os
import hmac
import hashlib

AUDITOR_SECRET = os.getenv("UAAL_AUDITOR_SECRET", "dev-secret")

def generate_auditor_token(auditor_id: str) -> str:
    msg = auditor_id.encode()
    return hmac.new(AUDITOR_SECRET.encode(), msg, hashlib.sha256).hexdigest()

def verify_auditor_token(auditor_id: str, token: str) -> bool:
    expected = generate_auditor_token(auditor_id)
    return hmac.compare_digest(expected, token)
