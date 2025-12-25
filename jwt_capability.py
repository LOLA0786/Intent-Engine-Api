import jwt, time

SECRET = "uaal-secret"
TTL = 300

def issue_jwt_cap(decision_id, action, principal):
    payload = {
        "decision_id": decision_id,
        "action": action,
        "principal": principal,
        "exp": time.time() + TTL
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_jwt_cap(token, action, principal):
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    if payload["action"] != action:
        raise Exception("Action mismatch")
    if payload["principal"] != principal:
        raise Exception("Principal mismatch")
    return payload
