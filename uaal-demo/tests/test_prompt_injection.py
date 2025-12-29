from core.engine import authorize

print("\n=== PROMPT INJECTION TEST ===")

declared_intent = {
    "action": "transfer_funds",
    "amount": 300_000,
    "recipient": "SAFE_ENTITY"
}

executed_intent = {
    "action": "transfer_funds",
    "amount": 300_000,
    "recipient": "SANCTIONED_ENTITY"
}

allowed, audit = authorize(
    executed_intent,
    declared_intent=declared_intent
)

print("Allowed:", allowed)
print("Audit:", audit)
