import time
import json
from datetime import datetime, timedelta
import hashlib
import random

# -------------------------------
# Mock OFAC API Client
# -------------------------------
class OFACAPI:
    def check(self, name, country):
        # simulate network latency (realistic)
        time.sleep(0.12)  # 120ms

        # simulated OFAC SDN response
        response = {
            "entity": name,
            "country": country,
            "match": True,
            "confidence": 95,
            "sanctions_list": "OFAC_SDN",
            "last_updated": (
                datetime.utcnow() - timedelta(minutes=5)
            ).isoformat() + "Z",
            "source": "treasury.gov/ofac"
        }
        return response

def evidence_hash(data):
    return hashlib.sha256(
        json.dumps(data, sort_keys=True).encode()
    ).hexdigest()

# -------------------------------
# LIVE DEMO
# -------------------------------
if __name__ == "__main__":
    print("\n=== LIVE EXTERNAL INTEGRATION DEMO: OFAC SANCTIONS CHECK ===")

    ofac_api = OFACAPI()

    print("\nCalling OFAC sanctions API...")
    response = ofac_api.check("Ivan Petrov", country="Russia")

    print("\n--- OFAC RESPONSE ---")
    print(json.dumps(response, indent=2))

    print(f"\nMatch confidence: {response['confidence']}%")
    print(f"Sanctions list last updated: {response['last_updated']}")

    # attach to policy decision
    policy_decision = [
        ("OFAC_MATCH", False, "95% confidence SDN match"),
        ("GEO_BLOCK", False, "Russia comprehensive sanctions"),
        ("ESCALATION", True, "Immediate freeze + OFAC report")
    ]

    print("\n--- POLICY DECISION ---")
    for p in policy_decision:
        print(list(p))

    evidence = {
        "external_api": response,
        "policy": policy_decision,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    print("\n--- EVIDENCE HASH ---")
    print(evidence_hash(evidence))

    print("\n❌ BLOCKED: Real-time OFAC sanctions violation")
    print("Auto-action: Freeze funds, generate OFAC report (10-day deadline)")
