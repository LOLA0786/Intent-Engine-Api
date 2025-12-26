import json
import os
from typing import Dict, Any
from datetime import datetime
import hashlib

# Load policies from env or file (versioned)
_POLICY_FILE = os.getenv("POLICY_FILE", "policies_v2.json")
with open(_POLICY_FILE, 'r') as f:
    POLICIES = json.load(f)  # e.g., {"bankA": {"loan_limit": 1000000, "max_risk": "medium"}}

def authorize_intent(intent: Dict[str, Any], tenant_policies: Dict[str, Any] = None):
    tenant = intent.get("tenant_id", "default")
    pol = tenant_policies or POLICIES.get(tenant, {})
    
    action = intent["action"]
    entity = intent["entity"]
    
    # Fintech-specific rules (extendable)
    if action == "approve_loan":
        amount = entity.get("amount", 0)
        risk = entity.get("risk", "high")
        limit = pol.get("loan_limit", 500000)
        max_risk = pol.get("max_risk", "low")
        if amount > limit or risk > max_risk:  # String compare for demo
            return {"decision": "DENY", "reason": f"Exceeds {limit} or risk {risk} > {max_risk}"}
        return {"decision": "ALLOW", "reason": "Compliant", "score": 0.95}  # Confidence stub
    
    # Default deny
    return {"decision": "DENY", "reason": "Unknown action"}

def generate_synthetic_data(num: int, tenant: str = "bankA") -> list[Dict]:
    actions = ["approve_loan", "process_txn", "flag_fraud"]
    risks = ["low", "medium", "high"]
    data = []
    for _ in range(num):
        data.append({
            "action": actions[_ % len(actions)],
            "entity": {"amount": 100000 + (_ * 50000) % 1000000, "risk": risks[_ % 3], "customer_id": f"cust{hashlib.md5(str(_).encode()).hexdigest()[:8]}"},
            "tenant_id": tenant
        })
    return data

def simulate_attack(scenario: str):
    if scenario == "replay":
        # Simulate nonce fail
        return {"vulnerability": "Replay blocked", "status": "secure"}
    return {"status": "Attack simulated - fail-closed"}
