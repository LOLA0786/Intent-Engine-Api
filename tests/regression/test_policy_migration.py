from auth import authorize_intent
from evidence import generate_evidence

def test_policy_version_migration():
    intent = {
        "action": "process_payment",
        "amount": 8000,
        "country": "India"
    }

    # Old policy
    decision_v1 = authorize_intent(intent)
    evidence_v1 = generate_evidence(intent, decision_v1, "fintech-v1.0")

    # New policy (should not change outcome here)
    decision_v2 = authorize_intent(intent)
    evidence_v2 = generate_evidence(intent, decision_v2, "fintech-v1.1")

    assert decision_v1 == decision_v2
    assert evidence_v1["policy_version"] != evidence_v2["policy_version"]
    assert evidence_v1["evidence_hash"] != evidence_v2["evidence_hash"]

