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
# DEMO 1: DARK PATTERNS / DECEPTIVE UX (FTC)
# -------------------------------------------------
section("DEMO 1: DARK PATTERNS & DECEPTIVE UX")

policy = [
    ("FTC_DARK_PATTERN", False, "Forced continuity detected"),
    ("FALSE_URGENCY", False, "Fake countdown timer"),
    ("CONSUMER_CONSENT", False, "Consent not freely given"),
    ("SECTION_5", True, "FTC deceptive practice")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Deceptive consumer experience")
print("AUTO-ACTION: UX flow frozen + legal review")

# -------------------------------------------------
# DEMO 2: SUBSCRIPTION & AUTO-RENEWAL VIOLATION
# -------------------------------------------------
section("DEMO 2: SUBSCRIPTION LAW VIOLATION")

policy = [
    ("AUTO_RENEWAL_LAW", False, "No clear cancellation path"),
    ("BILLING_DISCLOSURE", False, "Material terms hidden"),
    ("CONSENT_LOGGING", False, "Affirmative consent missing"),
    ("STATE_AG_RISK", True, "State AG enforcement likely")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Illegal subscription practice")

# -------------------------------------------------
# DEMO 3: PRICING MANIPULATION / FALSE DISCOUNTS
# -------------------------------------------------
section("DEMO 3: FALSE PRICING & DISCOUNT FRAUD")

policy = [
    ("REFERENCE_PRICE", False, "Inflated list price"),
    ("DISCOUNT_AUTHENTICITY", False, "Never-sold-at price"),
    ("FTC_PRICING_RULES", False, "False savings claim"),
    ("CLASS_ACTION", True, "High likelihood")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Pricing deception")

# -------------------------------------------------
# DEMO 4: PAYMENT / PCI / REFUND FAILURE
# -------------------------------------------------
section("DEMO 4: PAYMENT & REFUND NON-COMPLIANCE")

policy = [
    ("PCI_DSS", False, "Payment data mishandled"),
    ("REFUND_TIMELINE", False, "Delayed beyond statutory window"),
    ("CHARGEBACK_RISK", True, "Network penalties triggered"),
    ("CARD_NETWORK_RULES", False, "Visa/Mastercard violation")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Payment compliance failure")

# -------------------------------------------------
# DEMO 5: ADVERTISING & INFLUENCER DISCLOSURE
# -------------------------------------------------
section("DEMO 5: ADVERTISING & INFLUENCER VIOLATION")

policy = [
    ("FTC_ENDORSEMENT", False, "Sponsored content undisclosed"),
    ("INFLUENCER_GUIDELINES", False, "No #ad disclosure"),
    ("PLATFORM_POLICY", False, "Meta/Google violation"),
    ("BRAND_LIABILITY", True, "Advertiser responsible")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Illegal advertising")

# -------------------------------------------------
# DEMO 6: DATA PRIVACY (GDPR / CCPA)
# -------------------------------------------------
section("DEMO 6: CONSUMER DATA PRIVACY VIOLATION")

policy = [
    ("GDPR_CONSENT", False, "Implicit consent invalid"),
    ("CCPA_OPT_OUT", False, "Do Not Sell ignored"),
    ("DATA_MINIMIZATION", False, "Excessive tracking"),
    ("REGULATORY_FINE", True, "Enforcement exposure")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Privacy law violation")

# -------------------------------------------------
# DEMO 7: RETURNS & CONSUMER RIGHTS
# -------------------------------------------------
section("DEMO 7: ILLEGAL RETURN DENIAL")

policy = [
    ("CONSUMER_RIGHTS", False, "Statutory return denied"),
    ("DEFECTIVE_GOODS", False, "Mandatory refund required"),
    ("STATE_LAW", False, "CA/EU violation"),
    ("REPUTATIONAL_DAMAGE", True, "Brand trust erosion")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Consumer rights violation")

# -------------------------------------------------
# DEMO 8: CROSS-BORDER SHIPPING & DUTY FRAUD
# -------------------------------------------------
section("DEMO 8: CROSS-BORDER SHIPPING FRAUD")

policy = [
    ("CUSTOMS_DECLARATION", False, "Undervalued shipment"),
    ("HS_CODE", False, "Incorrect classification"),
    ("DUTY_EVASION", True, "Intent inferred"),
    ("SHIPMENT_SEIZURE", False, "High probability")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Customs & duty fraud")

# -------------------------------------------------
# FINAL D2C COMPLIANCE AUDIT
# -------------------------------------------------
section("FINAL: D2C COMPLIANCE AUDIT")

audit = {
    "audit_id": "d2c_audit_z9y8x7",
    "timestamp": now(),
    "channels": ["Web", "Mobile", "Marketplace", "Social Commerce"],
    "jurisdictions": ["US", "EU", "UK", "CA"],
    "critical_violations": 8,
    "prevented_outcomes": [
        "FTC enforcement",
        "State AG lawsuits",
        "Payment network bans",
        "Platform de-listing",
        "Privacy fines",
        "Chargeback death spiral",
        "Brand trust collapse"
    ],
    "system_role": "Consumer protection & platform compliance enforcement layer"
}

print(json.dumps(audit, indent=2))
print("\n--- EVIDENCE BUNDLE HASH ---")
print(h(audit))

print("\n✅ SYSTEM STATE:")
print("• Dark patterns blocked")
print("• Subscription abuse prevented")
print("• Pricing integrity enforced")
print("• Payments & refunds compliant")
print("• Ads & influencers regulated")
print("• Consumer trust protected")
print("• Regulator-ready audit trail generated")
