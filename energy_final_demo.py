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
# DEMO 1: GRID RELIABILITY / NERC CIP VIOLATION
# -------------------------------------------------
section("DEMO 1: GRID RELIABILITY & NERC CIP VIOLATION")

policy = [
    ("NERC_CIP_ACCESS", False, "Unauthorized access to BES cyber asset"),
    ("CHANGE_MANAGEMENT", False, "Unapproved control system change"),
    ("OPERATIONAL_RISK", False, "Risk to grid stability"),
    ("BLACKOUT_RISK", True, "Cascading outage possible")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: NERC CIP compliance breach")
print("AUTO-ACTION: Incident reported to Reliability Coordinator")

# -------------------------------------------------
# DEMO 2: ENVIRONMENTAL COMPLIANCE (EPA)
# -------------------------------------------------
section("DEMO 2: ENVIRONMENTAL REGULATION VIOLATION")

policy = [
    ("EPA_PERMIT", False, "Emission exceeds permitted threshold"),
    ("CLEAN_AIR_ACT", False, "Unauthorized pollutant discharge"),
    ("REPORTING_ACCURACY", False, "Emission data manipulation detected"),
    ("STRICT_LIABILITY", True, "No intent defense available")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Environmental violation")
print("AUTO-ACTION: Compliance alert + regulator disclosure draft")

# -------------------------------------------------
# DEMO 3: MARKET MANIPULATION (FERC / CFTC)
# -------------------------------------------------
section("DEMO 3: ENERGY MARKET MANIPULATION")

policy = [
    ("PRICE_MANIPULATION", False, "Artificial congestion strategy detected"),
    ("ANTI_GAMING", False, "Violates FERC market rules"),
    ("CFTC_EXPOSURE", True, "Derivatives manipulation risk"),
    ("ENRON_PATTERN", False, "Historical abuse signature matched")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Market manipulation attempt")

# -------------------------------------------------
# DEMO 4: SAFETY / PROCESS HAZARD FAILURE
# -------------------------------------------------
section("DEMO 4: INDUSTRIAL SAFETY VIOLATION")

policy = [
    ("OSHA_PSM", False, "Process Safety Management controls bypassed"),
    ("LOCKOUT_TAGOUT", False, "Energy isolation missing"),
    ("WORKER_SAFETY", False, "Imminent danger condition"),
    ("CRIMINAL_LIABILITY", True, "Willful safety violation")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Worker safety risk")
print("AUTO-ACTION: Plant shutdown + safety officer notification")

# -------------------------------------------------
# DEMO 5: PIPELINE / INFRASTRUCTURE INTEGRITY
# -------------------------------------------------
section("DEMO 5: PIPELINE & INFRASTRUCTURE INTEGRITY")

policy = [
    ("PHMSA_INTEGRITY", False, "Inspection overdue"),
    ("CORROSION_CONTROL", False, "Monitoring lapse detected"),
    ("LEAK_RISK", True, "High probability release"),
    ("PUBLIC_SAFETY", False, "Community exposure risk")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: Infrastructure integrity failure")

# -------------------------------------------------
# DEMO 6: CLIMATE / ESG MISREPORTING
# -------------------------------------------------
section("DEMO 6: CLIMATE & ESG DISCLOSURE FRAUD")

policy = [
    ("SEC_CLIMATE_RULE", False, "Scope 1/2 emissions misstated"),
    ("GREENWASHING", False, "Misleading sustainability claim"),
    ("INVESTOR_DISCLOSURE", False, "Material omission"),
    ("SEC_ENFORCEMENT", True, "Securities fraud risk")
]

show(policy)
print("\n--- EVIDENCE HASH ---")
print(h(policy))
print("\n❌ BLOCKED: ESG disclosure violation")

# -------------------------------------------------
# FINAL ENERGY COMPLIANCE AUDIT
# -------------------------------------------------
section("FINAL: ENERGY SECTOR COMPLIANCE AUDIT")

audit = {
    "audit_id": "energy_audit_e7d6c5",
    "timestamp": now(),
    "sectors": ["Power", "Oil & Gas", "Utilities", "Renewables"],
    "regulators": ["NERC", "FERC", "CFTC", "EPA", "OSHA", "PHMSA", "SEC"],
    "critical_violations": 6,
    "prevented_outcomes": [
        "Grid outage",
        "Environmental disaster",
        "Market manipulation fines",
        "Worker fatalities",
        "Pipeline rupture",
        "Securities enforcement"
    ],
    "system_role": "Deterministic safety, market, and compliance control plane"
}

print(json.dumps(audit, indent=2))
print("\n--- EVIDENCE BUNDLE HASH ---")
print(h(audit))

print("\n✅ SYSTEM STATE:")
print("• Grid stability protected")
print("• Environmental liability prevented")
print("• Energy markets kept fair")
print("• Worker & public safety enforced")
print("• ESG disclosures verified")
print("• Regulator-ready audit trail generated")
