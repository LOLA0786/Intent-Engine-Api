import asyncio
import time
import json
import hashlib
from datetime import datetime, timedelta

# -----------------------------
# Utilities
# -----------------------------
def h(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def now():
    return datetime.utcnow().isoformat() + "Z"

# -----------------------------
# Mock External Feeds (Async)
# -----------------------------
async def ofac_check(name, country):
    await asyncio.sleep(0.08)  # 80ms
    return {
        "feed": "OFAC",
        "match": True,
        "confidence": 95,
        "last_updated": (datetime.utcnow() - timedelta(minutes=5)).isoformat() + "Z"
    }

async def pep_check(name):
    await asyncio.sleep(0.05)  # 50ms
    return {
        "feed": "PEP",
        "match": True,
        "risk": "HIGH"
    }

async def geo_risk(country):
    await asyncio.sleep(0.03)  # 30ms
    return {
        "feed": "GEO",
        "risk": "HIGH",
        "reason": "Comprehensive sanctions"
    }

# -----------------------------
# Policy Engine (Async)
# -----------------------------
async def evaluate_transaction(fail_mode="FAIL_CLOSED"):
    start = time.time()
    latency = {}

    try:
        ofac_task = asyncio.wait_for(ofac_check("Ivan Petrov", "Russia"), timeout=0.15)
        pep_task = asyncio.wait_for(pep_check("Ivan Petrov"), timeout=0.10)
        geo_task = asyncio.wait_for(geo_risk("Russia"), timeout=0.10)

        ofac, pep, geo = await asyncio.gather(ofac_task, pep_task, geo_task)

        latency["OFAC_ms"] = 80
        latency["PEP_ms"] = 50
        latency["GEO_ms"] = 30

        policy = [
            ("OFAC_MATCH", False, "95% SDN match"),
            ("PEP_RISK", False, "Politically exposed person"),
            ("GEO_SANCTIONS", False, "High-risk jurisdiction")
        ]

        decision = "BLOCKED"
        reason = "Sanctions + PEP + Geography"

    except asyncio.TimeoutError as e:
        if fail_mode == "FAIL_CLOSED":
            policy = [
                ("EXTERNAL_FEED_TIMEOUT", False, "Regulatory feed timeout"),
            ]
            decision = "BLOCKED"
            reason = "Fail-closed on missing data"
        else:
            policy = [
                ("EXTERNAL_FEED_TIMEOUT", True, "Proceeding under fail-open"),
            ]
            decision = "ALLOWED"
            reason = "Fail-open policy applied"

    total_latency = int((time.time() - start) * 1000)

    evidence = {
        "timestamp": now(),
        "decision": decision,
        "reason": reason,
        "policy": policy,
        "latency_budget_ms": {
            **latency,
            "TOTAL_ms": total_latency
        }
    }

    print("\n--- POLICY DECISION ---")
    for p in policy:
        print(list(p))

    print("\n--- LATENCY BUDGET ---")
    print(json.dumps(evidence["latency_budget_ms"], indent=2))

    print("\n--- EVIDENCE HASH ---")
    print(h(evidence))

    print(f"\n❌ {decision}: {reason}" if decision == "BLOCKED" else f"\n✅ {decision}: {reason}")

# -----------------------------
# Run Demo
# -----------------------------
if __name__ == "__main__":
    print("\n=== ASYNC + FAILOVER DEMO (FAIL-CLOSED) ===")
    asyncio.run(evaluate_transaction(fail_mode="FAIL_CLOSED"))

    print("\n=== ASYNC + FAILOVER DEMO (FAIL-OPEN) ===")
    asyncio.run(evaluate_transaction(fail_mode="FAIL_OPEN"))
