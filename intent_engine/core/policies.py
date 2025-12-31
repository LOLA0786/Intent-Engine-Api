from intent_engine.config.uaal_config import (
    MAX_MONEY_TRANSFER,
    PROTECTED_ENVIRONMENTS,
)

def evaluate_policies(intent):
    violations = []
    payload = intent["payload"]

    if payload.get("tool") == "transfer_money":
        amount = payload.get("args", {}).get("amount", 0)
        if amount > MAX_MONEY_TRANSFER:
            violations.append("HIGH_VALUE_TRANSFER")

    if payload.get("environment") in PROTECTED_ENVIRONMENTS:
        if payload.get("tool") in ["delete_db", "drop_table"]:
            violations.append("DESTRUCTIVE_OPERATION_IN_PROD")

    return violations
