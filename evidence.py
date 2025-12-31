import hashlib
import json
import time
import uuid

# TEMP in-memory store (OK for local + demos)
_EVIDENCE_STORE = {}

def generate_evidence(intent: dict, decision: dict):
    decision_id = f"dec_{uuid.uuid4().hex}"
    timestamp = int(time.time())

    payload = {
        "decision_id": decision_id,
        "intent": intent,
        "decision": decision,
        "timestamp": timestamp,
    }

    raw = json.dumps(payload, sort_keys=True).encode()
    evidence_hash = hashlib.sha256(raw).hexdigest()

    record = {
        "decision_id": decision_id,
        "hash": evidence_hash,
        "algorithm": "sha256",
        "payload": payload,
    }

    _EVIDENCE_STORE[decision_id] = record
    return record

def verify_evidence(decision_id: str, evidence_hash: str) -> bool:
    record = _EVIDENCE_STORE.get(decision_id)
    if not record:
        return False
    return record["hash"] == evidence_hash
