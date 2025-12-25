import json
import hashlib
from datetime import datetime

def hash_evidence(data):
    return hashlib.sha256(
        json.dumps(data, sort_keys=True).encode()
    ).hexdigest()

def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

def main_case():
    section("GOVERNMENT DEMO: DEFENSE CONTRACT AWARD AGENT")

    intent = {
        "action": "award_contract",
        "vendor": "TechNovate_LLC",
        "contract_value": 85000000,
        "classification": "ITAR_restricted",
        "vendor_ownership": ["foreign_investor_35%", "us_citizen_65%"],
        "required_certifications": ["CMMC_Level_3", "FedRAMP_High"],
        "data_type": "controlled_unclassified_info"
    }

    policy = [
        ("ITAR_COMPLIANCE", False, "Foreign ownership >25% in ITAR project"),
        ("BUY_AMERICAN_ACT", True, "51% US content verified"),
        ("CMMC_VERIFICATION", False, "Missing CMMC Level 3"),
        ("FEDRAMP_AUTHORIZATION", False, "No FedRAMP High ATO"),
        ("SECTION_889", True, "No banned Chinese telecom equipment"),
        ("COST_REALISM", False, "42% below independent government estimate")
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

    h = hash_evidence(payload)

    print("\n--- EVIDENCE HASH ---")
    print(h)

    print("\n❌ BLOCKED - Multiple procurement violations")
    print("National Security Flags:")
    print("1. ITAR violation: Foreign control of restricted technology")
    print("2. CMMC gap: Insufficient cybersecurity")
    print("3. FedRAMP gap: Unauthorized cloud")

    print("\n--- AUDIT TRAIL (FOIA-READY) ---")
    print(f"Timestamp: {payload['timestamp']}")
    print("Solicitation: FA8645-25-R-0123")
    print("Agency: Department of Defense")
    print('Blocking_Regulations: ["ITAR 22 CFR 120-130", "DFARS 252.204-7021", "FAR 52.204-25"]')
    print('Required_Remediation: ["CFIUS filing", "CMMC certification", "FedRAMP JAB review"]')
    print(f"Evidence_Hash: {h}")

def block_election():
    section("BLOCK 1: ELECTION SECURITY / VOTING SYSTEMS")

    policy = [
        ("EAC_CERTIFICATION", False, "Not EAC certified per HAVA"),
        ("FOREIGN_MANUFACTURING", True, "Components from non-trusted country"),
        ("SOFTWARE_PROVENANCE", False, "Libraries from banned entities"),
        ("AUDIT_TRAIL_REQUIREMENT", False, "No voter-verifiable paper trail")
    ]

    h = hash_evidence(policy)

    for p in policy:
        print(list(p))

    print("\n❌ BLOCKED - Election infrastructure security failure")
    print("Statutory Violation: Help America Vote Act (HAVA)")
    print("State Conflicts: Paper trail required in 28 states")
    print(f"Evidence_Hash: {h}")

def block_intelligence():
    section("BLOCK 2: INTELLIGENCE COMMUNITY AI ANALYSIS")

    policy = [
        ("ICD_503_COMPLIANCE", False, "SCI requires accredited SCIF"),
        ("CONTRACTOR_TIER", False, "Tier 3 insufficient for TS/SCI"),
        ("JWICS_ACCESS", True, "Valid PKI certificate"),
        ("TWO_PERSON_RULE", False, "Single analyst access"),
        ("DATA_SPILL_PREVENTION", False, "No TEMPEST controls")
    ]

    h = hash_evidence(policy)

    for p in policy:
        print(list(p))

    print("\n❌ BLOCKED - Intelligence directive violations")
    print("Compartment: TOP SECRET // SCI")
    print("Immediate Action: Security officer notification")
    print(f"Evidence_Hash: {h}")

def block_public_benefits():
    section("BLOCK 3: PUBLIC BENEFITS / SOCIAL SERVICES")

    policy = [
        ("PRIVACY_ACT_1974", False, "IRS data use exceeds stated purpose"),
        ("COMPUTER_MATCHING_ACT", True, "Matching agreement exists"),
        ("E_GOV_ACT", False, "Section 508 accessibility missing"),
        ("DATA_MINIMIZATION", False, "Bank records unnecessary"),
        ("ADVERSE_ACTION_NOTICE", True, "Notice logic implemented")
    ]

    h = hash_evidence(policy)

    for p in policy:
        print(list(p))

    print("\n❌ BLOCKED - Public benefits legal violations")
    print("Civil Rights Risk: Disparate impact exposure")
    print("Legal Exposure: 42 U.S.C. § 1983 class action")
    print(f"Evidence_Hash: {h}")

if __name__ == "__main__":
    main_case()
    block_election()
    block_intelligence()
    block_public_benefits()
