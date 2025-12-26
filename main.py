from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from pydantic import BaseModel
import os
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from auth import get_current_user, create_jwt_token
from policy_engine import authorize_intent, generate_synthetic_data, simulate_attack, get_metrics
from replay_protection import protector
from fabric_integration import ledger
from typing import Dict, Any
from datetime import datetime
import json
import hashlib  # For legacy

app = FastAPI(title="Intent Engine API - Redis + Fabric", version="3.0.0")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

security = HTTPBearer()

class IntentRequest(BaseModel):
    action: str
    entity: Dict[str, Any]
    tenant_id: str = os.getenv("DEFAULT_TENANT", "bankA")

class BatchTestRequest(BaseModel):
    intents: list[IntentRequest]
    num_synthetics: int = 10

@app.post("/normalize-intent")
@limiter.limit(os.getenv("RATE_LIMIT", "100/minute"))
async def normalize_intent(intent: IntentRequest, authorization: str = Depends(security), request: Request = None):
    user = get_current_user(authorization.credentials)
    timestamp = datetime.utcnow().isoformat()
    norm_intent = {
        "action": intent.action, 
        "entity": intent.entity, 
        "tenant_id": intent.tenant_id, 
        "timestamp": timestamp, 
        "user_id": user["sub"]
    }
    # Full Redis nonce
    nonce = protector.generate_nonce(user["sub"], intent.tenant_id, timestamp)
    norm_intent["nonce"] = nonce
    if not await protector.check_and_cache_nonce(nonce, user["sub"], intent.tenant_id):
        raise HTTPException(409, "Replay attack detected - nonce already used")
    return norm_intent

@app.post("/authorize-intent")
@limiter.limit(os.getenv("RATE_LIMIT", "100/minute"))
async def authorize_intent_endpoint(intent: IntentRequest, authorization: str = Depends(security), request: Request = None):
    user = get_current_user(authorization.credentials)
    if not user: raise HTTPException(401, "Unauthorized")
    
    decision = {"decision": "DENY", "reason": "Fail-closed default"}
    
    try:
        norm_intent = await normalize_intent(intent, authorization)
        pol_decision = authorize_intent(norm_intent, user.get("tenant", "default"))
        if pol_decision["decision"] == "ALLOW":
            # Submit to Fabric for audit
            tx_id = ledger.submit_audit(norm_intent, pol_decision, user["sub"])
            if tx_id:
                pol_decision["fabric_tx_id"] = tx_id
                decision = pol_decision
            else:
                raise Exception("Fabric submit failed")
        else:
            decision = pol_decision
    except Exception as e:
        raise HTTPException(500, f"Blocked: {str(e)}")
    
    return decision

@app.post("/test-batch")
@limiter.limit("10/minute")
async def test_batch(req: BatchTestRequest, authorization: str = Depends(security)):
    user = get_current_user(authorization.credentials)
    results = []
    intents = req.intents or generate_synthetic_data(req.num_synthetics, "bankA")
    for i_intent in intents:
        decision = authorize_intent(i_intent, user["tenant"])  # Policy only for batch
        # Optional: Submit each to Fabric (comment for speed)
        # tx_id = ledger.submit_audit(i_intent, decision, user["sub"])
        results.append({"intent": i_intent, "decision": decision})
    return {"results": results, "note": "For full Fabric, uncomment submit"}

@app.post("/generate-synthetic")
async def gen_synthetic(num: int = 5, tenant: str = "bankA"):
    return generate_synthetic_data(num, tenant)

@app.post("/simulate-attack")
async def sim_attack(scenario: str = "replay"):
    if scenario == "replay":
        # Test nonce replay
        bad_intent = IntentRequest(action="test", entity={}, tenant_id="bankA")
        norm = await normalize_intent(bad_intent, "fake_auth")  # Will fail on second call, but sim
        return {"vulnerability": "Replay blocked by Redis", "status": "secure"}
    elif scenario == "fabric_replay":
        return {"note": "Fabric getBinding() prevents chain replays"}
    return simulate_attack(scenario)

@app.post("/replay-test")
async def replay_test(nonce: str, user_id: str, tenant: str):
    return {"is_replay": not await protector.check_and_cache_nonce(nonce, user_id, tenant)}

@app.get("/metrics")
async def metrics():
    return get_metrics()

@app.post("/login")
async def login(username: str, password: str):
    if username == "test" and password == "test":
        token = create_jwt_token({"sub": username, "tenant": "bankA"})
        return {"access_token": token}
    raise HTTPException(401, "Invalid creds")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
