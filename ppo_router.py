from stable_baselines3 import PPO
import numpy as np

class PPORouter:
    def __init__(self, model_path: str):
        self.model = PPO.load(model_path)

    def select_path(self, state: dict) -> dict:
        """
        Converts runtime state → PPO observation → provider choice
        """

        obs = np.array([[
            state["budget"],
            state["latency_sla_ms"] / 1000,
            1.0 if state["provider_health"].get("gpt") == "healthy" else 0.0,
            1.0 if state["provider_health"].get("local") == "healthy" else 0.0,
        ]])

        action, _ = self.model.predict(obs, deterministic=True)

        provider = ["gpt", "grok", "local"][int(action)]

        return {
            "provider": provider,
            "max_retries": 1,
            "timeout_ms": state["latency_sla_ms"]
        }
