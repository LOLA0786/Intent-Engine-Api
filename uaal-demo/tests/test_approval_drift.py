from core.engine import authorize
from core.intent import canonical_hash

print("\n=== APPROVAL DRIFT TEST ===")

intent = {
    "action": "transfer_funds",
    "amount": 501_000,
    "recipient": "VENDOR_X"
}

# Approval was for a DIFFERENT amount
approvals = {
    "treasury": True,
    "compliance": True,
    "intent_hash": canonical_hash({
        "amount": 499_000,
        "recipient": "VENDOR_X"
    })
}

allowed, audit = authorize(intent, approvals)

print("Allowed:", allowed)
print("Audit:", audit)
