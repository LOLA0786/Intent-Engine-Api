from fastapi import FastAPI, Header
from pydantic import BaseModel
import hashlib
import json

app = FastAPI()

class IntentRequest(BaseModel):
    prompt: str
    toolCall: str
    params: dict
    domain: str

def h(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()[:16]

@app.post("/v1/intent/analyze")
def analyze_intent(req: IntentRequest, authorization: str = Header(None)):
    core_intent = {
        "toolCall": req.toolCall,
        "domain": req.domain
    }

    payload = {
        "toolCall": req.toolCall,
        "params": req.params
    }

    risk = "LOW"
    if req.domain == "banking" and req.toolCall == "approve_loan":
        if req.params.get("amount", 0) > 200000:
            risk = "CRITICAL"

    return {
        "riskLevel": risk,
        "shadowMode": True,
        "policyDecision": "DENY" if risk == "CRITICAL" else "ALLOW",
        "intentDrift": risk == "CRITICAL",
        "evidence": {
            "coreIntentHash": h(core_intent),
            "payloadHash": h(payload)
        }
    }
