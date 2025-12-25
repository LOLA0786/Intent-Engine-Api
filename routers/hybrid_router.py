from routers.router import RuleBasedRouter
from ppo_router import PPORouter
from logs.logger import log_routing

class HybridRouter:
    def __init__(self, ppo_model_path="ppo_router"):
        self.rule = RuleBasedRouter()
        self.ppo = PPORouter(ppo_model_path)

    def select_path(self, state):
        rule_plan = self.rule.select_path(state)
        ppo_plan = self.ppo.select_path(state)

        # SAFETY: PPO may only override provider
        final_plan = rule_plan.copy()
        final_plan["provider"] = ppo_plan["provider"]

        log_routing({
            "router": "hybrid",
            "rule_provider": rule_plan["provider"],
            "ppo_provider": ppo_plan["provider"],
            "final_provider": final_plan["provider"],
            "state": state
        })

        return final_plan
