from typing import Dict, Any

HIGH_RISK_RECIPIENTS = {"offshore_high_risk"}

def calculate_risk(intent: Dict[str, Any], history: Dict[str, Any] | None = None) -> Dict[str, Any]:
    amount = intent["amount"]

    recipient_risk = 0.95 if intent["recipient"] in HIGH_RISK_RECIPIENTS else 0.2
    amount_risk = min(amount / 750_000, 1.0)  # normalized
    velocity_risk = history.get("velocity_risk", 0.4) if history else 0.4
    time_risk = history.get("time_risk", 0.3) if history else 0.3

    score = max(recipient_risk, amount_risk, velocity_risk, time_risk)
    exposure = int(score * amount)

    return {
        "score": round(score, 2),
        "exposure_usd": exposure,
        "factors": {
            "recipient_risk": round(recipient_risk, 2),
            "amount_risk": round(amount_risk, 2),
            "velocity_risk": round(velocity_risk, 2),
            "time_risk": round(time_risk, 2),
        },
        "model": "max-factor",
        "reasoning": "Highest contributing risk factor determines outcome"
    }
