import json, uuid, time

def append_audit(payload):
    tx_id = str(uuid.uuid4())
    record = {
        "tx_id": tx_id,
        "ts": time.time(),
        "payload": payload
    }
    print("AUDIT_APPEND:", json.dumps(record, indent=2))
    return tx_id

if __name__ == "__main__":
    tx = append_audit({
        "tenant": "bankA",
        "action": "approve_loan",
        "amount": 100000,
        "decision": "ALLOW",
        "policy_version": "v3.0"
    })
    print("Fabric tx_id:", tx)
