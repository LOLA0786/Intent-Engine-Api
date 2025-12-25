from auth import authorize_intent
from evidence import generate_evidence

POLICY = "fintech-v1.1"

def test_default_allow_medical_read():
    intent = {
        "action": "read_prescription",
        "country": "India"
    }

    decision = authorize_intent(intent)
    evidence = generate_evidence(intent, decision, POLICY)

    assert evidence["decision"] is True
