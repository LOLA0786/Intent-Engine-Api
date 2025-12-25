from redis_usage_tracker import check_rate, check_spend

TRUST_ORDER = {"low": 0, "medium": 1, "high": 2}

def authorize(action, principal, context, policy):
    rule = policy.get(action)
    if not rule:
        return False, "No policy"

    if principal["role"] not in rule["allowed_roles"]:
        return False, "Role not allowed"

    if TRUST_ORDER[principal["trust_level"]] < TRUST_ORDER[rule["min_trust_level"]]:
        return False, "Trust too low"

    amount = context.get("amount", 0)

    if amount > rule["max_amount"]:
        return False, "Amount exceeds limit"

    if not check_rate(principal["id"], rule["rate_limit_per_min"]):
        return False, "Rate limit exceeded"

    if not check_spend(principal["id"], amount, rule["daily_spend_cap"]):
        return False, "Daily spend exceeded"

    return True, "Authorized"
