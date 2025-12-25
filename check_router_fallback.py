from router import RuleBasedRouter

state = {
    "task_type": "analysis",
    "budget": 0.005,
    "latency_sla_ms": 500,
    "provider_health": {
        "grok": "healthy",
        "gpt": "rate_limited",
        "local": "unhealthy"
    }
}

router = RuleBasedRouter()
plan = router.select_path(state)

print("Routing plan:", plan)
assert plan["provider"] == "grok"
print("✅ Fallback routing works")
