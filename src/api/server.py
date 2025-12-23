from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
import uuid
import json

api = FastAPI()

# -----------------------
# Load API keys
# -----------------------
with open("api_keys.json") as f:
    API_KEYS = json.load(f)

def require_api_key(x_api_key: str = Header(...)):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if API_KEYS[x_api_key]["used"] >= API_KEYS[x_api_key]["credits"]:
        raise HTTPException(status_code=402, detail="Quota exceeded")

    API_KEYS[x_api_key]["used"] += 1
    return x_api_key

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

class VerifyIntentRequest(BaseModel):
    topic: str

# -----------------------
# Health
# -----------------------
@api.get("/health")
def health():
    return {"status": "ok"}

# -----------------------
# Inject Intent (FREE)
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
# Verify Intent (PAID)
# -----------------------
@api.post("/verify-intent")
def verify_intent(
    req: VerifyIntentRequest,
    api_key: str = Depends(require_api_key)
):
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
