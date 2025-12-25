def authorize(intent, plan):
    if not intent["allowed"]:
        return False, "Intent denied"

    if plan["provider"] == "grok" and intent.get("sensitive"):
        return False, "Sensitive task blocked on grok"

    return True, "Authorized"
