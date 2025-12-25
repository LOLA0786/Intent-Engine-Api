import json, hashlib, time

def write_audit(decision_id, stage, data, allowed, reason):
    record = {
        "ts": time.time(),
        "decision_id": decision_id,
        "stage": stage,
        "allowed": allowed,
        "reason": reason,
        "data": data
    }
    record["hash"] = hashlib.sha256(
        json.dumps(record, sort_keys=True).encode()
    ).hexdigest()

    with open("audit.log", "a") as f:
        f.write(json.dumps(record) + "\n")
