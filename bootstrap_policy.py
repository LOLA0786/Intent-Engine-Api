from policy_registry import register_policy, activate_policy

policy = {
  "approve_loan": {
    "allowed_roles": ["agent"],
    "max_amount": 500000,
    "min_trust_level": "high",
    "rate_limit_per_min": 5,
    "daily_spend_cap": 1000000
  }
}

register_policy("prod-v1", policy, active=True)
activate_policy("prod-v1")

print("Policy prod-v1 active")
