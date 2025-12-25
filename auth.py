def authorize(intent, plan):
    if not intent["allowed"]:
        return False, "Intent denied"

    if plan["provider"] == "grok" and intent.get("sensitive"):
        return False, "Sensitive task blocked on grok"

    return True, "Authorized"

# ==============================
# CANONICAL AUTHORIZATION ADAPTER
# ==============================
def authorize_intent(intent: dict) -> dict:
    """
    Stable API-facing authorization wrapper.
    Selects default policy plan.
    """
    DEFAULT_PLAN = "fintech-v1.1"

    result = authorize(intent, DEFAULT_PLAN)

    # Normalize result to dict
    if isinstance(result, tuple):
        return {"allowed": result[0], "reason": result[1]}
    if isinstance(result, bool):
        return {"allowed": result, "reason": "POLICY_DECISION"}
    if isinstance(result, dict):
        return result

    return {"allowed": False, "reason": "INVALID_AUTH_RESULT"}

# ==============================
# CANONICAL DECISION FUNCTION
# ==============================
def decide_intent(intent: dict, plan: str) -> dict:
    """
    Deterministic allow/deny decision.
    This is the ONLY function the API should call.
    """
    # --- minimal deterministic rules (start simple) ---
    if intent.get("action") == "process_payment":
        if intent.get("amount", 0) >= 10000:
            return {"allowed": False, "reason": "AML_THRESHOLD"}
        if intent.get("country") in ["Russia", "Belarus"]:
            return {"allowed": False, "reason": "SANCTIONED_GEO"}

    if intent.get("sensitive") and intent.get("risk") == "medium":
        return {"allowed": False, "reason": "SENSITIVE_MEDIUM_RISK"}

    return {"allowed": True, "reason": "POLICY_OK"}

# ==============================
# API-FACING ADAPTER
# ==============================
def authorize_intent(intent: dict) -> dict:
    DEFAULT_PLAN = "fintech-v1.1"
    return decide_intent(intent, DEFAULT_PLAN)
