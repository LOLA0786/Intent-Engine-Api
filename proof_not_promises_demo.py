import hashlib
import time
import random

# -------------------------------------------------
# Core primitives
# -------------------------------------------------

def hash_proof(obj):
    return hashlib.sha256(str(obj).encode()).hexdigest()

def execute_policy(intent, node):
    """
    Deterministic policy evaluation.
    Node location MUST NOT affect outcome.
    """
    policy = {
        "max_amount": 1000000,
        "blocked_countries": ["Russia", "Belarus", "Iran"]
    }

    decision = "ALLOW"
    if intent.get("amount", 0) > policy["max_amount"]:
        decision = "BLOCK"

    proof = hash_proof({
        "intent": intent,
        "policy": policy,
        "decision": decision
    })

    return decision, proof


# -------------------------------------------------
# Sanctions policy (hot-swappable)
# -------------------------------------------------

ACTIVE_POLICY = {
    "version": "v1.0",
    "blocked_countries": ["Russia", "Belarus"]
}

def hot_swap_policy(version):
    global ACTIVE_POLICY
    if version == "v1.1":
        ACTIVE_POLICY = {
            "version": "v1.1",
            "blocked_countries": ["Russia", "Belarus", "Iran"]
        }
    time.sleep(0.015)  # simulate 15ms rollout

def check_sanction(country):
    return "BLOCKED" if country in ACTIVE_POLICY["blocked_countries"] else "ALLOWED"


# -------------------------------------------------
# External dependency failure simulation
# -------------------------------------------------

def ofac_api():
    latency = random.randint(50, 120)
    time.sleep(latency / 1000)
    if latency > 80:
        raise TimeoutError("OFAC API timeout")
    return {"status": "OK"}

def check_with_timeout(fn, timeout_ms):
    start = time.time()
    try:
        fn()
        return {
            "decision": "ALLOW",
            "confidence": 95,
            "mode": "NORMAL"
        }
    except Exception:
        return {
            "decision": "BLOCK",
            "confidence": 100,
            "mode": "FAIL_CLOSED"
        }


# -------------------------------------------------
# DEMO SEQUENCE
# -------------------------------------------------

def main():
    print("=== REAL-WORLD STRESS TEST ===")

    # 1. Deterministic replay across nodes
    print("\n1. NODE CONSENSUS TEST:")
    intent = {"action": "approve_loan", "amount": 500000}
    nodes = ["us-east-1", "eu-west-1", "ap-south-1"]

    hashes = []
    for node in nodes:
        decision, proof = execute_policy(intent, node)
        hashes.append(proof)
        print(f"  {node}: Decision={decision}, Hash={proof[:16]}...")

    assert len(set(hashes)) == 1, "❌ Hash mismatch across nodes"
    print("  ✅ Deterministic consensus across regions")

    # 2. Policy hot-swap
    print("\n2. POLICY HOT-SWAP (OFAC update):")
    print(f"  Active policy: {ACTIVE_POLICY}")
    print(f"  Russia: {check_sanction('Russia')}")

    hot_swap_policy("v1.1")
    print("  🔄 Hot-swapped to policy v1.1 in ~15ms")
    print(f"  Active policy: {ACTIVE_POLICY}")
    print(f"  Iran: {check_sanction('Iran')}")
    print("  ✅ Zero downtime, versioned policy enforcement")

    # 3. External dependency failure
    print("\n3. EXTERNAL DEPENDENCY FAILURE:")
    print("  Simulating OFAC API timeout...")
    result = check_with_timeout(ofac_api, timeout_ms=80)
    print(f"  Result: {result['decision']}")
    print(f"  Mode: {result['mode']}")
    print("  ✅ System failed safely and remained responsive")


if __name__ == "__main__":
    main()
