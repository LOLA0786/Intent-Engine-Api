from auth import authorize_intent
from evidence import generate_evidence, verify_evidence

POLICY = "fintech-v1.1"

# 1️⃣ Missing required field → fail closed
def test_missing_amount_fails_closed():
    intent = {"action": "process_payment", "country": "India"}
    decision = authorize_intent(intent)
    assert decision["allowed"] is False

# 2️⃣ Unknown action → fail closed
def test_unknown_action_fails_closed():
    intent = {"action": "do_weird_thing"}
    decision = authorize_intent(intent)
    assert decision["allowed"] is False

# 3️⃣ Type confusion attack
def test_amount_string_fails_closed():
    intent = {"action": "process_payment", "amount": "5000", "country": "India"}
    decision = authorize_intent(intent)
    assert decision["allowed"] is False

# 4️⃣ Boundary precision abuse
def test_amount_precision_edge():
    intent = {"action": "process_payment", "amount": 9999.999, "country": "India"}
    decision = authorize_intent(intent)
    assert decision["allowed"] is False

# 5️⃣ Case-insensitive country normalization
def test_country_case_normalization():
    intent = {"action": "process_payment", "amount": 5000, "country": "rUsSiA"}
    decision = authorize_intent(intent)
    assert decision["allowed"] is False

# 6️⃣ Evidence tampering (intent)
def test_evidence_tamper_intent_fails():
    intent = {"action": "process_payment", "amount": 5000, "country": "India"}
    decision = authorize_intent(intent)
    evidence = generate_evidence(intent, decision, POLICY)

    tampered_intent = dict(intent)
    tampered_intent["amount"] = 7000

    assert verify_evidence(
        tampered_intent,
        decision,
        POLICY,
        evidence["evidence_hash"]
    ) is False

# 7️⃣ Evidence tampering (decision)
def test_evidence_tamper_decision_fails():
    intent = {"action": "process_payment", "amount": 5000, "country": "India"}
    decision = authorize_intent(intent)
    evidence = generate_evidence(intent, decision, POLICY)

    tampered_decision = {"allowed": False, "reason": "HACKED"}

    assert verify_evidence(
        intent,
        tampered_decision,
        POLICY,
        evidence["evidence_hash"]
    ) is False

# 8️⃣ Policy version tampering
def test_policy_version_tamper_fails():
    intent = {"action": "process_payment", "amount": 5000, "country": "India"}
    decision = authorize_intent(intent)
    evidence = generate_evidence(intent, decision, POLICY)

    assert verify_evidence(
        intent,
        decision,
        "fintech-v9.9",
        evidence["evidence_hash"]
    ) is False

# 9️⃣ Determinism under repetition
def test_determinism_under_repetition():
    intent = {"action": "process_payment", "amount": 5000, "country": "India"}
    hashes = set()

    for _ in range(50):
        decision = authorize_intent(intent)
        evidence = generate_evidence(intent, decision, POLICY)
        hashes.add(evidence["evidence_hash"])

    assert len(hashes) == 1

# 🔟 Timestamp exclusion from hash
def test_timestamp_not_in_hash():
    intent = {"action": "process_payment", "amount": 5000, "country": "India"}
    decision = authorize_intent(intent)

    e1 = generate_evidence(intent, decision, POLICY)
    e2 = generate_evidence(intent, decision, POLICY)

    assert e1["evidence_hash"] == e2["evidence_hash"]
    assert e1["timestamp"] != e2["timestamp"]
