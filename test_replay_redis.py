import time, hashlib, redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

TENANT = "bankA"
USER = "agent_1"

def make_nonce():
    raw = f"{time.time()}:{USER}:{TENANT}"
    return hashlib.sha256(raw.encode()).hexdigest()

def check_nonce(nonce):
    key = f"nonce:{TENANT}:{USER}:{nonce}"
    if r.exists(key):
        return False
    r.setex(key, 1800, "1")  # 30 min TTL
    return True

nonce = make_nonce()

print("First use:", check_nonce(nonce))   # EXPECT True
print("Replay:", check_nonce(nonce))      # EXPECT False
