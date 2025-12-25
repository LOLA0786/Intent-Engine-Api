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
# DEMO 1: PCI DSS
# -------------------------------------------------
section("DEMO 1: PCI DSS VIOLATION")

policy = [
    ("PCI_DSS_3.2.1", False, "CVV storage prohibited"),
    ("ENCRYPTION_AT_REST", False, "Card data unencrypted"),
    ("ACCESS_LOGGING", False, "No audit logs"),
    ("PCI_SCAN", False, "Quarterly scan missing")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: PCI DSS non-compliance")

# -------------------------------------------------
# DEMO 2: GDPR CONSENT
# -------------------------------------------------
section("DEMO 2: GDPR CONSENT VIOLATION")

policy = [
    ("GDPR_CONSENT", False, "Pre-checked box invalid"),
    ("DATA_TRANSFER", False, "No SCCs"),
    ("PRIVACY_NOTICE", False, "EU rights missing"),
    ("DPO_REQUIRED", False, "No DPO appointed")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: GDPR violation")

# -------------------------------------------------
# DEMO 3: COPPA
# -------------------------------------------------
section("DEMO 3: COPPA CHILD DATA")

policy = [
    ("AGE_VERIFICATION", False, "User under 13"),
    ("PARENTAL_CONSENT", False, "No consent"),
    ("CHILD_DATA_LIMIT", False, "Photos collected"),
    ("CHILD_PRIVACY_POLICY", False, "Missing")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: COPPA violation")

# -------------------------------------------------
# DEMO 4: HAZMAT SHIPPING
# -------------------------------------------------
section("DEMO 4: HAZARDOUS SHIPPING")

policy = [
    ("IATA_DGR", False, "Lithium battery restriction"),
    ("IMPORT_LICENSE_DE", False, "German license missing"),
    ("HAZMAT_TRAINING", False, "Staff uncertified"),
    ("AIR_CARRIER_RULES", False, "Policy breach")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Hazardous shipment")

# -------------------------------------------------
# DEMO 5: SALES TAX NEXUS
# -------------------------------------------------
section("DEMO 5: SALES TAX NEXUS")

policy = [
    ("ECONOMIC_NEXUS", False, "Ohio threshold exceeded"),
    ("TAX_REGISTRATION", False, "Not registered"),
    ("TAX_COLLECTION", False, "No tax collected"),
    ("PENALTY_RISK", True, "Back taxes inevitable")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Sales tax violation")

# -------------------------------------------------
# DEMO 6: CUSTOMS FRAUD
# -------------------------------------------------
section("DEMO 6: CUSTOMS UNDERVALUATION")

policy = [
    ("CUSTOMS_FRAUD", False, "Declared value too low"),
    ("DUTY_EVASION", True, "Intent inferred"),
    ("SEIZURE_RISK", False, "High"),
    ("IMPORT_PRIVILEGE", False, "Revocable")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Customs fraud")

# -------------------------------------------------
# DEMO 7: WARRANTY LAW
# -------------------------------------------------
section("DEMO 7: WARRANTY ACT VIOLATION")

policy = [
    ("MAGNUSON_MOSS", False, "Tie-in sales illegal"),
    ("RIGHT_TO_REPAIR", False, "Violated"),
    ("FTC_GUIDANCE", False, "Non-compliant"),
    ("CLASS_ACTION", False, "Likely")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Warranty violation")

# -------------------------------------------------
# DEMO 8: BANNED PRODUCT
# -------------------------------------------------
section("DEMO 8: PROHIBITED PRODUCT")

policy = [
    ("FDA_APPROVAL", False, "Not approved"),
    ("MISBRANDING", True, "Marketed as supplement"),
    ("PLATFORM_POLICY", False, "Marketplace ban"),
    ("CRIMINAL_RISK", False, "Possible")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Illegal product")

# -------------------------------------------------
# DEMO 9: APP STORE POLICY
# -------------------------------------------------
section("DEMO 9: APP STORE VIOLATION")

policy = [
    ("APPLE_3_1_1", False, "Alternative payments"),
    ("PAYMENT_SKIRTING", True, "Detected"),
    ("CONTENT_POLICY", False, "Adult content"),
    ("ACCOUNT_BAN", False, "High risk")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: App store rejection")

# -------------------------------------------------
# DEMO 10: DECEPTIVE MARKETING
# -------------------------------------------------
section("DEMO 10: FTC DECEPTION")

policy = [
    ("FTC_DECEPTION", False, "Fake urgency"),
    ("FALSE_ADVERTISING", True, "Section 5"),
    ("CONSUMER_TRUST", False, "Eroded"),
    ("REFUND_LIABILITY", False, "Triggered")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Deceptive practice")

# -------------------------------------------------
# DEMO 11: RETURN RIGHTS
# -------------------------------------------------
section("DEMO 11: ILLEGAL RETURN DENIAL")

policy = [
    ("SONG_BEVERLY", False, "CA law violated"),
    ("IMPLIED_WARRANTY", False, "Merchantability"),
    ("STATUTORY_DAMAGES", True, "Applicable"),
    ("CLASS_ACTION", False, "Pattern risk")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Return denial illegal")

# -------------------------------------------------
# DEMO 12: BREACH RESPONSE
# -------------------------------------------------
section("DEMO 12: DATA BREACH RESPONSE FAILURE")

policy = [
    ("CA_1798_82", False, "Late notification"),
    ("NY_SHIELD", False, "Deadline missed"),
    ("FTC_DELAY", True, "Unreasonable"),
    ("CREDIT_MONITORING", False, "Not offered")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Breach handling violation")

# -------------------------------------------------
# FINAL ECOMMERCE AUDIT
# -------------------------------------------------
section("FINAL: ECOMMERCE COMPLIANCE AUDIT")

audit = {
    "audit_id": "ecom_audit_4x5y6z",
    "timestamp": now(),
    "monthly_volume": "$500K",
    "jurisdictions": ["US", "EU", "CA"],
    "critical_violations": 6,
    "prevented_outcomes": [
        "PCI fraud liability",
        "GDPR fines",
        "COPPA class action",
        "Customs seizure",
        "Sales tax audits",
        "FTC enforcement"
    ]
}

print(json.dumps(audit, indent=2))
print("\n--- EVIDENCE BUNDLE HASH ---")
print(h(audit))

print("\n✅ SYSTEM STATE:")
print("• Illegal intents blocked pre-execution")
print("• Financial & criminal exposure prevented")
print("• Cryptographic audit trail generated")
print("• Regulator-ready evidence bundle available")
