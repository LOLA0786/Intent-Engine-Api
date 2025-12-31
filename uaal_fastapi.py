from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import os

from policy_engine import authorize_intent
from evidence import generate_evidence, verify_evidence
from replay_protection import check_replay

app = FastAPI(title="Intent Engine API", version="1.0.0")

# --- Auth ---
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != os.getenv("API_SECRET_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

# --- Models ---
class IntentRequest(BaseModel):
    intent: dict
    agent_id: str
    nonce: str

class VerifyRequest(BaseModel):
    decision_id: str
    evidence_hash: str

# --- Endpoints ---
@app.post("/authorize-intent")
async def authorize(request: IntentRequest, key: str = Depends(get_api_key)):
    if not check_replay(request.nonce):
        raise HTTPException(
            status_code=429,
            detail={
                "code": "REPLAY_DETECTED",
                "reason": "Replay detected"
            }
        )

    try:
        decision = authorize_intent(request.intent)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "ENGINE_ERROR",
                "reason": "Authorization engine failure"
            }
        )

    if not decision.get("allowed", False):
        raise HTTPException(
            status_code=403,
            detail={
                "code": "POLICY_DENY",
                "reason": decision.get("reason", "Policy denied")
            }
        )

    evidence = generate_evidence(request.intent, decision)

    return {
        "decision_id": evidence["decision_id"],
        "decision": decision,
        "evidence": {
            "hash": evidence["hash"],
            "algorithm": evidence["algorithm"]
        }
    }

@app.post("/verify-evidence")
async def verify(req: VerifyRequest, key: str = Depends(get_api_key)):
    valid = verify_evidence(req.decision_id, req.evidence_hash)
    if not valid:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_EVIDENCE",
                "reason": "Evidence hash does not match decision"
            }
        )

    return {
        "decision_id": req.decision_id,
        "verified": True
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
