# Policy Registry with Versioning + Rollback

import json
from datetime import datetime

POLICY_STORE = "policies.json"

def load_policies():
    try:
        with open(POLICY_STORE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_policies(policies):
    with open(POLICY_STORE, "w") as f:
        json.dump(policies, f, indent=2)

def register_policy(version: str, policy: dict, active=False):
    policies = load_policies()
    policies[version] = {
        "policy": policy,
        "created_at": datetime.utcnow().isoformat(),
        "active": active
    }
    save_policies(policies)

def activate_policy(version: str):
    policies = load_policies()
    if version not in policies:
        raise ValueError("Policy version not found")

    for v in policies:
        policies[v]["active"] = False

    policies[version]["active"] = True
    save_policies(policies)

def get_active_policy():
    policies = load_policies()
    for v, data in policies.items():
        if data.get("active"):
            return v, data["policy"]
    raise RuntimeError("No active policy")

def rollback(to_version: str):
    activate_policy(to_version)
    return f"Rolled back to policy {to_version}"
