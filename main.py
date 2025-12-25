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
