from ppo_router import PPORouter
from execute_and_log import execute_and_log

router = PPORouter("ppo_router")

for _ in range(30):
    state = {
        "task_type": "analysis",
        "budget": 0.02,
        "latency_sla_ms": 800,
        "provider_health": {
            "grok": "healthy",
            "gpt": "healthy",
            "local": "healthy"
        }
    }

    plan = router.select_path(state)
    execute_and_log("ppo_reward", state, plan["provider"])

print("✅ PPO executions logged")
