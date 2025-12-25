from abc import ABC, abstractmethod
from typing import Dict, Any
from logs.logger import log_routing

class ExecutionRouter(ABC):
    @abstractmethod
    def select_path(self, state: Dict[str, Any]) -> Dict[str, Any]:
        pass


class RuleBasedRouter(ExecutionRouter):
    def select_path(self, state):
        health = state["provider_health"]
        budget = state["budget"]
        latency = state["latency_sla_ms"]

        if health.get("local") == "healthy":
            provider = "local"
        elif health.get("gpt") == "healthy" and budget >= 0.01:
            provider = "gpt"
        else:
            provider = "grok"

        plan = {
            "provider": provider,
            "max_retries": 1,
            "timeout_ms": latency
        }

        log_routing({
            "router": "rule_based",
            "state": state,
            "plan": plan
        })

        return plan
