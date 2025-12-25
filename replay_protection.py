import redis, time, json
from datetime import datetime

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

MAX_REPLAY_PER_HOUR = 10

def record_replay_attempt(principal_id: str):
    hour = datetime.utcnow().strftime("%Y%m%d%H")
    key = f"replay_attempts:{principal_id}:{hour}"

    attempts = r.incr(key)
    r.expire(key, 3600)

    if attempts > MAX_REPLAY_PER_HOUR:
        alert = {
            "principal": principal_id,
            "attempts": attempts,
            "time": datetime.utcnow().isoformat()
        }
        r.lpush("security_alerts", json.dumps(alert))
        return False

    return True

def blacklist_token(jti: str, reason: str):
    payload = {
        "reason": reason,
        "time": datetime.utcnow().isoformat()
    }
    r.setex(f"blacklisted:{jti}", 86400, json.dumps(payload))

def is_blacklisted(jti: str) -> bool:
    return r.exists(f"blacklisted:{jti}") == 1
