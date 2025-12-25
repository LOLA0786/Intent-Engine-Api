import time
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

RATE_WINDOW = 60          # seconds
DAILY_WINDOW = 86400     # seconds

def check_rate(principal_id, limit):
    key = f"rate:{principal_id}"
    now = int(time.time())

    r.zadd(key, {now: now})
    r.zremrangebyscore(key, 0, now - RATE_WINDOW)

    count = r.zcard(key)
    r.expire(key, RATE_WINDOW)

    return count <= limit

def check_spend(principal_id, amount, cap):
    key = f"spend:{principal_id}"
    current = int(r.get(key) or 0)

    if current + amount > cap:
        return False

    r.incrby(key, amount)
    r.expire(key, DAILY_WINDOW)
    return True
