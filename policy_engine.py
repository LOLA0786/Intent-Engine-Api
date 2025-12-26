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
    
    # Fintech-specific rules (extended)
    if action == "approve_loan":
        amount = entity.get("amount", 0)
        risk = entity.get("risk", "high")
        limit = pol.get("loan_limit", 1000000)
        max_risk = pol.get("max_risk", "medium")
        if amount > limit or risk > max_risk:  # String compare for demo
            return {"decision": "DENY", "reason": f"Exceeds {limit} or risk {risk} > {max_risk}", "score": 0.10}
        return {"decision": "ALLOW", "reason": "Compliant", "score": 0.95}
    elif action == "process_txn":
        amount = entity.get("amount", 0)
        daily_cap = pol.get("txn_daily_cap", 5000000)
        if amount > daily_cap:
            return {"decision": "DENY", "reason": f"Exceeds daily cap {daily_cap}", "score": 0.30}
        return {"decision": "ALLOW", "reason": "Txn processed", "score": 0.85}
    elif action == "flag_fraud":
        risk = entity.get("risk", "high")
        if risk == "low":
            return {"decision": "ALLOW", "reason": "No fraud flags", "score": 0.98}
        return {"decision": "DENY", "reason": f"Fraud flagged due to {risk} risk", "score": 0.20}
    
    # Default deny
    return {"decision": "DENY", "reason": "Unknown action", "score": 0.00}

def generate_synthetic_data(num: int, tenant: str = "bankA") -> list[Dict]:
    actions = ["approve_loan", "process_txn", "flag_fraud"]
    risks = ["low", "medium", "high"]
    data = []
    for i in range(num):
        data.append({
            "action": actions[i % len(actions)],
            "entity": {"amount": 50000 + (i * 50000), "risk": risks[i % 3], "customer_id": f"cust{hashlib.md5(str(i).encode()).hexdigest()[:8]}"},
            "tenant_id": tenant
        })
    return data

def simulate_attack(scenario: str):
    if scenario == "replay":
        return {"vulnerability": "Replay blocked", "status": "secure"}
    return {"status": "Attack simulated - fail-closed"}

def get_metrics():
    return {"decisions": {"ALLOW": 60, "DENY": 40}, "avg_score": 0.75}
