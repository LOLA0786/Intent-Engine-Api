import uuid, time, redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def issue_capability(decision_id, action, principal_id, ttl=300):
    cap_id = str(uuid.uuid4())
    cap = {
        "decision_id": decision_id,
        "action": action,
        "principal": principal_id,
        "used": "false"
    }

    key = f"cap:{cap_id}"
    r.hset(key, mapping=cap)
    r.expire(key, ttl)

    return cap_id

def consume_capability(cap_id, action, principal_id):
    key = f"cap:{cap_id}"
    cap = r.hgetall(key)

    if not cap:
        return False, "Token expired or invalid"
    if cap["used"] == "true":
        return False, "Token already used"
    if cap["action"] != action:
        return False, "Action mismatch"
    if cap["principal"] != principal_id:
        return False, "Principal mismatch"

    r.hset(key, "used", "true")
    return True, "Capability consumed"
