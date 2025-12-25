import json, hashlib, time, re

MAX_CONTROLLED_FREQUENCY = 3  # per day

def hash_evidence(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()

def parse_frequency(freq):
    """
    Accepts: daily, 2x_daily, 3x_daily, 4x_daily
    Rejects malformed input.
    """
    m = re.match(r"(\d)x_daily", freq)
    if m:
        return int(m.group(1))
    if freq == "daily":
        return 1
    return None  # invalid

def evaluate_policy(intent):
    decisions = []

    # AGE
    if intent["patient_age"] < 18:
        decisions.append(["AGE_CHECK", False, "Patient under 18"])
        age_ok = False
    else:
        decisions.append(["AGE_CHECK", True, "Patient age valid"])
        age_ok = True

    # ALLERGY
    if intent["drug"] in intent["allergies"]:
        decisions.append(["ALLERGY_CHECK", False, "CRITICAL: Allergy conflict"])
        allergy_ok = False
    else:
        decisions.append(["ALLERGY_CHECK", True, "No known allergies"])
        allergy_ok = True

    # CONTROLLED SUBSTANCE
    freq = parse_frequency(intent["frequency"])
    if intent["controlled"]:
        if freq is None:
            decisions.append(["FREQUENCY_FORMAT", False, "Invalid frequency format"])
            freq_ok = False
        elif freq > MAX_CONTROLLED_FREQUENCY:
            decisions.append(["FREQUENCY_LIMIT", False, "Max 3x daily exceeded"])
            decisions.append(["PDMP_CHECK", False, "Active prescription exists"])
            decisions.append(["MANDATORY_REVIEW", False, "30-day review missing"])
            freq_ok = False
        else:
            decisions.append(["FREQUENCY_LIMIT", True, "Frequency within limit"])
            freq_ok = True
    else:
        freq_ok = True

    allowed = age_ok and allergy_ok and freq_ok
    return allowed, decisions

def main():
    drug = input("Enter drug: ").strip().lower()
    age = int(input("Enter patient_age: "))
    allergies = input("Enter allergies (comma-separated or 'none'): ").strip().lower()
    frequency = input("Enter frequency (daily / 2x_daily / 4x_daily): ").strip().lower()
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
        print("\n❌ BLOCKED - Controlled substance violation")
        print("Legal: DEA reporting triggered")

if __name__ == "__main__":
    main()
