import json

def canonical_signal_payload(signal: dict) -> bytes:
    """
    Deterministic, ordered signal payload for signing
    """
    payload = {
        "signal": signal["signal"],
        "value": signal["value"],
        "provider": signal["provider"],
        "detail": signal.get("detail", ""),
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
