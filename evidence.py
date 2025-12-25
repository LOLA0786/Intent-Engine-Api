import json
import hashlib
import time

def record_evidence(event):
    payload = json.dumps(event, sort_keys=True)
    digest = hashlib.sha256(payload.encode()).hexdigest()

    record = {
        "event": event,
        "hash": digest,
        "timestamp": time.time()
    }

    with open("logs/evidence.log", "a") as f:
        f.write(json.dumps(record) + "\n")

    return digest

# ==============================
# CANONICAL EVIDENCE API (STABLE)
# ==============================
import hashlib
import json
from datetime import datetime

def generate_evidence(intent: dict, decision: dict, policy_version: str) -> dict:
    """
    Stable, deterministic evidence generator.
    This is the ONLY function APIs should import.
    """
    payload = {
        "intent": intent,
        "decision": decision,
        "policy_version": policy_version
    }

    serialized = json.dumps(payload, sort_keys=True).encode()
    evidence_hash = hashlib.sha256(serialized).hexdigest()

    return {
        "decision": decision.get("allowed"),
        "reason": decision.get("reason"),
        "policy_version": policy_version,
        "evidence_hash": evidence_hash,
        "timestamp": datetime.utcnow().isoformat()
    }
