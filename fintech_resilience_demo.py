import asyncio
import time
import json
import hashlib
from datetime import datetime

# --------------------------------------------------
# Utilities
# --------------------------------------------------
def h(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()

def now():
    return datetime.utcnow().isoformat() + "Z"

# --------------------------------------------------
# Circuit Breaker
# --------------------------------------------------
class CircuitBreaker:
    def __init__(self, failures=2):
        self.failures = failures
        self.count = 0
        self.open = False

    def record_failure(self):
        self.count += 1
        if self.count >= self.failures:
            self.open = True

    def record_success(self):
        self.count = 0
        self.open = False

# --------------------------------------------------
# Mock Feeds
# --------------------------------------------------
async def ofac_feed(timeout_ms=85):
    await asyncio.sleep(timeout_ms / 1000)
    raise asyncio.TimeoutError("OFAC timeout")

async def pep_feed():
    await asyncio.sleep(0.05)
    return {"feed": "PEP", "risk": "HIGH"}

async def geo_feed():
    await asyncio.sleep(0.08)
    return {"feed": "GEO", "risk": "MEDIUM"}

# --------------------------------------------------
# Policy Engine
# --------------------------------------------------
async def evaluate(fail_mode="FAIL_CLOSED", hot_policy=True):
    start = time.time()
    breaker = CircuitBreaker()
    evidence_chain = []

    policy_version = "v1.0"
    if hot_policy:
        policy_version = "v1.1-hot-reload"

    # ---------------- TIMEOUT + RETRY ----------------
    ofac_result = None
    for attempt in range(1, 3):
        try:
            await asyncio.wait_for(ofac_feed(), timeout=0.085)
        except asyncio.TimeoutError:
            breaker.record_failure()
            evidence_chain.append({
                "attempt": attempt,
                "feed": "OFAC",
                "result": "TIMEOUT",
                "timestamp": now()
            })

    # ---------------- CIRCUIT BREAKER ----------------
    if breaker.open:
        ofac_status = ("OFAC_MATCH", "TIMEOUT", "API timeout at 85ms")
    else:
        ofac_status = ("OFAC_MATCH", False, "No match")

    pep = await pep_feed()
    geo = await geo_feed()

    # ---------------- DEGRADED MODE ----------------
    degraded = breaker.open
    confidence = 70 if degraded else 95

    policy = [
        ofac_status,
        ("PEP_RISK", False, "Politically exposed person"),
        ("GEO_SANCTIONS", True, "Medium risk jurisdiction")
    ]

    decision = "BLOCK"
    fallout = "FAIL-CLOSED: Block transaction"

    if fail_mode == "FAIL_OPEN" and degraded:
        decision = "ALLOW_WITH_REVIEW"
        fallout = "FAIL-OPEN: Manual review + compliance alert"

    total_latency = int((time.time() - start) * 1000)

    evidence = {
        "timestamp": now(),
        "policy_version": policy_version,
        "decision": decision,
        "confidence": f"{confidence}%",
        "degraded_mode": degraded,
        "policy": policy,
        "evidence_chain": evidence_chain,
        "latency_ms": total_latency
    }

    # ---------------- OUTPUT ----------------
    print("\n--- POLICY DECISION ---")
    for p in policy:
        print(list(p))

    if degraded:
        print("\n--- DEGRADED MODE ACTIVE ---")
        print("Available: PEP + GEO (130ms combined)")
        print("Unavailable: OFAC (timeout)")
        print(f"Decision: {decision}")
        print(f"Confidence: {confidence}%")

    print("\n--- FALLOUT ACTION ---")
    print(fallout)

    print("\n--- EVIDENCE HASH ---")
    print(h(evidence))

# --------------------------------------------------
# Run Demo
# --------------------------------------------------
if __name__ == "__main__":
    print("\n=== RESILIENCE DEMO: FAIL-CLOSED ===")
    asyncio.run(evaluate(fail_mode="FAIL_CLOSED"))

    print("\n=== RESILIENCE DEMO: FAIL-OPEN ===")
    asyncio.run(evaluate(fail_mode="FAIL_OPEN"))
