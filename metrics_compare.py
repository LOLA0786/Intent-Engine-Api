import json
from collections import Counter

def compare(path="logs/routing.log"):
    rule = {"cost":0, "latency":0, "n":0, "providers": Counter()}
    ppo  = {"cost":0, "latency":0, "n":0, "providers": Counter()}

    with open(path) as f:
        for line in f:
            e = json.loads(line)

            if "outcome" not in e:
                continue

            o = e["outcome"]
            router = e.get("router")

            target = ppo if router == "ppo_reward" else rule

            # --- accumulate metrics ---
            target["cost"] += o.get("cost", 0)
            target["latency"] += o.get("latency_ms", 0)
            target["n"] += 1

            # --- provider distribution (safe) ---
            provider = o.get("provider")
            if provider:
                target["providers"][provider] += 1

    return {
        "rule_avg_cost": rule["cost"]/rule["n"] if rule["n"] else 0,
        "ppo_avg_cost": ppo["cost"]/ppo["n"] if ppo["n"] else 0,
        "rule_avg_latency": rule["latency"]/rule["n"] if rule["n"] else 0,
        "ppo_avg_latency": ppo["latency"]/ppo["n"] if ppo["n"] else 0,
        "rule_provider_mix": dict(rule["providers"]),
        "ppo_provider_mix": dict(ppo["providers"]),
    }
