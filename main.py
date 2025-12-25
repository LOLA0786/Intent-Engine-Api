from fastapi import FastAPI
from intent_schema import IntentEnvelope
from auth import authorize_enveloped_intent
from evidence import generate_evidence, verify_evidence
from pydantic import BaseModel

app = FastAPI(title="Intent Engine API")

# ==============================
# AUTHORIZE INTENT (ENVELOPE ONLY)
# ==============================
@app.post("/authorize-intent")
def authorize_intent_api(envelope: IntentEnvelope):
    decision = authorize_enveloped_intent(envelope.model_dump())

    return generate_evidence(
        intent=envelope.core.model_dump(),
        decision=decision,
        policy_version="fintech-v1.1"
    )

# ==============================
# VERIFY EVIDENCE
# ==============================
class VerifyPayload(BaseModel):
    intent: dict
    decision: dict
    policy_version: str
    evidence_hash: str

@app.post("/verify-evidence")
def verify_evidence_api(payload: VerifyPayload):
    valid = verify_evidence(
        payload.intent,
        payload.decision,
        payload.policy_version,
        payload.evidence_hash
    )
    return {"valid": valid}

# ==============================
# STARTUP SAFETY CHECK
# ==============================
@app.on_event("startup")
def assert_single_authorize_route():
    count = sum(
        1 for r in app.routes
        if getattr(r, "path", None) == "/authorize-intent"
    )
    assert count == 1, "Duplicate /authorize-intent routes detected"
