from policy_registry import register_policy, activate_policy
from policy_diff_and_dryrun import dry_run
from capability_token import issue_capability, consume_capability

policy = {
  "approve_loan": {
    "allowed_roles": ["agent"],
    "max_amount": 500000,
    "min_trust_level": "high",
    "rate_limit_per_min": 2,
    "daily_spend_cap": 700000
  }
}

register_policy("v4", policy, active=True)
activate_policy("v4")

principal = {
    "id": "agent_b",
    "role": "agent",
    "type": "agent",
    "trust_level": "high"
}

context = {"amount": 300000}

# 1️⃣ Dry run
print(dry_run("v4", "approve_loan", principal, context))

# 2️⃣ Issue capability
decision_id = "dec-001"
cap_id = issue_capability(decision_id, "approve_loan", principal["id"])
print("CAP ISSUED:", cap_id)

# 3️⃣ Consume once (OK)
print(consume_capability(cap_id, "approve_loan", principal["id"]))

# 4️⃣ Replay attack (BLOCKED)
print(consume_capability(cap_id, "approve_loan", principal["id"]))

# 5️⃣ Rate limit test (3rd call should fail)
print(dry_run("v4", "approve_loan", principal, context))
print(dry_run("v4", "approve_loan", principal, context))
print(dry_run("v4", "approve_loan", principal, context))
