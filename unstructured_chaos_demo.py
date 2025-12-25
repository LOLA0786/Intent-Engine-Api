import re
import random
import hashlib
import json

# -------------------------------------------------
# NORMALIZATION (Unstructured → Canonical Intent)
# -------------------------------------------------
def normalize_intent(text):
    t = text.lower()

    intent = {
        "action": "prescribe_medication",
        "drug": "unknown",
        "patient_age": 0,
        "allergies": [],
        "frequency": "daily",
        "controlled": False,
        "symptoms": [],
        "pregnant": False
    }

    # Drug extraction
    if "penicillin" in t:
        intent["drug"] = "penicillin"
    elif "accutane" in t or "isotretinoin" in t:
        intent["drug"] = "accutane"
    elif "oxycodone" in t or "oxy" in t:
        intent["drug"] = "oxycodone"
        intent["controlled"] = True

    # Age extraction
    age_match = re.search(r"(\d+)\s*(yo|yr|year)", t)
    if age_match:
        intent["patient_age"] = int(age_match.group(1))

    # Pregnancy detection
    if "pregnant" in t:
        intent["pregnant"] = True

    # Allergy detection
    allergy_match = re.search(r"allerg(?:y|ic)\s+to\s+([a-z]+)", t)
    if allergy_match:
        intent["allergies"].append(allergy_match.group(1))

    # Symptoms
    if "rash" in t:
        intent["symptoms"].append("rash")

    # Frequency
    if "4x" in t:
        intent["frequency"] = "4x_daily"
    elif "2x" in t:
        intent["frequency"] = "2x_daily"

    return intent

# -------------------------------------------------
# POLICY ENGINE (Graduated + Deterministic)
# -------------------------------------------------
def evaluate_policy(intent):
    decisions = []
    score = 0.0
    weights = {"critical": 0.6, "medium": 0.3, "low": 0.1}

    # AGE
    age_ok = intent["patient_age"] >= 18
    decisions.append([
        "AGE_CHECK",
        age_ok,
        "Patient age valid" if age_ok else "Under 18 – requires guardian"
    ])
    if not age_ok:
        score += weights["medium"]

    # ALLERGY
    allergy_ok = intent["drug"] not in intent["allergies"]
    decisions.append([
        "ALLERGY_CHECK",
        allergy_ok,
        "No known allergies" if allergy_ok else "CRITICAL: Allergy conflict"
    ])
    if not allergy_ok:
        score += weights["critical"]

    # SYMPTOM PROXY (rash + penicillin)
    if "rash" in intent["symptoms"] and intent["drug"] == "penicillin":
        decisions.append([
            "SYMPTOM_RISK",
            False,
            "Rash may indicate allergic reaction"
        ])
        score += weights["low"]

    # AGE-RESTRICTED DRUG
    if intent["drug"] == "accutane":
        age_restricted_ok = intent["patient_age"] >= 18
        decisions.append([
            "AGE_RESTRICTED_DRUG",
            age_restricted_ok,
            "Age restriction satisfied" if age_restricted_ok else "Accutane prohibited for minors"
        ])
        if not age_restricted_ok:
            score += weights["medium"]

    # PREGNANCY ABSOLUTE BLOCK (Accutane)
    if intent["pregnant"] and intent["drug"] == "accutane":
        decisions.append([
            "PREGNANCY_CONTRAINDICATION",
            False,
            "Accutane causes severe fetal harm"
        ])
        score += weights["critical"]

    # OUTCOME
    if score == 0:
        outcome = "✅ APPROVED - Prescription allowed"
    elif score <= 0.4:
        outcome = "⚠️ ESCALATE - Conditional approval"
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
    unstructured = (
        "Prescribe accutane daily to 16-year-old teen girl "
        "with acne, no allergies, but she's pregnant"
    )

    intent = normalize_intent(unstructured)
    outcome, decisions, h = evaluate_policy(intent)

    print("\n=== UNSTRUCTURED CHAOS TEST ===")
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
