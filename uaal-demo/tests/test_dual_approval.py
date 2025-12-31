from core.engine import authorize

print("\n=== DUAL APPROVAL TEST ===")

intent = {
    "action": "transfer_funds",
    "amount": 500_000,
    "recipient": "VENDOR_X"
}

allowed, audit = authorize(intent, approvals={"treasury": True})

print("Allowed:", allowed)
print("Audit:", audit)
