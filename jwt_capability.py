import jwt, time, uuid, redis
from replay_protection import record_replay_attempt, is_blacklisted

SECRET = "uaal-secret"
TTL = 300
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def issue_jwt_cap(decision_id, action, principal):
    jti = str(uuid.uuid4())
    payload = {
        "jti": jti,
        "decision_id": decision_id,
        "action": action,
        "principal": principal,
        "exp": time.time() + TTL
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_jwt_cap(token, action, principal):
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])

    jti = payload["jti"]

    if is_blacklisted(jti):
        raise Exception("Token blacklisted")

    if payload["action"] != action:
        raise Exception("Action mismatch")

    if payload["principal"] != principal:
        raise Exception("Principal mismatch")

    key = f"used_jti:{jti}"
    if r.exists(key):
        record_replay_attempt(principal)
        raise Exception("Replay detected")

    ttl = int(payload["exp"] - time.time())
    r.setex(key, ttl, "1")

    return payload
