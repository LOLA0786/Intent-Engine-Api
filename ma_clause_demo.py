import json
import hashlib
from datetime import datetime

def evidence_hash(data):
    return hashlib.sha256(
        json.dumps(data, sort_keys=True).encode()
    ).hexdigest()

def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

def main_case():
    section("LEGALTECH DEMO: MERGER CLAUSE VALIDATION")

    intent = {
        "action": "approve_legal_clause",
        "clause_type": "change_of_control",
        "jurisdiction": "california",
        "deal_size": 2500000000,
        "parties": ["public_company", "pe_firm"],
        "contains_fiduciary_duty": True,
        "contains_termination_fee": False
    }

    policy = [
        ("SEC_8K_REQUIREMENT", True, "Public company disclosure triggered"),
        ("HART_SCOTT_RODINO", False, "$2.5B exceeds $101M HSR threshold"),
        ("CALIFORNIA_APPROVAL", True, "CA Secretary of State filing required"),
        ("FIDUCIARY_OUT_CLAUSE", False, "Missing fiduciary duty termination right"),
        ("TERMINATION_FEE_CAP", True, "No fee specified - review required"),
        ("MATERIAL_ADVERSE_CHANGE", False, "MAC clause definition insufficient")
    ]

    payload = {
        "intent": intent,
        "policy": policy,
        "timestamp": datetime.utcnow().isoformat()
    }

    print("\n--- INTENT ---")
    print(json.dumps(intent, indent=2))

    print("\n--- POLICY DECISION ---")
    for p in policy:
        print(list(p))

    h = evidence_hash(payload)

    print("\n--- EVIDENCE HASH ---")
    print(h)

    print("\n❌ BLOCKED - Critical legal deficiencies")
    print("Required Actions:")
    print("1. File HSR Notification (45-day waiting period)")
    print("2. Strengthen MAC clause per Delaware precedent")
    print("3. Add fiduciary duty termination provision")
    print("4. Specify termination fee or remove entirely")

    print("\n--- LEGAL AUDIT TRAIL ---")
    print(f"Timestamp: {payload['timestamp']}")
    print("Clause_ID: COC_7892_FINAL")
    print('Deal: "Project Atlas"')
    print('Jurisdictions: ["CA", "DE", "Federal"]')
    print("Blocking_Issues: 3 of 6 checks failed")
    print('Legal_Precedents_Cited: ["Revlon v. MacAndrews", "Omnicare v. NCS"]')
    print('Regulatory_Flags: ["HSR Threshold", "SEC Rule 13e-3"]')
    print(f"Evidence_Hash: {h}")

def block_regulatory():
    section("BLOCK 1: REGULATORY THRESHOLD VIOLATION")

    policy = [
        ("CFIUS_REVIEW", False, "Foreign ownership > 20% in critical tech"),
        ("EXON_FLORIO", True, "Presidential suspension authority"),
        ("DATA_PRIVACY_REVIEW", False, "GDPR transfer assessment missing"),
        ("IP_EXPORT_CONTROL", False, "Encryption tech requires BIS license")
    ]

    h = evidence_hash(policy)

    for p in policy:
        print(list(p))

    print("\n❌ BLOCKED - National security & export control violations")
    print("Immediate Action: File CFIUS declaration (45-day review)")
    print("Legal Risk: Transaction unwind + $50M+ penalties")
    print(f"Evidence_Hash: {h}")

def block_fiduciary():
    section("BLOCK 2: CONFLICT OF INTEREST / FIDUCIARY BREACH")

    policy = [
        ("DUTY_OF_LOYALTY", False, "CEO private fund party to deal"),
        ("ENTIRE_FAIRNESS_REVIEW", False, "No independent committee"),
        ("SPECIAL_COMMITTEE", False, "Missing disinterested directors"),
        ("FAIRNESS_OPINION", True, "Required but not obtained")
    ]

    h = evidence_hash(policy)

    for p in policy:
        print(list(p))

    print("\n❌ BLOCKED - Corporate governance failure")
    print("Fiduciary Breach: Delaware duty of loyalty violation")
    print("Escalation: Immediate board counsel notification")
    print(f"Evidence_Hash: {h}")

def block_antitrust():
    section("BLOCK 3: ANTITRUST / MARKET CONCENTRATION")

    policy = [
        ("HHI_CALCULATION", False, "Post-merger HHI > 2500"),
        ("MARKET_SHARE", False, "Combined 75% exceeds DOJ safe harbor"),
        ("PRICE_EFFECT_ANALYSIS", False, "Econometric model missing"),
        ("EFFICIENCIES_DEFENSE", True, "Claimed but unsubstantiated")
    ]

    h = evidence_hash(policy)

    for p in policy:
        print(list(p))

    print("\n❌ BLOCKED - Presumptive antitrust violation")
    print("DOJ / FTC Challenge Probability: 85%+")
    print("Required: Upfront buyer or divestiture plan")
    print(f"Evidence_Hash: {h}")

if __name__ == "__main__":
    main_case()
    block_regulatory()
    block_fiduciary()
    block_antitrust()
