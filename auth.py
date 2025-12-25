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

# ==============================
# API-FACING ADAPTER
# ==============================
def authorize_intent(intent: dict) -> dict:
    DEFAULT_PLAN = "fintech-v1.1"
    return decide_intent(intent, DEFAULT_PLAN)

def shadow_decide_intent(intent: dict, plan: str) -> dict:
    """
    Evaluates policy without enforcing it.
    """
    decision = decide_intent(intent, plan)
    return {
        "shadow_allowed": decision["allowed"],
        "shadow_reason": decision["reason"]
    }
def decide_intent(intent: dict, plan: str) -> dict:
    """
    Deterministic, fail-closed authorization decision.
    """

    # ---- required structure ----
    if not isinstance(intent, dict):
        return {"allowed": False, "reason": "INVALID_INTENT_TYPE"}

    action = intent.get("action")
    if action not in {"process_payment", "engage_legal_counsel", "read_prescription"}:
        return {"allowed": False, "reason": "UNKNOWN_ACTION"}

    # ---- normalize fields ----
    amount = intent.get("amount")
    country = intent.get("country")
    risk = intent.get("risk")
    sensitive = intent.get("sensitive", False)

    # ---- payment rules ----
    if action == "process_payment":
        if amount is None or country is None:
            return {"allowed": False, "reason": "MISSING_REQUIRED_FIELD"}

        # type safety
        if not isinstance(amount, (int, float)):
            return {"allowed": False, "reason": "INVALID_AMOUNT_TYPE"}

        # precision guard
        if amount != round(amount, 2):
            return {"allowed": False, "reason": "INVALID_AMOUNT_PRECISION"}

        country = country.strip().lower()

        if amount >= 10000:
            return {"allowed": False, "reason": "AML_THRESHOLD"}

        if country in {"russia", "belarus"}:
            return {"allowed": False, "reason": "SANCTIONED_GEO"}

    # ---- legal rules ----
    if action == "engage_legal_counsel":
        if sensitive and risk == "medium":
            return {"allowed": False, "reason": "SENSITIVE_MEDIUM_RISK"}

    # ---- default allow (explicit) ----
    return {"allowed": True, "reason": "POLICY_OK"}

# ==============================
# CORE-ONLY AUTHORIZATION
# ==============================
from intent_schema import IntentEnvelope

def authorize_enveloped_intent(envelope: dict) -> dict:
    """
    API-facing authorization entrypoint.
    Only the CORE is used for decisions.
    Payload is ignored by policy.
    """
    parsed = IntentEnvelope(**envelope)
    core_intent = parsed.core.model_dump()

    return authorize_intent(core_intent)
