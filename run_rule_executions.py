from routers.router import RuleBasedRouter
from execute_and_log import execute_and_log

router = RuleBasedRouter()

for _ in range(30):
    state = {
        "task_type": "analysis",
        "budget": 0.02,
        "latency_sla_ms": 800,
        "provider_health": {
            "grok": "healthy",
            "gpt": "healthy",
            "local": "unhealthy"
        }
    }

    plan = router.select_path(state)
    execute_and_log("rule_based", state, plan["provider"])

print("✅ Rule-based executions logged")
