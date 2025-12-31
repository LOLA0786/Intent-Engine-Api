import time
from collections import defaultdict

_calls = defaultdict(list)

def check_rate(agent_id, limit):
    now = time.time()
    window = now - 60

    _calls[agent_id] = [t for t in _calls[agent_id] if t > window]

    if len(_calls[agent_id]) >= limit:
        return False

    _calls[agent_id].append(now)
    return True
