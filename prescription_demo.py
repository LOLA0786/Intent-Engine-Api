import json, hashlib, time

RESTRICTED_AGE = 18
AGE_RESTRICTED_DRUGS = ["accutane"]

def hash_evidence(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()

def evaluate_policy(intent):
    decisions = []

    # Age check
    if intent["patient_age"] >= RESTRICTED_AGE:
        decisions.append(["AGE_CHECK", True, "Patient age valid"])
        age_ok = True
    else:
        decisions.append(["AGE_CHECK", False, "Patient under 18"])
        age_ok = False

    # Allergy check
    if intent["drug"] in intent["allergies"]:
        decisions.append(["ALLERGY_CHECK", False, "CRITICAL: Patient allergic to medication"])
        allergy_ok = False
    else:
        decisions.append(["ALLERGY_CHECK", True, "No known allergies"])
        allergy_ok = True

    # Drug-specific age restriction
    if intent["drug"] in AGE_RESTRICTED_DRUGS and intent["patient_age"] < RESTRICTED_AGE:
        decisions.append(["AGE_RESTRICTED_DRUG", False, "Age-restricted medication"])
        drug_age_ok = False
    else:
        decisions.append(["AGE_RESTRICTED_DRUG", True, "Drug age restriction satisfied"])
        drug_age_ok = True

    allowed = age_ok and allergy_ok and drug_age_ok
    return allowed, decisions

def main():
    drug = input("Enter drug: ").strip().lower()
    age = int(input("Enter patient_age: "))
    allergies = input("Enter allergies (comma-separated or 'none'): ").strip().lower()
    frequency = input("Enter frequency: ").strip().lower()
    controlled = input("Controlled substance? (true/false): ").strip().lower() == "true"

    allergy_list = [] if allergies == "none" else [a.strip() for a in allergies.split(",")]

    intent = {
        "action": "prescribe_medication",
        "drug": drug,
        "patient_age": age,
        "allergies": allergy_list,
        "frequency": frequency,
        "controlled": controlled
    }

    print("\n--- INTENT ---")
    print(json.dumps(intent, indent=2))

    allowed, decisions = evaluate_policy(intent)

    print("\n--- POLICY DECISION ---")
    for d in decisions:
        print(d)

    evidence = {
        "intent": intent,
        "decisions": decisions,
        "timestamp": time.time()
    }

    print("\n--- EVIDENCE HASH ---")
    print(hash_evidence(evidence))

    if allowed:
        print("\n✅ APPROVED - Prescription allowed")
    else:
        print("\n❌ BLOCKED - Regulatory or safety violation")

if __name__ == "__main__":
    main()
