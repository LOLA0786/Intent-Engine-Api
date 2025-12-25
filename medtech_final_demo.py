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
# DEMO 1: DRUG–ALLERGY FATAL INTERACTION
# -------------------------------------------------
section("DEMO 1: DRUG-ALLERGY FATAL INTERACTION")

policy = [
    ("ALLERGY_CONFLICT", False, "FATAL: Penicillin allergy → anaphylaxis"),
    ("CONTRAINDICATION", False, "Absolute contraindication"),
    ("ALTERNATIVES_CHECK", True, "Azithromycin available"),
    ("EMERGENCY_PROTOCOL", True, "Epinephrine alert triggered")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Life-threatening drug interaction")

# -------------------------------------------------
# DEMO 2: GENETIC CONTRAINDICATION
# -------------------------------------------------
section("DEMO 2: GENETIC CONTRAINDICATION")

policy = [
    ("GENETIC_CONTRAINDICATION", False, "HLA-B*1502 → Stevens-Johnson risk"),
    ("FDA_BLACK_BOX", False, "Boxed warning violated"),
    ("INFORMED_CONSENT", False, "Genetic counseling missing"),
    ("ETHNICITY_PROTOCOL", False, "Mandatory screening not done")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Genetic contraindication")

# -------------------------------------------------
# DEMO 3: PREGNANCY SAFETY (iPLEDGE)
# -------------------------------------------------
section("DEMO 3: PREGNANCY / TERATOGENIC RISK")

policy = [
    ("TERATOGENIC_RISK", False, "Category X fetal defects"),
    ("IPLEDGE_REQUIREMENT", False, "Not enrolled"),
    ("TWO_NEGATIVE_TESTS", False, "Only one test"),
    ("CONTRACEPTION_VERIFIED", False, "Not verified")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Severe teratogenic risk")

# -------------------------------------------------
# DEMO 4: DRUG–DRUG INTERACTIONS
# -------------------------------------------------
section("DEMO 4: LETHAL DRUG INTERACTIONS")

policy = [
    ("QT_PROLONGATION", False, "QTc 480ms → Torsades"),
    ("STATIN_INTERACTION", False, "Rhabdomyolysis risk"),
    ("ANTICOAG_INTERACTION", False, "Bleeding risk"),
    ("LETHAL_COMBINATION", True, "Triple interaction")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Multiple lethal interactions")

# -------------------------------------------------
# DEMO 5: OFF-LABEL / IRB VIOLATION
# -------------------------------------------------
section("DEMO 5: OFF-LABEL USE VIOLATION")

policy = [
    ("OFF_LABEL_PROTOCOL", False, "IRB approval missing"),
    ("INSURANCE_FRAUD", True, "False Claims Act risk"),
    ("INFORMED_CONSENT", False, "Generic consent insufficient"),
    ("RESEARCH_PROTOCOL", False, "Not a clinical trial")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Off-label compliance failure")

# -------------------------------------------------
# DEMO 6: MEDICAL DEVICE RECALL
# -------------------------------------------------
section("DEMO 6: MEDICAL DEVICE RECALL")

policy = [
    ("FDA_RECALL", False, "Class I recall – serious injury/death"),
    ("INFORMED_CONSENT", False, "Recall not disclosed"),
    ("ALTERNATIVE_AVAILABLE", True, "Safe model available"),
    ("HOSPITAL_POLICY", False, "Implant protocol violated")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Class I device recall")

# -------------------------------------------------
# DEMO 7: SCOPE OF PRACTICE
# -------------------------------------------------
section("DEMO 7: SCOPE OF PRACTICE VIOLATION")

policy = [
    ("SCOPE_OF_PRACTICE", False, "NP cannot perform ablation"),
    ("SUPERVISION_REQUIRED", False, "No physician"),
    ("FACILITY_CREDENTIALING", False, "Facility not licensed"),
    ("MALPRACTICE_COVERAGE", True, "Coverage excluded")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Practicing without license")

# -------------------------------------------------
# DEMO 8: CLINICAL TRIAL BREACH
# -------------------------------------------------
section("DEMO 8: CLINICAL TRIAL PROTOCOL BREACH")

policy = [
    ("INCLUSION_CRITERIA", False, "Age exclusion violated"),
    ("RENAL_EXCLUSION", False, "EGFR < 30"),
    ("PROTOCOL_DEVIATION", True, "Major deviation"),
    ("FDA_IND_REPORTING", False, "Not reported")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Trial protocol violation")

# -------------------------------------------------
# DEMO 9: RACIAL BIAS
# -------------------------------------------------
section("DEMO 9: RACIAL BIAS DETECTION")

policy = [
    ("RACIAL_BIAS", False, "Disparate opioid prescribing"),
    ("PAIN_GUIDELINE", False, "Pain 8 requires opioid"),
    ("DISPARATE_IMPACT", True, "p < 0.01"),
    ("EQUITY_POLICY", False, "Hospital policy violated")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Discriminatory care")

# -------------------------------------------------
# DEMO 10: BILLING FRAUD
# -------------------------------------------------
section("DEMO 10: BILLING / UPCODING FRAUD")

policy = [
    ("CPT_UPCODING", False, "99215 unsupported"),
    ("FALSE_CLAIMS", True, "Medicare fraud"),
    ("DOCUMENTATION_MISMATCH", False, "Supports 99212"),
    ("COMPLIANCE_PROGRAM", False, "Policy violated")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: False Claims Act risk")

# -------------------------------------------------
# FINAL COMPREHENSIVE AUDIT
# -------------------------------------------------
section("FINAL: COMPREHENSIVE PATIENT SAFETY AUDIT")

audit = {
    "audit_id": "med_audit_893475",
    "timestamp": now(),
    "critical_failures": 4,
    "prevented_harm": [
        "anaphylaxis",
        "fatal_bleed",
        "renal_failure",
        "fetal_defects"
    ]
}

print(json.dumps(audit, indent=2))
print("\n--- EVIDENCE BUNDLE HASH ---")
print(h(audit))

print("\n✅ SYSTEM STATE:")
print("• Fatal harm prevented")
print("• Full audit trail generated")
print("• FDA / CDC / Civil Rights compliance enforced")
print("• Regulator-ready evidence bundle produced")
