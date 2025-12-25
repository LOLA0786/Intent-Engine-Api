from auth import authorize_intent
from evidence import generate_evidence, verify_evidence

POLICY = "fintech-v1.1"

def test_evidence_verification_passes():
    intent = {
        "action": "process_payment",
        "amount": 5000,
        "country": "India"
    }

    decision = authorize_intent(intent)
    evidence = generate_evidence(intent, decision, POLICY)

    assert verify_evidence(
        intent,
        decision,
        POLICY,
        evidence["evidence_hash"]
    ) is True
