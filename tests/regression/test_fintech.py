from auth import authorize_intent
from evidence import generate_evidence

POLICY = "fintech-v1.1"

def run(intent):
    decision = authorize_intent(intent)
    return generate_evidence(intent, decision, POLICY)

def test_payment_allowed_under_threshold():
    intent = {
        "action": "process_payment",
        "amount": 5000,
        "country": "India"
    }

    r1 = run(intent)
    r2 = run(intent)

    assert r1["decision"] is True
    assert r1["reason"] == "POLICY_OK"
    assert r1["evidence_hash"] == r2["evidence_hash"]

def test_payment_blocked_aml():
    intent = {
        "action": "process_payment",
        "amount": 20000,
        "country": "India"
    }

    r = run(intent)

    assert r["decision"] is False
    assert r["reason"] == "AML_THRESHOLD"
