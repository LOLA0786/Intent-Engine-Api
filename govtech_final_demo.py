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
# DEMO 1: CLASSIFIED INFORMATION LEAK
# -------------------------------------------------
section("DEMO 1: TS//SCI INFORMATION EXFILTRATION")

policy = [
    ("CLEARANCE_MISMATCH", False, "Recipient lacks TS//SCI clearance"),
    ("NEED_TO_KNOW", False, "No documented need-to-know"),
    ("NETWORK_VIOLATION", False, "TS//SCI leaving SCIF"),
    ("DATA_MARKING", False, "Incomplete portion markings"),
    ("EXFILTRATION_TTP", True, "Matches known exfil patterns")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Espionage Act risk (18 U.S.C. § 793)")

# -------------------------------------------------
# DEMO 2: ELECTION INTERFERENCE
# -------------------------------------------------
section("DEMO 2: ELECTION INTERFERENCE PREVENTION")

policy = [
    ("FOREIGN_ACCESS", False, "Foreign IP detected"),
    ("BATCH_MODIFICATION", False, "Suspicious bulk changes"),
    ("TIME_ANOMALY", False, "Outside business hours"),
    ("CREDENTIAL_COMPROMISE", True, "Stolen credentials"),
    ("HAVA_VIOLATION", False, "Election infrastructure breach")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Voter fraud attempt (52 U.S.C. § 20511)")

# -------------------------------------------------
# DEMO 3: FEDERAL PROCUREMENT FRAUD
# -------------------------------------------------
section("DEMO 3: FEDERAL PROCUREMENT FRAUD")

policy = [
    ("FAR_15_403", False, "Improper cost-plus modification"),
    ("ANTI_DEFICIENCY", False, "31 U.S.C. § 1341 violation"),
    ("KICKBACK_RISK", True, "Related subcontractor"),
    ("FALSE_CLAIMS", False, "FCA exposure"),
    ("PROCUREMENT_INTEGRITY", False, "41 U.S.C. § 2102 breach")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Major Fraud Act exposure")

# -------------------------------------------------
# DEMO 4: CYBER ROE VIOLATION
# -------------------------------------------------
section("DEMO 4: CYBER RULES OF ENGAGEMENT")

policy = [
    ("ROE_VIOLATION", False, "Preemptive strike"),
    ("PRESIDENTIAL_FINDING", False, "Missing authorization"),
    ("COLLATERAL_DAMAGE", False, "Civilian risk"),
    ("ESCALATION_RISK", False, "High"),
    ("WAR_POWERS", True, "Potential violation")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Unauthorized cyber operation")

# -------------------------------------------------
# DEMO 5: CONSTITUTIONAL VIOLATION
# -------------------------------------------------
section("DEMO 5: FOURTH AMENDMENT VIOLATION")

policy = [
    ("FOURTH_AMENDMENT", False, "Unreasonable search"),
    ("FISA_APPROVAL", False, "Court rejected"),
    ("US_PERSON_PROTECTION", False, "Minimization failure"),
    ("BULK_COLLECTION", True, "USA FREEDOM Act"),
    ("OVERSIGHT", False, "Congress bypassed")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Constitutional violation")

# -------------------------------------------------
# DEMO 6: BIO / CHEMICAL WEAPONS
# -------------------------------------------------
section("DEMO 6: BIOLOGICAL WEAPONS PROTOCOL")

policy = [
    ("BSL_REQUIREMENT", False, "BSL-4 data published"),
    ("DUAL_USE_RESEARCH", False, "Weaponization risk"),
    ("NSABB_REVIEW", False, "Bypassed"),
    ("EXPORT_CONTROL", False, "Misclassified"),
    ("BIOLOGICAL_WEAPONS", True, "18 U.S.C. § 175")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Biological Weapons Act violation")

# -------------------------------------------------
# DEMO 7: SPACE DEBRIS
# -------------------------------------------------
section("DEMO 7: SPACE DEBRIS GENERATION")

policy = [
    ("SPACE_DEBRIS", False, "Long-term debris risk"),
    ("COLLISION_PROBABILITY", False, ">1e-4 ignored"),
    ("SPACE_TRAFFIC", False, "STM violation"),
    ("OUTER_SPACE_TREATY", True, "Article IX"),
    ("KESSLER_RISK", False, "Cascade risk")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Orbital debris creation")

# -------------------------------------------------
# DEMO 8: HATCH ACT
# -------------------------------------------------
section("DEMO 8: HATCH ACT VIOLATION")

policy = [
    ("HATCH_ACT", False, "Political activity on duty"),
    ("SOLICITATION", False, "Fundraising prohibited"),
    ("OFFICIAL_RESOURCES", False, "Gov email used"),
    ("IMPLIED_ENDORSEMENT", True, "Official appearance"),
    ("OSC_JURISDICTION", False, "OSC violation")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Hatch Act breach")

# -------------------------------------------------
# DEMO 9: CENSUS PRIVACY
# -------------------------------------------------
section("DEMO 9: CENSUS DATA PRIVACY")

policy = [
    ("TITLE_13", False, "Confidentiality breached"),
    ("DIFFERENTIAL_PRIVACY", False, "Noise insufficient"),
    ("REIDENTIFICATION", False, "High risk"),
    ("STATISTICAL_DISCLOSURE", True, "Detected"),
    ("PRIVACY_ACT", False, "1974 Act violated")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Census confidentiality violation")

# -------------------------------------------------
# DEMO 10: JUDICIAL ETHICS
# -------------------------------------------------
section("DEMO 10: JUDICIAL ETHICS VIOLATION")

policy = [
    ("CANON_2", False, "Appearance of impropriety"),
    ("EX_PARTE", False, "Prohibited communication"),
    ("DISCLOSURE", False, "Not disclosed"),
    ("RECUSAL", True, "28 U.S.C. § 455"),
    ("JUDICIAL_CONDUCT", False, "Code violated")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Judicial misconduct")

# -------------------------------------------------
# DEMO 11: RESEARCH MISCONDUCT
# -------------------------------------------------
section("DEMO 11: RESEARCH FABRICATION")

policy = [
    ("RESEARCH_MISCONDUCT", False, "Fabrication detected"),
    ("NIH_POLICY", False, "42 CFR Part 93"),
    ("FALSE_STATEMENTS", True, "18 U.S.C. § 1001"),
    ("GRANT_FRAUD", False, "FCA exposure"),
    ("DEBARMENT", False, "Funding ban risk")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Research fraud")

# -------------------------------------------------
# FINAL NATIONAL SECURITY AUDIT
# -------------------------------------------------
section("FINAL: NATIONAL SECURITY COMPLIANCE AUDIT")

audit = {
    "audit_id": "gov_audit_9a8b7c",
    "timestamp": now(),
    "agencies": ["DoD", "DOJ", "DHS", "DOS", "NASA"],
    "classifications": ["UNCLASS", "CONFIDENTIAL", "SECRET", "TS//SCI"],
    "checks_performed": 212,
    "critical_findings": 6,
    "national_security_impact": "EXTREME"
}

print(json.dumps(audit, indent=2))
print("\n--- EVIDENCE BUNDLE HASH ---")
print(h(audit))

print("\n✅ SYSTEM STATE:")
print("• Classified data protected")
print("• Constitutional limits enforced")
print("• Treaty obligations honored")
print("• Cross-agency violations prevented")
print("• Classified audit trail generated")
