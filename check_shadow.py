from routers.router import RuleBasedRouter
from ppo_shadow import ShadowPPORouter
from logs.logger import log_routing

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

rule_router = RuleBasedRouter()
shadow_router = ShadowPPORouter()

rule_plan = rule_router.select_path(state)
ppo_choice = shadow_router.suggest(state)

log_routing({
    "router": "shadow_ppo",
    "rule_choice": rule_plan["provider"],
    "ppo_choice": ppo_choice,
    "state": state
})

print("Rule-based choice:", rule_plan["provider"])
print("Shadow PPO choice:", ppo_choice)
print("✅ Shadow PPO check complete")
