from auth import authorize_intent
from evidence import generate_evidence

POLICY = "fintech-v1.1"  # reuse engine, different intent

def test_sensitive_medium_risk_block():
    intent = {
        "action": "engage_legal_counsel",
        "sensitive": True,
        "risk": "medium"
    }

    decision = authorize_intent(intent)
    evidence = generate_evidence(intent, decision, POLICY)

    assert evidence["decision"] is False
    assert evidence["reason"] == "SENSITIVE_MEDIUM_RISK"

