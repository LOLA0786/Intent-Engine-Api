from router import RuleBasedRouter

# Simulated runtime state
state = {
    "task_type": "analysis",
    "budget": 0.02,
    "latency_sla_ms": 800,
    "provider_health": {
        "grok": "rate_limited",
        "gpt": "healthy",
        "local": "unhealthy"
    }
}

router = RuleBasedRouter()
plan = router.select_path(state)

print("Routing plan:", plan)

# Hard check
assert plan["provider"] == "gpt", "Router picked wrong provider"
print("✅ Router check passed")
