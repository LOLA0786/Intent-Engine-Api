from execute_sim import simulate_execution
from reward import compute_reward
from logs.logger import log_routing

def execute_and_log(router_name, state, provider):
    outcome = simulate_execution(provider)
    reward = compute_reward(outcome)

    log_routing({
        "router": router_name,
        "state": state,
        "outcome": outcome,
        "reward": reward
    })

    return outcome, reward
