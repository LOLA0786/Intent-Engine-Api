def enforce_guardrails(intent, plan):
    """
    Final hard safety checks before execution
    """

    # Example: block sensitive tasks on grok
    if intent.get("sensitive") and plan["provider"] == "grok":
        return False, "Sensitive task blocked on grok"

    # Example: latency cap
    if plan.get("timeout_ms", 0) > 2000:
        return False, "Timeout exceeds allowed max"

    return True, "OK"
