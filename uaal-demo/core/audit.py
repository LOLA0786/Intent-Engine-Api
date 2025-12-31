import time
from core.intent import canonical_hash

AUDIT_LOG = []

def log_decision(intent, allowed, reason):
    record = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        "intent": intent,
        "decision": "ALLOW" if allowed else "BLOCK",
        "reason": reason,
        "intent_hash": canonical_hash(intent)
    }
    AUDIT_LOG.append(record)
    return record
