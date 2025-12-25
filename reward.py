def compute_reward(outcome: dict) -> float:
    """
    Reward function for PPO routing.
    outcome example:
    {
        "success": True,
        "cost": 0.011,
        "latency_ms": 620,
        "rate_limited": False,
        "retries": 0
    }
    """

    if not outcome.get("success"):
        return -2.0

    reward = 1.0

    # Cost penalty (target = -zsh.01)
    reward -= min(outcome["cost"] / 0.01, 3.0) * 0.6


    # Latency penalty (target = 1000ms)
    reward -= min(outcome["latency_ms"] / 1000, 2.0) * 0.2

    # Rate limit penalty
    if outcome.get("rate_limited"):
        reward -= 0.8

    # Retry penalty
    reward -= min(outcome.get("retries", 0), 3) * 0.15

    return max(-3, reward)
