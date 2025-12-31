from core.intent import canonical_hash

def evaluate_policy(intent: dict, approvals: dict = None):
    if intent["action"] == "transfer_funds":
        if intent["amount"] >= 500_000:
            if not approvals:
                return False, "Missing approvals"

            expected_hash = canonical_hash({
                "amount": intent["amount"],
                "recipient": intent["recipient"]
            })

            if approvals.get("intent_hash") != expected_hash:
                return False, "Approval does not match intent parameters"

            if not approvals.get("treasury"):
                return False, "Treasury approval missing"

            if not approvals.get("compliance"):
                return False, "Compliance approval missing"

    if intent.get("derived_from_model") and not intent.get("source_verified"):
        return False, "Unverified model-derived data (hallucination)"

    return True, "Policy satisfied"
