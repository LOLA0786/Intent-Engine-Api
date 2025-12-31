def unwrap_decision(signed_decision: dict) -> dict:
    """
    Always returns the canonical decision payload.
    """
    return signed_decision["payload"]
