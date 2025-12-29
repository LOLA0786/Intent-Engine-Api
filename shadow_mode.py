import json
from approval_store import store_approval_request  # you'll add this

def shadow_evaluate(intent: dict, real_decision: dict):
    shadow_decision = {}  # run alternative policy/ML risk
    if real_decision["allowed"] != shadow_decision.get("allowed", True):
        print(f"SHADOW ALERT: Divergence on intent {intent}")
        # Log to audit
    
    if real_decision.get("risk_score", 0) > 0.8:
        ticket = store_approval_request(intent, real_decision)
        return {"escalated": True, "ticket_id": ticket}
    
    return real_decision
