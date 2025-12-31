from intent_binding import canonical_hash

def expected_approval_hash(intent: dict) -> str:
    return canonical_hash({
        "action": intent.get("action"),
        "amount": intent.get("amount"),
        "recipient": intent.get("recipient"),
        "currency": intent.get("currency"),
    })

def assert_approval_binding(intent: dict, approval: dict):
    if not approval:
        raise Exception("APPROVAL_MISSING")

    if approval.get("intent_hash") != expected_approval_hash(intent):
        raise Exception("APPROVAL_BINDING_VIOLATION")
