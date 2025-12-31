import os
import json
import hashlib
from datetime import datetime

REGISTRY_PATH = "opa_policy_registry.json"

def _hash_policy(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def register_policy(policy_text: str) -> dict:
    entry = {
        "hash": _hash_policy(policy_text),
        "timestamp": datetime.utcnow().isoformat(),
        "policy": policy_text
    }

    if os.path.exists(REGISTRY_PATH):
        data = json.load(open(REGISTRY_PATH))
    else:
        data = []

    data.append(entry)
    json.dump(data, open(REGISTRY_PATH, "w"), indent=2)

    return entry

def list_policies():
    if not os.path.exists(REGISTRY_PATH):
        return []
    return json.load(open(REGISTRY_PATH))

def diff_policies(hash_a, hash_b):
    policies = {p["hash"]: p["policy"] for p in list_policies()}
    a = policies.get(hash_a, "").splitlines()
    b = policies.get(hash_b, "").splitlines()

    import difflib
    return list(difflib.unified_diff(a, b, lineterm=""))
