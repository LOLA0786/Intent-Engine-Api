from core.engine import authorize

print("\n=== MODEL HALLUCINATION TEST ===")

intent = {
    "action": "approve_loan",
    "loan_amount": 100_000,
    "credit_score": 720,
    "derived_from_model": True,
    "source_verified": False
}

allowed, audit = authorize(intent)

print("Allowed:", allowed)
print("Audit:", audit)
