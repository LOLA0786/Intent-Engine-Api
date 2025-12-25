import time
from collections import defaultdict

CALLS = defaultdict(list)
SPEND = defaultdict(int)

def check_rate(principal_id, limit):
    now = time.time()
    CALLS[principal_id] = [t for t in CALLS[principal_id] if now - t < 60]
    if len(CALLS[principal_id]) >= limit:
        return False
    CALLS[principal_id].append(now)
    return True

def check_spend(principal_id, amount, cap):
    if SPEND[principal_id] + amount > cap:
        return False
    SPEND[principal_id] += amount
    return True
