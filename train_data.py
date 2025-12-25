import json

def load_training_data(path="logs/routing.log"):
    states = []
    actions = []
    rewards = []

    with open(path) as f:
        for line in f:
            event = json.loads(line)

            if event.get("router") != "ppo_reward":
                continue

            state = event["state"]
            outcome = event["outcome"]
            reward = event["reward"]

            obs = [
                state["budget"],
                state["latency_sla_ms"] / 1000,
                1.0 if state["provider_health"].get("gpt") == "healthy" else 0.0,
                1.0 if state["provider_health"].get("local") == "healthy" else 0.0,
            ]

            action = ["grok", "gpt", "local"].index(outcome["provider"])

            states.append(obs)
            actions.append(action)
            rewards.append(reward)

    return states, actions, rewards
