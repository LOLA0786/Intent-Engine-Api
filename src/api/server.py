from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import uuid

api = FastAPI()

# -----------------------
# In-memory intent store
# -----------------------
INTENTS = []

# -----------------------
# Models
# -----------------------
class InjectIntentRequest(BaseModel):
    topic: str
    confidence: float | None = None
    momentum: str | None = None
    authenticity: dict | None = None
    streak_days: int | None = None


class VerifyIntentRequest(BaseModel):
    topic: str


# -----------------------
# Health
# -----------------------
@api.get("/health")
def health():
    return {"status": "ok"}


# -----------------------
# Inject Intent
# -----------------------
@api.post("/inject-intent")
def inject_intent(req: InjectIntentRequest):
    intent = {
        "id": str(uuid.uuid4()),
        "topic": req.topic,
        "confidence": req.confidence or 0.0,
        "created_at": datetime.utcnow().isoformat()
    }
    INTENTS.append(intent)
    return {"id": intent["id"]}


# -----------------------
# VERIFY INTENT (PRODUCT)
# -----------------------
@api.post("/verify-intent")
def verify_intent(req: VerifyIntentRequest):
    if not INTENTS:
        return {
            "allowed": False,
            "reason": "No active intent signals"
        }

    last = INTENTS[-1]

    if last["topic"].lower() == req.topic.lower():
        return {
            "allowed": True,
            "intent_score": last.get("confidence", 0),
            "reason": "Live human intent detected"
        }

    return {
        "allowed": False,
        "reason": "Intent not strong enough"
    }
