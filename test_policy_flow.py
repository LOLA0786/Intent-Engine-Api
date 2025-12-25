from policy_registry import register_policy, activate_policy, get_active_policy, rollback
from policy_diff_and_dryrun import policy_diff, dry_run

# 1️⃣ Register policies
policy_v1 = {
    "approve_loan": {
        "allowed_roles": ["human"],
        "max_amount": 500000,
        "require_human": True
    }
}

policy_v2 = {
    "approve_loan": {
        "allowed_roles": ["human", "agent"],
        "max_amount": 1000000,
        "require_human": False
    }
}

register_policy("v1", policy_v1, active=True)
register_policy("v2", policy_v2)

# 2️⃣ Diff policies
print("DIFF v1 -> v2")
print(policy_diff("v1", "v2"))

# 3️⃣ Dry-run before activation
principal = {"id": "agent_1", "role": "agent", "type": "agent"}
context = {"amount": 700000}

print("DRY RUN v2")
print(dry_run("v2", "approve_loan", principal, context))

# 4️⃣ Activate v2
activate_policy("v2")
print("ACTIVE POLICY:", get_active_policy()[0])

# 5️⃣ Rollback
rollback("v1")
print("AFTER ROLLBACK:", get_active_policy()[0])
