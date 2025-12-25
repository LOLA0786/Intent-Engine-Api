import re
import random
import hashlib
import json

# -------------------------------------------------
# INTENT NORMALIZATION (Unstructured → Canonical JSON)
# -------------------------------------------------
def normalize_intent(unstructured_text):
    text = unstructured_text.lower()

    intent = {
        "action": "prescribe_medication",
        "drug": "unknown",
        "patient_age": 0,
        "allergies": [],
        "frequency": "daily",
        "controlled": False
    }

    # Drug extraction
    if "penicillin" in text:
        intent["drug"] = "penicillin"
    elif "oxy" in text or "oxycodone" in text:
        intent["drug"] = "oxycodone"
        intent["controlled"] = True

    # Age extraction (e.g. 5yo, 35 year)
    age_match = re.search(r"(\d+)\s*(yo|year)", text)
    if age_match:
        intent["patient_age"] = int(age_match.group(1))

    # Frequency extraction
    if "4x" in text:
        intent["frequency"] = "4x_daily"
    elif "2x" in text:
        intent["frequency"] = "2x_daily"

    return intent

# -------------------------------------------------
# POLICY ENGINE (Deterministic + Graduated)
# -------------------------------------------------
def evaluate_policy(intent):
    decisions = []
    score = 0.0
    weights = {"critical": 0.6, "medium": 0.3}

    # AGE CHECK
    age_ok = intent["patient_age"] >= 18
    decisions.append([
        "AGE_CHECK",
        age_ok,
        "Patient age valid" if age_ok else "Under 18 – requires guardian"
    ])
    if not age_ok:
        score += weights["medium"]

    # ALLERGY CHECK (stub: no allergies)
    allergy_ok = intent["drug"] not in intent["allergies"]
    decisions.append([
        "ALLERGY_CHECK",
        allergy_ok,
        "No known allergies" if allergy_ok else "CRITICAL: Allergy conflict"
    ])
    if not allergy_ok:
        score += weights["critical"]

    # CONTROLLED SUBSTANCE LOGIC
    if intent["controlled"]:
        freq_exceeded = intent["frequency"].startswith("4x")
        decisions.append([
            "FREQUENCY_LIMIT",
            not freq_exceeded,
            "Frequency within limit" if not freq_exceeded else "Max 3x daily exceeded"
        ])
        if freq_exceeded:
            score += weights["medium"]

        # PDMP (simulated 20% chance)
        pdmp_active = random.random() < 0.2
        decisions.append([
            "PDMP_CHECK",
            not pdmp_active,
            "PDMP clear" if not pdmp_active else "Active prescription exists"
        ])
        if pdmp_active:
            score += weights["critical"]

        review_needed = freq_exceeded or pdmp_active
        decisions.append([
            "MANDATORY_REVIEW",
            not review_needed,
            "Review complete" if not review_needed else "30-day review missing"
        ])
        if review_needed:
            score += weights["medium"]

    # OUTCOME
    if score == 0:
        outcome = "✅ APPROVED - Prescription allowed"
    elif score <= 0.4:
        outcome = "⚠️ APPROVE WITH CONDITIONS - Escalated review"
    else:
        outcome = "❌ BLOCKED - Regulatory or safety violation"

    evidence_hash = hashlib.sha256(
        json.dumps(decisions, sort_keys=True).encode()
    ).hexdigest()

    return outcome, decisions, evidence_hash

# -------------------------------------------------
# DEMO RUN
# -------------------------------------------------
if __name__ == "__main__":
    unstructured = "Give penicillin to 5yo kid with rash"

    intent = normalize_intent(unstructured)
    outcome, decisions, h = evaluate_policy(intent)

    print("\n=== UNSTRUCTURED INTENT DEMO ===")
    print(f"Input: {unstructured}")

    print("\n--- NORMALIZED INTENT ---")
    print(json.dumps(intent, indent=2))

    print("\n--- POLICY DECISION ---")
    for d in decisions:
        print(d)

    print("\n--- EVIDENCE HASH ---")
    print(h)

    print("\n--- OUTCOME ---")
    print(outcome)
