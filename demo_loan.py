import hashlib
import json

# -----------------------------
# Policy Configuration
# -----------------------------
AMOUNT_LIMIT = 1_000_000  # ₹10L

# -----------------------------
# Utilities
# -----------------------------
def evidence_hash(obj):
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True).encode()
    ).hexdigest()

def print_section(title):
    print("\n" + "-" * 60)
    print(title)
    print("-" * 60)

# -----------------------------
# Policy Engine
# -----------------------------
def evaluate_policy(intent):
    decisions = []

    # Policy 1: Amount limit
    if intent["loan_amount"] <= AMOUNT_LIMIT:
        decisions.append([
            "AMOUNT_LIMIT",
            True,
            "Loan amount within limit"
        ])
        amount_ok = True
    else:
        decisions.append([
            "AMOUNT_LIMIT",
            False,
            "Loan amount exceeds ₹10L policy limit"
        ])
        amount_ok = False

    # Policy 2: Sensitive + Risk
    if intent["sensitive"] and intent["risk"] in ["medium", "high"]:
        decisions.append([
            "RISK_CHECK",
            False,
            "Sensitive actions blocked for medium/high risk"
        ])
        risk_ok = False
    else:
        decisions.append([
            "RISK_CHECK",
            True,
            "Risk level acceptable"
        ])
        risk_ok = True

    allowed = amount_ok and risk_ok
    return allowed, decisions

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    loan_amount = int(input("Enter loan_amount: "))
    risk = input("Enter risk (low/medium/high): ").strip().lower()
    sensitive = input("Enter sensitive (true/false): ").strip().lower() == "true"

    intent = {
        "action": "approve_loan",
        "loan_amount": loan_amount,
        "risk": risk,
        "sensitive": sensitive
    }

    print_section("INTENT")
    print(json.dumps(intent, indent=2))

    allowed, policy_decisions = evaluate_policy(intent)

    print_section("POLICY DECISION")
    for d in policy_decisions:
        print(d)

    print_section("EVIDENCE HASH")
    print(evidence_hash({
        "intent": intent,
        "policy_decisions": policy_decisions
    }))

    print_section("FINAL OUTCOME")
    if allowed:
        print("✅ APPROVED - All policy checks passed")
    else:
        print("❌ BLOCKED BY POLICY")

