# Audit Log + Policy Versioning

import json, hashlib, time
from datetime import datetime

POLICY_VERSION = "v1.0.0"

AUDIT_LOG_FILE = "audit_log.jsonl"

def hash_decision(payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()

def write_audit_log(
    decision_id: str,
    principal: dict,
    action: str,
    resource: dict,
    decision: str,
    reason: str
):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "decision_id": decision_id,
        "policy_version": POLICY_VERSION,
        "principal": principal,
        "action": action,
        "resource": resource,
        "decision": decision,
        "reason": reason
    }

    entry["decision_hash"] = hash_decision(entry)

    with open(AUDIT_LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    return entry["decision_hash"]
