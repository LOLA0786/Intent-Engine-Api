import os
import uuid
import requests

INTENT_ENGINE_URL = os.getenv("INTENT_ENGINE_URL", "http://localhost:8000")
API_KEY = os.getenv("API_SECRET_KEY")

class IntentDenied(Exception):
    """Raised when the intent is explicitly denied by policy."""
    pass

class IntentEngineUnavailable(Exception):
    """Raised when the intent engine cannot be reached."""
    pass

def authorize_intent(intent: dict, agent_id: str = "langchain-agent"):
    if not API_KEY:
        raise RuntimeError(
            "API_SECRET_KEY is not set. "
            "Export API_SECRET_KEY before running the client."
        )

    payload = {
        "intent": intent,
        "agent_id": agent_id,
        "nonce": str(uuid.uuid4())
    }

    try:
        resp = requests.post(
            f"{INTENT_ENGINE_URL}/authorize-intent",
            json=payload,
            headers={"X-API-Key": API_KEY},
            timeout=1.0
        )
    except requests.exceptions.ConnectionError:
        raise IntentEngineUnavailable(
            "Intent Engine is unreachable — failing closed"
        )

    if resp.status_code == 403:
        detail = resp.json().get("detail", {})
        raise IntentDenied(detail)

    resp.raise_for_status()
    return resp.json()
