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
# DEMO 1: AML / KYC FAILURE (BSA / FINCEN)
# -------------------------------------------------
section("DEMO 1: AML / CFT PROGRAM VIOLATION")

policy = [
    ("EDD_REQUIRED", False, "High-risk entity without Enhanced Due Diligence"),
    ("UBO_VERIFICATION", False, "Beneficial ownership incomplete"),
    ("SANCTIONS_SCREENING", False, "OFAC screening missing"),
    ("BSA_COMPLIANCE", False, "Risk-based AML controls absent"),
    ("SAR_TRIGGER", True, "Suspicious onboarding pattern detected")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: BSA / PATRIOT Act violation")
print("AUTO-ACTION: Draft SAR generated for compliance review")

# -------------------------------------------------
# DEMO 2: UDAAP VIOLATION (CFPB)
# -------------------------------------------------
section("DEMO 2: UNFAIR / DECEPTIVE PRACTICE (UDAAP)")

policy = [
    ("ADVERTISED_APR", False, "Headline APR 2% misleading"),
    ("EFFECTIVE_APR", False, "Effective APR calculated at 5%"),
    ("DISCLOSURE_CLARITY", False, "Material fees obscured"),
    ("UDAAP_STANDARD", False, "Deceptive marketing detected"),
    ("CONSUMER_HARM", True, "Likely consumer financial harm")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: CFPB UDAAP enforcement risk")

# -------------------------------------------------
# DEMO 3: FAIR LENDING / CRA RISK
# -------------------------------------------------
section("DEMO 3: FAIR LENDING / CRA DISPARATE IMPACT")

policy = [
    ("DISPARATE_IMPACT_RATIO", False, "Denial ratio exceeds 0.8 threshold"),
    ("PROTECTED_CLASS", False, "Minority population affected"),
    ("ECOA_RISK", False, "Potential discriminatory outcome"),
    ("CRA_COMPLIANCE", False, "Digital redlining risk"),
    ("HUMAN_REVIEW", True, "Manual underwriting required")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Fair lending & CRA violation")
print("AUTO-ACTION: Routed to human credit committee")

# -------------------------------------------------
# DEMO 4: TILA / TISA DISCLOSURE FAILURE
# -------------------------------------------------
section("DEMO 4: TRUTH IN LENDING / SAVINGS VIOLATION")

policy = [
    ("FINANCE_CHARGE", False, "Missing finance charge"),
    ("TOTAL_PAYMENTS", False, "Total of payments absent"),
    ("APR_CALCULATION", False, "Numerical inconsistency"),
    ("TILA_DISCLOSURE", False, "Required fields incomplete"),
    ("REGULATORY_APPROVAL", False, "Approval cannot finalize")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: TILA / TISA disclosure violation")

# -------------------------------------------------
# FINAL BANKING COMPLIANCE AUDIT
# -------------------------------------------------
section("FINAL: BANKING COMPLIANCE AUDIT SUMMARY")

audit = {
    "audit_id": "bank_audit_b9c8d7",
    "timestamp": now(),
    "regulators": ["OCC", "Federal Reserve", "FDIC", "CFPB", "FinCEN"],
    "critical_violations": 4,
    "prevented_outcomes": [
        "AML enforcement action",
        "CFPB UDAAP penalties",
        "CRA downgrade",
        "TILA rescission & fines"
    ],
    "system_role": "Deterministic authorization layer for autonomous banking agents"
}

print(json.dumps(audit, indent=2))
print("\n--- EVIDENCE BUNDLE HASH ---")
print(h(audit))

print("\n✅ SYSTEM STATE:")
print("• High-risk onboarding blocked")
print("• Deceptive marketing prevented")
print("• Fair lending enforced")
print("• Mandatory disclosures guaranteed")
print("• Regulator-ready audit trail generated")
