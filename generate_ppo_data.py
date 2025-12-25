
import random
from routers.router import RuleBasedRouter
from logs.logger import log_routing
from reward import compute_reward
from execute_sim import simulate_execution
providers = ["gpt", "grok", "local"]

router = RuleBasedRouter()

for _ in range(60):
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
 provider = random.choice(providers) 
    plan = router.select_path(state)
    outcome = simulate_execution(plan["provider"])
    reward = compute_reward(outcome)

    log_routing({
        "router": "ppo_reward",
        "state": state,
        "outcome": outcome,
        "reward": reward
    })

print("✅ PPO training data generated")
