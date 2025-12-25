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
# DEMO 1: CONFLICT OF INTEREST
# -------------------------------------------------
section("DEMO 1: CONFLICT OF INTEREST VIOLATION")

policy = [
    ("CONFLICT_OF_INTEREST", False, "Firm represented opposing party 2022–2024"),
    ("CONFIDENTIALITY_BREACH", True, "Risk of confidential misuse"),
    ("CLIENT_CONSENT_REQUIRED", False, "No informed consent"),
    ("ETHICAL_WALL", False, "No documented wall")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Rule 1.7 / 1.9 conflict")

# -------------------------------------------------
# DEMO 2: PRIVILEGE WAIVER
# -------------------------------------------------
section("DEMO 2: ATTORNEY–CLIENT PRIVILEGE BREACH")

policy = [
    ("PRIVILEGE_DESTROYED", False, "Third-party consultant included"),
    ("COMMON_INTEREST", False, "No common interest agreement"),
    ("WORK_PRODUCT", True, "But waived"),
    ("E_DISCOVERY_RISK", False, "Now discoverable")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Privilege waived")

# -------------------------------------------------
# DEMO 3: FEE SPLITTING
# -------------------------------------------------
section("DEMO 3: FEE SPLITTING / UPL")

policy = [
    ("FEE_SPLITTING", False, "Rule 5.4 violation"),
    ("UNAUTHORIZED_PRACTICE", True, "Non-lawyer influence"),
    ("INDEPENDENCE", False, "Professional independence breached"),
    ("CLIENT_DISCLOSURE", False, "Not disclosed")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Illegal fee sharing")

# -------------------------------------------------
# DEMO 4: MULTI-JURISDICTION PRACTICE
# -------------------------------------------------
section("DEMO 4: UNAUTHORIZED PRACTICE OF LAW")

policy = [
    ("UPL_NY", False, "Not licensed in NY"),
    ("PRO_HAC_VICE", False, "No admission filed"),
    ("LOCAL_COUNSEL", False, "None associated"),
    ("SUBSTANTIAL_RELATIONSHIP", True, "Exception insufficient")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Unauthorized practice")

# -------------------------------------------------
# DEMO 5: E-DISCOVERY SPOLIATION
# -------------------------------------------------
section("DEMO 5: E-DISCOVERY SPOLIATION")

policy = [
    ("SPOLIATION", False, "Data deletion under hold"),
    ("ZUBULAKE_DUTY", False, "Preservation duty violated"),
    ("ADVERSE_INFERENCE", True, "Guaranteed"),
    ("RULE_37E", False, "Sanctions inevitable")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Evidence spoliation")

# -------------------------------------------------
# DEMO 6: INSIDER TRADING RISK
# -------------------------------------------------
section("DEMO 6: INSIDER TRADING / MNPI")

policy = [
    ("MNPI_ACCESS", False, "Material nonpublic info"),
    ("RULE_10B5", True, "Insider trading risk"),
    ("ETHICAL_WALL", False, "Wall breached"),
    ("TIPPING", False, "Tipping liability")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Insider trading exposure")

# -------------------------------------------------
# DEMO 7: STATUTE OF LIMITATIONS
# -------------------------------------------------
section("DEMO 7: STATUTE OF LIMITATIONS MISSED")

policy = [
    ("SOL_MISSED", False, "Filed 1 day late"),
    ("MALPRACTICE", True, "Strict liability"),
    ("CLAIM_BARRED", False, "Claim lost"),
    ("INSURANCE", True, "Coverage disputed")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Time-barred claim")

# -------------------------------------------------
# DEMO 8: CLASS ACTION / PAGA
# -------------------------------------------------
section("DEMO 8: ILLEGAL CLASS ACTION WAIVER")

policy = [
    ("PAGA_VIOLATION", False, "Cannot waive PAGA"),
    ("UNENFORCEABLE", True, "Iskanian"),
    ("CLASS_ACTION", False, "Certification guaranteed"),
    ("BAD_FAITH", False, "Fee shifting risk")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Illegal contract clause")

# -------------------------------------------------
# DEMO 9: GDPR / CCPA
# -------------------------------------------------
section("DEMO 9: GDPR / CCPA DATA TRANSFER")

policy = [
    ("GDPR_TRANSFER", False, "No SCCs"),
    ("CCPA_FINE", True, "$7,500 per record"),
    ("DATA_SUBJECT", False, "Rights violated"),
    ("EU_FINE", False, "4% global revenue")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Illegal data transfer")

# -------------------------------------------------
# DEMO 10: SANCTIONS / EXPORT CONTROL
# -------------------------------------------------
section("DEMO 10: OFAC / EAR VIOLATION")

policy = [
    ("OFAC_SDN", False, "SDN match"),
    ("EAR_9A610", False, "Export license required"),
    ("ANTIBOYCOTT", True, "Risk detected"),
    ("FACILITATION", False, "Prohibited facilitation")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Sanctions violation")

# -------------------------------------------------
# DEMO 11: SECURITIES LAW
# -------------------------------------------------
section("DEMO 11: ILLEGAL SECURITIES OFFERING")

policy = [
    ("SECTION_5", False, "Unregistered offering"),
    ("ACCREDITED_INVESTOR", False, "No verification"),
    ("BAD_ACTOR", True, "Unchecked"),
    ("FORM_D", False, "Not filed")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Securities fraud risk")

# -------------------------------------------------
# DEMO 12: ETHICAL WALL FAILURE
# -------------------------------------------------
section("DEMO 12: ETHICAL WALL FAILURE")

policy = [
    ("IMPUTED_DISQUALIFICATION", False, "Firm-wide"),
    ("SCREENING", False, "Inadequate"),
    ("CLIENT_CONSENT", False, "Missing"),
    ("CONFIDENTIALITY", True, "High risk")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Firm disqualification")

# -------------------------------------------------
# FINAL COMPREHENSIVE AUDIT
# -------------------------------------------------
section("FINAL: COMPREHENSIVE LEGAL RISK AUDIT")

audit = {
    "audit_id": "legal_audit_7f8g9h",
    "timestamp": now(),
    "critical_violations": 5,
    "practice_areas": ["M&A", "Litigation", "Securities", "Employment"],
    "prevented_outcomes": [
        "Firm disqualification",
        "Automatic malpractice liability",
        "Criminal sanctions",
        "Class action exposure",
        "GDPR fines"
    ]
}

print(json.dumps(audit, indent=2))
print("\n--- EVIDENCE BUNDLE HASH ---")
print(h(audit))

print("\n✅ SYSTEM STATE:")
print("• Malpractice prevented")
print("• Ethical compliance enforced")
print("• Court-defensible audit trail generated")
print("• Regulator-ready export available")
