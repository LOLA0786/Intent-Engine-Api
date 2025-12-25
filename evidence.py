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
