def authorize_intent(intent: dict):
    # TEMP deterministic stub
    if intent.get("amount", 0) > 10000:
        return {"allowed": False, "reason": "Amount exceeds limit"}
    return {"allowed": True, "reason": "Allowed"}
