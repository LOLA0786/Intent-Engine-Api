import json
from intent_engine.core.key_provider import sign

def sign_payload(payload: dict) -> dict:
    message = json.dumps(payload, sort_keys=True).encode()
    sig = sign(message)

    return {
        "payload": payload,
        "signature": sig["signature"],
        "key_provider": sig["provider"]
    }
