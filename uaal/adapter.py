USE_MOCK_UAAL = True  # DEMO SAFE MODE

def authorize_intent(intent_payload):
    amount = intent_payload.get("loan_amount", 0)
    risk = intent_payload.get("risk")

    # Policy 1: amount-based limit
    if amount > 1_000_000:
        return {
            "allowed": False,
            "reason": "Loan amount exceeds AI approval threshold"
        }

    # Policy 2: risk-based deny
    if risk == "high":
        return {
            "allowed": False,
            "reason": "High-risk customer requires manual approval"
        }

    return {
        "allowed": True,
        "reason": "Intent allowed by policy"
    }


def authorize_execution(intent_decision, plan):
    if USE_MOCK_UAAL:
        # Execution-level checks
        if plan["provider"] == "local" and intent_decision.get("sensitive"):
            return {
                "allowed": True,
                "reason": "Local execution allowed for sensitive intent"
            }
        return {
            "allowed": True,
            "reason": "Execution allowed"
        }

    raise RuntimeError("Live UAAL not enabled")
