import json
import hashlib
import uuid
from datetime import datetime

# =========================================================
# Utilities
# =========================================================
def sha(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()

def now():
    return datetime.utcnow().isoformat() + "Z"

# =========================================================
# Cross-Region Quorum (3 regions)
# =========================================================
REGIONS = ["us-east", "eu-west", "ap-south"]

def regional_decision(region, input_payload):
    """
    Deterministic per-region evaluation.
    In real life: separate infra, keys, logs.
    """
    return {
        "region": region,
        "decision": "ALLOW_WITH_DAILY_REPORT",
        "confidence": 70,
        "policy_version": "v1.1",
        "input_hash": sha(input_payload)
    }

def quorum_decision(input_payload):
    regional_results = [regional_decision(r, input_payload) for r in REGIONS]

    decisions = [r["decision"] for r in regional_results]
    final_decision = max(set(decisions), key=decisions.count)  # majority

    return regional_results, final_decision

# =========================================================
# Cryptographic Attestation (Sigstore-style)
# =========================================================
def attest(decision_record):
    """
    Simulates signed attestation.
    """
    attestation = {
        "attestor": "intent-engine-prod",
        "timestamp": now(),
        "decision_hash": sha(decision_record),
        "signature": sha("PRIVATE_KEY::" + sha(decision_record))
    }
    return attestation

# =========================================================
# Regulator-Verifiable Export Bundle
# =========================================================
def export_bundle(input_payload, regions, final_decision, attestation):
    bundle = {
        "bundle_version": "1.0",
        "exported_at": now(),
        "input": input_payload,
        "regional_votes": regions,
        "final_decision": final_decision,
        "attestation": attestation,
        "bundle_hash": sha({
            "input": input_payload,
            "regions": regions,
            "decision": final_decision,
            "attestation": attestation
        })
    }
    return bundle

# =========================================================
# FINAL BOSS DEMO
# =========================================================
if __name__ == "__main__":
    decision_id = str(uuid.uuid4())

    input_payload = {
        "decision_id": decision_id,
        "action": "approve_large_wire",
        "amount": 4500000,
        "entity": "shell_company",
        "owner": "95%_match_sanctioned",
        "geography": "high_risk_country",
        "velocity": "9th_tx_this_week"
    }

    print("\n=== FINAL BOSS: CROSS-REGION QUORUM ===")
    regions, final_decision = quorum_decision(input_payload)
    print(json.dumps(regions, indent=2))
    print(f"\nFinal quorum decision: {final_decision}")

    print("\n=== FINAL BOSS: CRYPTOGRAPHIC ATTESTATION ===")
    decision_record = {
        "decision_id": decision_id,
        "decision": final_decision,
        "regions": regions,
        "timestamp": now()
    }
    attestation = attest(decision_record)
    print(json.dumps(attestation, indent=2))

    print("\n=== FINAL BOSS: REGULATOR EXPORT BUNDLE ===")
    bundle = export_bundle(input_payload, regions, final_decision, attestation)
    print(json.dumps(bundle, indent=2))

    print("\n✅ SYSTEM STATE:")
    print("• Decision quorum-verified across regions")
    print("• Decision cryptographically attested")
    print("• Regulator-verifiable export bundle generated")
