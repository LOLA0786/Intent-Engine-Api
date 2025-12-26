import random

def generate_synthetic_data(n=10, spike_prob=0.2):
    synthetics = []

    for i in range(n):
        # base signals
        amount = random.choice([50_000, 100_000, 150_000, 250_000, 500_000])
        velocity = round(i / max(n - 1, 1), 2)
        history_score = round(1 - velocity, 2)

        # 🔥 inject suspicious spikes
        if random.random() < spike_prob:
            velocity = round(random.uniform(0.8, 1.0), 2)
            history_score = round(random.uniform(0.0, 0.3), 2)
            amount = random.choice([750_000, 1_200_000])

        synthetics.append({
            "action": random.choice(["approve_loan", "process_txn", "flag_fraud"]),
            "entity": {
                "amount": amount,
                "velocity": velocity,
                "history_score": history_score
            },
            "tenant_id": "bankA"
        })

    return synthetics


def infer_risk(entity):
    if entity["velocity"] > 0.75 or entity["history_score"] < 0.3:
        return "high"
    if entity["velocity"] > 0.4:
        return "medium"
    return "low"


def authorize_intent(intent):
    risk = infer_risk(intent["entity"])
    amt = intent["entity"]["amount"]
    action = intent["action"]

    if risk == "high":
        return {"decision": "DENY", "reason": "High inferred risk"}

    if action == "approve_loan" and amt > 500_000:
        return {"decision": "DENY", "reason": "Amount exceeds limit"}

    if action not in {"approve_loan", "process_txn", "flag_fraud"}:
        return {"decision": "DENY", "reason": "Unknown action"}

    return {"decision": "ALLOW", "reason": "Compliant"}
from collections import deque
import statistics

WINDOW = 20
velocity_window = deque(maxlen=WINDOW)
amount_window = deque(maxlen=WINDOW)

def detect_anomaly(entity):
    velocity = entity["velocity"]
    amount = entity["amount"]

    velocity_window.append(velocity)
    amount_window.append(amount)

    if len(velocity_window) < 5:
        return False, None

    v_mean = statistics.mean(velocity_window)
    v_std = statistics.stdev(velocity_window) or 0.01

    a_mean = statistics.mean(amount_window)
    a_std = statistics.stdev(amount_window) or 1

    v_z = abs((velocity - v_mean) / v_std)
    a_z = abs((amount - a_mean) / a_std)

    if v_z > 3 or a_z > 3:
        return True, f"ANOMALY_SPIKE (v_z={v_z:.2f}, a_z={a_z:.2f})"

    return False, None

def authorize_intent(intent):
    entity = intent["entity"]
    action = intent["action"]

    is_anom, reason = detect_anomaly(entity)
    if is_anom:
        return {"decision": "DENY", "reason": reason}

    risk = infer_risk(entity)
    amt = entity["amount"]

    if risk == "high":
        return {"decision": "DENY", "reason": "High inferred risk"}

    if action == "approve_loan" and amt > 500_000:
        return {"decision": "DENY", "reason": "Amount exceeds limit"}

    if action not in {"approve_loan", "process_txn", "flag_fraud"}:
        return {"decision": "DENY", "reason": "Unknown action"}

    return {"decision": "ALLOW", "reason": "Compliant"}
