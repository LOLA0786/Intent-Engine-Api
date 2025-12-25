POLICY_V3 = {
  "approve_loan": {
    "allowed_roles": ["agent", "human"],
    "max_amount": 1000000,
    "require_human": False,
    "min_trust_level": "high",
    "rate_limit_per_min": 3,
    "daily_spend_cap": 2000000
  }
}
