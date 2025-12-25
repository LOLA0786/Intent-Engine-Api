def simulate_execution(provider: str) -> dict:
    import random

    profiles = {
        "gpt":   {"cost": 0.012, "latency": (600, 900), "rl_prob": 0.01},
        "grok": {"cost": 0.004, "latency": (500, 1100), "rl_prob": 0.20},
        "local":{"cost": 0.000, "latency": (200, 500), "rl_prob": 0.00}
    }

    p = profiles[provider]
    rate_limited = random.random() < p["rl_prob"]

    return {
        "provider": provider,
        "success": not rate_limited,
        "cost": p["cost"],
        "latency_ms": random.randint(*p["latency"]),
        "rate_limited": rate_limited,
        "retries": 1 if rate_limited else 0
    }

