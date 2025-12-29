import requests
import json

OPA_URL = "http://localhost:8181/v1/data/intent/authz"  # run OPA server separately

def evaluate_with_opa(intent: dict, policy_version: str = "v1"):
    payload = {
        "input": {
            "intent": intent,
            "policy_version": policy_version
        }
    }
    try:
        resp = requests.post(OPA_URL, json=payload)
        resp.raise_for_status()
        result = resp.json()
        return {
            "allowed": result.get("result", {}).get("allow", False),
            "reason": result.get("result", {}).get("reason", "Policy violation")
        }
    except Exception as e:
        return {"allowed": False, "reason": f"OPA error: {str(e)}"}

# Example Rego policy (save as policies/authz.rego)
# package intent.authz
# default allow = false
# allow { input.intent.amount <= 10000 }
