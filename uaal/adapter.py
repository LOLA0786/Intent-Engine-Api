import requests

UAAL_URL = "http://127.0.0.1:8001"

def authorize_intent(intent_payload):
    """
    intent_payload = {
        "topic": str,
        "confidence": float,
        "sensitive": bool
    }
    """
    try:
        r = requests.post(
            f"{UAAL_URL}/authorize/intent",
            json=intent_payload,
            timeout=2
        )
        return r.json()
    except Exception as e:
        return {
            "allowed": False,
            "reason": f"UAAL intent auth failed: {e}"
        }


def authorize_execution(intent_decision, plan):
    payload = {
        "intent": intent_decision,
        "plan": plan
    }

    try:
        r = requests.post(
            f"{UAAL_URL}/authorize/execution",
            json=payload,
            timeout=2
        )
        return r.json()
    except Exception as e:
        return {
            "allowed": False,
            "reason": f"UAAL exec auth failed: {e}"
        }
