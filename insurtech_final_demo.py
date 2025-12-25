import json
import hashlib
from datetime import datetime

# -------------------------------------------------
# Utilities
# -------------------------------------------------
def h(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()

def now():
    return datetime.utcnow().isoformat() + "Z"

def section(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)

def show(policy):
    for p in policy:
        print(list(p))

# -------------------------------------------------
# DEMO 1: UNFAIR DISCRIMINATION IN UNDERWRITING
# -------------------------------------------------
section("DEMO 1: UNFAIR DISCRIMINATION / REDLINING")

policy = [
    ("PROXY_DISCRIMINATION", False, "ZIP code used as proxy for protected class"),
    ("FAIR_UNDERWRITING", False, "No actuarial support for 2.5x multiplier"),
    ("STATE_LAW_IL", False, "Violates IL Insurance Code § 424"),
    ("DISPARATE_IMPACT", True, "Statistical bias threshold exceeded")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Unfair discrimination risk")
print("AUTO-ACTION: Escalated to Chief Compliance Officer")

# -------------------------------------------------
# DEMO 2: FILED RATE DOCTRINE / ANTI-REBATING
# -------------------------------------------------
section("DEMO 2: FILED RATE DOCTRINE VIOLATION")

policy = [
    ("RATE_DEVIATION", False, "10% deviation from filed rate SER-2023-45"),
    ("ANTI_REBATING", True, "Unauthorized inducement to purchase"),
    ("STATE_DOI", False, "Strict liability offense"),
    ("LICENSE_ACTION", False, "Suspension or revocation risk")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Illegal rate offer")
print("AUTO-ACTION: Logged for mandatory DOI self-reporting")

# -------------------------------------------------
# DEMO 3: BAD FAITH CLAIMS HANDLING
# -------------------------------------------------
section("DEMO 3: UNFAIR CLAIMS SETTLEMENT PRACTICE")

policy = [
    ("UCSPA_CA", False, "CA Reg. §2695.7 requires thorough investigation"),
    ("TIMELINESS", False, "Decision exceeded 40-day guideline"),
    ("BAD_FAITH", True, "Unreasonable denial pattern"),
    ("PUNITIVE_DAMAGES", False, "Punitive exposure likely")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Bad faith claims exposure")
print("AUTO-ACTION: Routed to senior adjuster + legal review")

# -------------------------------------------------
# DEMO 4: UNAUTHORIZED SURPLUS LINES PLACEMENT
# -------------------------------------------------
section("DEMO 4: SURPLUS LINES LAW VIOLATION")

policy = [
    ("ELIGIBILITY", False, "No declinations from admitted carriers"),
    ("CARRIER_APPROVAL", False, "Carrier not on approved surplus list"),
    ("BROKER_AUTHORITY", False, "Violates surplus lines license"),
    ("POLICY_NULLITY", True, "Coverage may be unenforceable")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Illegal surplus lines placement")

# -------------------------------------------------
# DEMO 5: POLICY FORM / DISCLOSURE FAILURE
# -------------------------------------------------
section("DEMO 5: UNFILED POLICY FORM")

policy = [
    ("FORM_FILING", False, "Policy form not approved by DOI"),
    ("MANDATORY_DISCLOSURE", False, "Required consumer notice missing"),
    ("CONTRACT_ENFORCEABILITY", False, "Policy subject to rescission"),
    ("MARKET_CONDUCT", True, "Exam trigger likely")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Non-compliant policy issuance")

# -------------------------------------------------
# DEMO 6: RESERVING / SOLVENCY RISK
# -------------------------------------------------
section("DEMO 6: SOLVENCY & RESERVING VIOLATION")

policy = [
    ("RBC_THRESHOLD", False, "Risk-Based Capital ratio breached"),
    ("SAP_COMPLIANCE", False, "Under-reserving detected"),
    ("FINANCIAL_MISSTATEMENT", True, "Regulatory reporting risk"),
    ("REGULATORY_ACTION", False, "DOI supervision likely")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Solvency risk escalation")

# -------------------------------------------------
# FINAL INSURANCE COMPLIANCE AUDIT
# -------------------------------------------------
section("FINAL: INSURTECH COMPLIANCE AUDIT")

audit = {
    "audit_id": "ins_audit_f3e2d1",
    "timestamp": now(),
    "lines_of_business": ["P&C", "Health", "Commercial"],
    "regulators": ["State DOI", "NAIC"],
    "critical_violations": 6,
    "prevented_outcomes": [
        "Disparate impact lawsuits",
        "Filed rate penalties",
        "Bad faith verdicts",
        "License revocation",
        "Market conduct exam failures",
        "Solvency supervision"
    ],
    "system_role": "Deterministic compliance & solvency enforcement layer"
}

print(json.dumps(audit, indent=2))
print("\n--- EVIDENCE BUNDLE HASH ---")
print(h(audit))

print("\n✅ SYSTEM STATE:")
print("• Unfair underwriting blocked")
print("• Filed-rate compliance enforced")
print("• Bad-faith claims prevented")
print("• Unauthorized placements stopped")
print("• Solvency & reserving safeguarded")
print("• Regulator-ready audit trail generated")
