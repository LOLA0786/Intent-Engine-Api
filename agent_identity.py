AGENT_REGISTRY = {
    "agent_a": {"role": "agent", "trust_level": "low"},
    "agent_b": {"role": "agent", "trust_level": "high"}
}

def authenticate_agent(agent_id):
    agent = AGENT_REGISTRY.get(agent_id)
    if not agent:
        return None
    return {
        "id": agent_id,
        "role": agent["role"],
        "type": "agent",
        "trust_level": agent["trust_level"]
    }
