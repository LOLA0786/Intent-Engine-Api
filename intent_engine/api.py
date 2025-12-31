from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from intent_engine.core.authorizer import authorize
from intent_engine.core.audit import get_decision, init_db

init_db()

app = FastAPI(
    title="UAAL Intent Engine",
    version="0.2.0"
)

class IntentRequest(BaseModel):
    layer: str
    payload: dict
    timestamp: str | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/authorize")
def authorize_intent(intent: IntentRequest):
    return authorize(intent.dict())

@app.get("/audit/{evidence_id}")
def audit_replay(evidence_id: str):
    record = get_decision(evidence_id)
    if not record:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return record

@app.get("/audit/query")
def audit_query(agent_id: str | None = None,
                policy: str | None = None,
                since: str | None = None,
                until: str | None = None):
    from intent_engine.core.audit import query_audit
    return query_audit(agent_id, since, until, policy)

@app.post("/simulate")
def simulate_intent(intent: IntentRequest):
    from intent_engine.core.authorizer import authorize
    from intent_engine.config.uaal_config import UAAL_SHADOW_MODE

    # force shadow regardless of env
    decision = authorize(intent.dict())
    return {
        "simulation": True,
        "decision": decision
    }

@app.get("/audit/view/{evidence_id}")
def auditor_view(evidence_id: str):
    from intent_engine.core.audit import get_decision
    from intent_engine.core.merkle import current_root

    record = get_decision(evidence_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")

    record["merkle_root"] = current_root()
    return record

@app.post("/audit/anchor")
def anchor_daily_root():
    from intent_engine.core.root_publisher import publish_daily_root
    return publish_daily_root()

from fastapi import Header
from intent_engine.core.auth import verify_auditor_token

def auditor_guard(auditor_id: str, token: str):
    if not verify_auditor_token(auditor_id, token):
        raise HTTPException(status_code=403, detail="Invalid auditor token")

@app.get("/audit/view/{evidence_id}")
def auditor_view(
    evidence_id: str,
    x_auditor_id: str = Header(...),
    x_auditor_token: str = Header(...)
):
    auditor_guard(x_auditor_id, x_auditor_token)
    from intent_engine.core.audit import get_decision
    from intent_engine.core.merkle import current_root

    record = get_decision(evidence_id)
    if not record:
        raise HTTPException(status_code=404, detail="Not found")

    record["merkle_root"] = current_root()
    return record
