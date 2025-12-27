from typing import Dict, Any

class PolicyEngine:
    def evaluate(self, intent: Dict[str, Any], actor: Dict[str, Any]) -> Dict[str, Any]:
        amount = intent.get("amount", 0)
        recipient = intent.get("recipient", "")
        hour = intent.get("timestamp_hour", 12)

        recipient_risk = 0.95 if "offshore" in recipient else 0.2
        amount_risk = min(amount / 500000, 1.0)
        velocity_risk = 0.4  # stub (plug txn history later)
        time_risk = 0.3 if hour < 9 or hour > 18 else 0.1

        score = round(
            max(recipient_risk, amount_risk, velocity_risk, time_risk),
            2
        )

        exposure = int(amount * score)

        return {
            "allow": score < 0.5,
            "risk": {
                "score": score,
                "exposure_usd": exposure,
                "factors": {
                    "recipient_risk": recipient_risk,
                    "amount_risk": amount_risk,
                    "velocity_risk": velocity_risk,
                    "time_risk": time_risk
                },
                "reasoning": "Offshore transfer + high amount"
            }
        }

policy_engine = PolicyEngine()
