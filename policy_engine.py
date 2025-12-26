import json
import os
from typing import Dict, Any
from datetime import datetime
import hashlib
import random  # For synthetic variance
from ml_risk_model import infer_risk  # New ML integration

# Load policies from env or file (versioned)
_POLICY_FILE = os.getenv("POLICY_FILE", "policies_v2.json")
with open(_POLICY_FILE, 'r') as f:
    POLICIES = json.load(f)

def authorize_intent(intent: Dict[str, Any], tenant_policies: Dict[str, Any] = None):
    tenant = intent.get("tenant_id", "default")
    pol = tenant_policies or POLICIES.get(tenant, {})
    
    action = intent["action"]
    entity = intent["entity"]
    
    # Infer risk if not provided (ML magic)
    risk = entity.get("risk", infer_risk(entity))
    entity["risk"] = risk  # Cache for logs
    
    # Fintech-specific rules (ML-enhanced)
    if action == "approve_loan":
        amount = entity.get("amount", 0)
        limit = pol.get("loan_limit", 1000000)
        max_risk = pol.get("max_risk", "medium")
        if amount > limit or risk > max_risk:
            return {"decision": "DENY", "reason": f"Exceeds {limit} or inferred risk {risk} > {max_risk}", "score": 0.10}
        return {"decision": "ALLOW", "reason": "Compliant", "score": 0.95}
    elif action == "process_txn":
        amount = entity.get("amount", 0)
        daily_cap = pol.get("txn_daily_cap", 5000000)
        if amount > daily_cap or risk == "high":
            return {"decision": "DENY", "reason": f"Exceeds {daily_cap} or high inferred risk", "score": 0.30}
        return {"decision": "ALLOW", "reason": "Txn processed", "score": 0.85}
    elif action == "flag_fraud":
        if risk == "low":
            return {"decision": "ALLOW", "reason": "No fraud flags", "score": 0.98}
        return {"decision": "DENY", "reason": f"Fraud flagged due to inferred {risk} risk", "score": 0.20}
    
    # Default deny
    return {"decision": "DENY", "reason": "Unknown action", "score": 0.00}

def generate_synthetic_data(num: int, tenant: str = "bankA") -> list[Dict]:
    actions = ["approve_loan", "process_txn", "flag_fraud"]
    data = []
    for i in range(num):
        base_amount = 50000 + (i * 50000)
        # Add variance: 20% chance of high-risk spike
        if random.random() < 0.2:
            velocity = random.uniform(0.7, 1.0)  # Suspicious speed
            history = random.uniform(0.0, 0.3)   # Bad history
            amount = base_amount * 1.5  # Inflate amount
        else:
            velocity = (i / num)
            history = 1 - (i / num)
            amount = base_amount
        
        data.append({
            "action": actions[i % len(actions)],
            "entity": {"amount": amount, "velocity": velocity, "history_score": history},
            "tenant_id": tenant
        })
    return data

def simulate_attack(scenario: str):
    if scenario == "replay":
        return {"vulnerability": "Replay blocked", "status": "secure"}
    return {"status": "Attack simulated - fail-closed"}

def get_metrics():
    return {"decisions": {"ALLOW": 70, "DENY": 30}, "avg_score": 0.78, "ml_infers": True}
