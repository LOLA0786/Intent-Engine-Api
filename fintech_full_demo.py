import json
import hashlib
from datetime import datetime

def h(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def section(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)

def show(policy):
    for p in policy:
        print(list(p))

# ============================================================
# DEMO 1: PAYMENTS FRAUD ENGINE
# ============================================================
def demo_fraud():
    section("DEMO 1: PAYMENTS FRAUD ENGINE")

    intent = {
        "action": "process_payment",
        "amount": 9500,
        "card_country": "Nigeria",
        "ip_country": "Russia",
        "velocity": "15 tx / 60 min",
        "merchant_category": "digital_goods"
    }

    policy = [
        ("AML_STRUCTURING", False, "Just-under-$10K structuring pattern"),
        ("GEO_MISMATCH", False, "Card vs IP mismatch"),
        ("VELOCITY_ALERT", False, "Exceeds 10 tx/hour"),
        ("HIGH_RISK_MCC", True, "Digital goods fraud-prone")
    ]

    print("\n--- INTENT ---")
    print(json.dumps(intent, indent=2))
    print("\n--- POLICY DECISION ---")
    show(policy)

    print("\n--- EVIDENCE HASH ---")
    print(h(policy))

    print("\n❌ BLOCKED: Multi-layer fraud detected")
    print("Auto-action: FinCEN SAR + freeze merchant")

# ============================================================
# DEMO 2: FAIR LENDING / BIAS
# ============================================================
def demo_fair_lending():
    section("DEMO 2: FAIR LENDING VIOLATION")

    policy = [
        ("FAIR_LENDING_TEST", False, "72% denial vs 28% baseline"),
        ("ECOA_COMPLIANCE", False, "Zipcode as race proxy"),
        ("ALTERNATIVE_DATA", True, "Cash-flow verified"),
        ("REDLINING_CHECK", False, "Historical discrimination pattern")
    ]

    show(policy)
    print("\n--- EVIDENCE HASH ---")
    print(h(policy))

    print("\n❌ BLOCKED: Reg B / ECOA risk")
    print("Required: Manual review + disparate impact report")

# ============================================================
# DEMO 3: TRADING BEST EXECUTION
# ============================================================
def demo_trading():
    section("DEMO 3: BEST EXECUTION FAILURE")

    policy = [
        ("BEST_EXECUTION", False, "Inferior price by $0.01/share"),
        ("CONFLICT_INTEREST", False, "Internal routing rebate"),
        ("REG_NMS_605", False, "Order protection violation"),
        ("DISCLOSURE_REQUIRED", True, "Not disclosed to client")
    ]

    show(policy)
    print("\n--- EVIDENCE HASH ---")
    print(h(policy))

    print("\n❌ BLOCKED: Best execution breach")
    print("Penalty: Client restitution + SEC report")

# ============================================================
# DEMO 4: REAL-TIME SANCTIONS
# ============================================================
def demo_sanctions():
    section("DEMO 4: REAL-TIME SANCTIONS SCREENING")

    policy = [
        ("OFAC_MATCH", False, "95% match to new SDN"),
        ("PEP_SCREEN", False, "Politically exposed person"),
        ("GEO_BLOCK", False, "Russia comprehensive sanctions"),
        ("RELATIONSHIP_CHECK", True, "No prior relationship")
    ]

    show(policy)
    print("\n--- EVIDENCE HASH ---")
    print(h(policy))

    print("\n❌ BLOCKED: OFAC violation (5 min fresh)")
    print("Auto-action: Freeze funds + OFAC report")

# ============================================================
# DEMO 5: INSURANCE CLAIMS BIAS
# ============================================================
def demo_insurance():
    section("DEMO 5: INSURANCE CLAIMS BIAS")

    policy = [
        ("UNFAIR_DISCRIMINATION", False, "Catastrophe area bias"),
        ("CONSTRUCTIVE_DENIAL", True, "Policy sold then denied"),
        ("BAD_FAITH_CHECK", False, "Systematic denial pattern"),
        ("STATE_EMERGENCY_ORDER", False, "FL hurricane rule violated")
    ]

    show(policy)
    print("\n--- EVIDENCE HASH ---")
    print(h(policy))

    print("\n❌ BLOCKED: Bad faith insurance risk")
    print("Required: Re-evaluate claims + regulator notice")

# ============================================================
# ULTIMATE COMBINED RISK TEST
# ============================================================
def demo_combined():
    section("ULTIMATE TEST: COMBINED FINANCIAL RISK")

    policy = [
        ("AML_STRUCTURING", False, "Repeated near-threshold wires"),
        ("SANCTIONS_MATCH", False, "95% SDN owner match"),
        ("CRYPTO_MSB_CHECK", False, "Unregistered MSB"),
        ("GEOGRAPHIC_RISK", False, "High-risk jurisdiction"),
        ("VELOCITY_MONITOR", False, "9th tx this week"),
        ("SHELL_COMPANY", False, "No operating history")
    ]

    show(policy)
    print("\n--- EVIDENCE HASH ---")
    print(h(policy))

    print("\n❌ BLOCKED: Multi-regulator failure")
    print("Triggered: AML + OFAC + MSB + Geo-risk")

# ============================================================
if __name__ == "__main__":
    demo_fraud()
    demo_fair_lending()
    demo_trading()
    demo_sanctions()
    demo_insurance()
    demo_combined()
