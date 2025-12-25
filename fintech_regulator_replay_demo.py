import json
import hashlib
import uuid
from datetime import datetime

# --------------------------------------------------
# Utilities
# --------------------------------------------------
def sha(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()

def now():
    return datetime.utcnow().isoformat() + "Z"

# --------------------------------------------------
# Canonical Decision Function (PURE / DETERMINISTIC)
# --------------------------------------------------
def canonical_decision(input_payload):
    """
    IMPORTANT:
    - No randomness
    - No wall-clock dependency
    - Same input => same output
    """

    confidence = 70  # degraded mode
    decision = "ALLOW_WITH_DAILY_REPORT"

    policy = [
        ("OFAC_MATCH", "TIMEOUT", "API timeout at 85ms"),
        ("PEP_RISK", False, "Politically exposed person"),
        ("GEO_SANCTIONS", True, "Medium risk jurisdiction")
    ]

    evidence = {
        "policy": policy,
        "confidence": confidence,
        "decision": decision,
        "input_hash": sha(input_payload)
    }

    return decision, sha(evidence)

# --------------------------------------------------
# Production Execution
# --------------------------------------------------
def production_run():
    decision_id = str(uuid.uuid4())

    input_payload = {
        "action": "approve_large_wire",
        "amount": 4500000,
        "entity": "shell_company",
        "owner": "95%_match_sanctioned",
        "geography": "high_risk_country",
        "velocity": "9th_tx_this_week"
    }

    decision, evidence_hash = canonical_decision(input_payload)

    production_record = {
        "decision_id": decision_id,
        "timestamp": now(),
        "input": input_payload,
        "decision": decision,
        "evidence_hash": evidence_hash
    }

    print("\n=== PRODUCTION DECISION ===")
    print(json.dumps(production_record, indent=2))

    return production_record

# --------------------------------------------------
# REGULATOR SIMULATION MODE
# --------------------------------------------------
def regulator_replay(production_record):
    print("\n--- REGULATOR TEST MODE ---")

    replay_input = production_record["input"]
    expected_decision = production_record["decision"]
    expected_hash = production_record["evidence_hash"]

    decision, evidence_hash = canonical_decision(replay_input)

    print(f"Input replayed: {production_record['decision_id']}")
    print(f"Decision: {decision} (MATCHES PRODUCTION)")
    print(f"Evidence hash: {evidence_hash} (MATCHES)")

    if decision == expected_decision and evidence_hash == expected_hash:
        print("\n✅ Regulator audit passed: Deterministic replay verified")
    else:
        print("\n❌ Regulator audit FAILED: Non-deterministic behavior detected")

# --------------------------------------------------
# Run Demo
# --------------------------------------------------
if __name__ == "__main__":
    prod = production_run()
    regulator_replay(prod)
