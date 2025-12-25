from fastapi import FastAPI
from pydantic import BaseModel
from auth import authorize_intent
from evidence import generate_evidence

app = FastAPI(title="Intent Engine API")

class RawIntent(BaseModel):
    raw_text: str

class NormalizedIntent(BaseModel):
    action: str
    amount: float | None = None
    country: str | None = None
    risk: str | None = None
    sensitive: bool = False


@app.post("/normalize-intent")
def normalize_intent_api(payload: RawIntent):
    return {
        "action": "process_payment",
        "amount": 9999.5,
        "country": "Nigeria",
        "risk": "high",
        "sensitive": True
    }


@app.post("/authorize-intent")
def authorize_intent_api(intent: NormalizedIntent):
    decision = authorize_intent(intent.dict())

    return generate_evidence(
        intent=intent.dict(),
        decision=decision,
        policy_version="fintech-v1.1"
    )

from evidence import verify_evidence

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
from intent_schema import IntentEnvelope
from auth import authorize_enveloped_intent
from evidence import generate_evidence

@app.post("/authorize-intent")
def authorize_intent_api(envelope: IntentEnvelope):
    decision = authorize_enveloped_intent(envelope.dict())

    return generate_evidence(
        intent=envelope.core.dict(),
        decision=decision,
        policy_version="fintech-v1.1"
    )
