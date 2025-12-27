from approval_store import issue_approval, validate_and_consume_approval
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
import time

from policy_engine import authorize

app = FastAPI(title="UAAL Intent Control Plane")

# --------------------
# In-memory approval store (PILOT ONLY)
# --------------------
_APPROVALS = {}

# --------------------
# Models
# --------------------

class IntentRequest(BaseModel):
    intent: dict
    actor: dict
    approval_id: Optional[str] = None


class ApprovalRequest(BaseModel):
    approved_by: str
    role: str
    amount: int
    currency: str
    recipient: str
    valid_for_seconds: int = 300


# --------------------
# Routes
# --------------------

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/approve")
def approve(req: ApprovalRequest):
    approval_id = f"HAP-{uuid.uuid4().hex[:8]}"
    _APPROVALS[approval_id] = {
        "approved_by": req.approved_by,
        "role": req.role,
        "amount": req.amount,
        "currency": req.currency,
        "recipient": req.recipient,
        "expires_at": time.time() + req.valid_for_seconds,
        "used": False,
    }
    return {
        "approval_id": approval_id,
        "approved_by": req.approved_by,
        "expires_in_seconds": req.valid_for_seconds,
        "single_use": True
    }



@app.post("/authorize-intent")
def authorize_intent(payload: dict):
    intent = payload.get("intent")
    actor = payload.get("actor")
    approval_id = payload.get("approval_id")

    print("=== AUTHORIZE INTENT HIT ===")
    print("approval_id:", approval_id)
    print("intent:", intent)

    if not intent or not actor:
        raise HTTPException(status_code=422, detail="Missing intent or actor")

    # Enforce human approval if provided
    if approval_id:
        print("=== CHECKING APPROVAL ===")
        ok, reason = validate_and_consume_approval(approval_id, intent)
        print("APPROVAL RESULT:", ok, reason)
        if not ok:
            raise HTTPException(status_code=400, detail=reason)

    # Policy evaluation
    decision = policy_engine.evaluate(intent, actor)

    if not decision.get("allow"):
        return {
            "allowed": False,
            "reason": "Human approval required",
            "execution": "NOT_PERFORMED",
        }

    return {
        "allowed": True,
        "reason": "Human approval verified",
        "execution": "PERFORMED",
    }

@app.post("/approve-intent")
def approve_intent(payload: dict):
    approval_id = issue_approval(
        scope=payload["scope"],
        approved_by=payload["approved_by"],
        valid_for_seconds=payload.get("valid_for_seconds", 300),
    )
    return {
        "approval_id": approval_id,
        "status": "ACTIVE"
    }

@app.post("/approve-intent")
def approve_intent(payload: dict):
    approval_id = issue_approval(
        scope=payload["scope"],
        approved_by=payload["approved_by"],
        valid_for_seconds=payload.get("valid_for_seconds", 300),
    )
    return {
        "approval_id": approval_id,
        "status": "ACTIVE"
    }
# --- Approval Store ---
