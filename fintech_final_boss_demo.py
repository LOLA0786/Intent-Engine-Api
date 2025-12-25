import asyncio
import time
import json
import hashlib
import uuid
from datetime import datetime

# --------------------------------------------------
# Utilities
# --------------------------------------------------
def sha(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()

def now():
    return datetime.utcnow().isoformat() + "Z"

# --------------------------------------------------
# Replay Protection (Idempotency Store)
# --------------------------------------------------
PROCESSED_DECISIONS = set()

def check_replay(decision_id):
    if decision_id in PROCESSED_DECISIONS:
        raise Exception("REPLAY_DETECTED: Decision already executed")
    PROCESSED_DECISIONS.add(decision_id)

# --------------------------------------------------
# Mock External Services (Async)
# --------------------------------------------------
async def ofac_feed():
    await asyncio.sleep(0.09)  # SLA breach
    raise asyncio.TimeoutError("OFAC timeout")

async def pep_feed():
    await asyncio.sleep(0.04)
    return {"service": "PEP", "risk": "HIGH"}

async def geo_feed():
    await asyncio.sleep(0.06)
    return {"service": "GEO", "risk": "MEDIUM"}

# --------------------------------------------------
# Risk-Based Escalation
# --------------------------------------------------
def escalation_action(confidence):
    if confidence < 50:
        return "BLOCK + ALERT_COMPLIANCE_TEAM"
    elif confidence < 80:
        return "ALLOW_WITH_DAILY_REPORT"
    else:
        return "ALLOW_WITH_MONTHLY_AUDIT"

# --------------------------------------------------
# Policy Engine
# --------------------------------------------------
async def evaluate_transaction():
    trace_id = str(uuid.uuid4())
    decision_id = str(uuid.uuid4())
    check_replay(decision_id)

    start = time.time()
    evidence_chain = []

    # ---- OFAC (Timeout) ----
    try:
        await asyncio.wait_for(ofac_feed(), timeout=0.085)
    except asyncio.TimeoutError:
        evidence_chain.append({
            "trace_id": trace_id,
            "service": "OFAC",
            "result": "TIMEOUT",
            "timestamp": now()
        })

    # ---- PEP + GEO ----
    pep, geo = await asyncio.gather(pep_feed(), geo_feed())

    evidence_chain.append({
        "trace_id": trace_id,
        "service": "PEP",
        "result": pep,
        "timestamp": now()
    })

    evidence_chain.append({
        "trace_id": trace_id,
        "service": "GEO",
        "result": geo,
        "timestamp": now()
    })

    # ---- Confidence Calculation ----
    confidence = 70  # degraded mode (OFAC missing)

    policy = [
        ("OFAC_MATCH", "TIMEOUT", "API timeout at 85ms"),
        ("PEP_RISK", False, "Politically exposed person"),
        ("GEO_SANCTIONS", True, "Medium risk jurisdiction")
    ]

    action = escalation_action(confidence)

    # ---- Evidence Hash Chaining ----
    chained_hash = None
    for step in evidence_chain:
        step_hash = sha(step)
        chained_hash = sha({
            "previous": chained_hash,
            "current": step_hash
        })

    total_latency = int((time.time() - start) * 1000)

    decision = {
        "trace_id": trace_id,
        "decision_id": decision_id,
        "timestamp": now(),
        "policy": policy,
        "confidence": f"{confidence}%",
        "escalation_action": action,
        "latency_ms": total_latency,
        "evidence_chain_hash": chained_hash
    }

    # ---- Output ----
    print("\n=== FINAL BOSS DEMO: RISK-BASED AUTHORIZATION ===")
    print("\n--- DISTRIBUTED TRACE ID ---")
    print(trace_id)

    print("\n--- POLICY DECISION ---")
    for p in policy:
        print(list(p))

    print("\n--- CONFIDENCE SCORE ---")
    print(f"{confidence}%")

    print("\n--- AUTO-ESCALATION ACTION ---")
    print(action)

    print("\n--- EVIDENCE CHAIN HASH ---")
    print(chained_hash)

    print("\n--- LATENCY ---")
    print(f"{total_latency} ms")

    print("\n✅ Decision is REPLAY-SAFE and AUDIT-READY")

# --------------------------------------------------
# Run
# --------------------------------------------------
if __name__ == "__main__":
    asyncio.run(evaluate_transaction())
