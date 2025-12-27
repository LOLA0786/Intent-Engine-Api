from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from approval_store import (
    issue_approval,
    validate_and_collect_approvals,
    consume_approvals,
)

app = FastAPI(title="UAAL Intent Control Plane")

DUAL_AUTH_THRESHOLD = 250_000


class Intent(BaseModel):
    action: str
    amount: int
    currency: str
    recipient: str


class Actor(BaseModel):
    id: str
    type: str


class ApproveIntentRequest(BaseModel):
    approver: str
    scope: Intent
    valid_for_seconds: int


class AuthorizeIntentRequest(BaseModel):
    intent: Intent
    actor: Actor
    approval_ids: Optional[List[str]] = []


@app.post("/approve-intent")
def approve_intent(req: ApproveIntentRequest):
    approval_id = issue_approval(
        approver=req.approver,
        scope=req.scope.dict(),
        valid_for_seconds=req.valid_for_seconds,
    )
    return {"approval_id": approval_id, "status": "ACTIVE"}


@app.post("/authorize-intent")
def authorize_intent(req: AuthorizeIntentRequest):
    intent = req.intent.dict()

    if intent["amount"] > DUAL_AUTH_THRESHOLD:
        if not validate_and_collect_approvals(req.approval_ids, intent):
            return {
                "allowed": False,
                "reason": "Dual approval required",
                "execution": "NOT_PERFORMED",
            }

        consume_approvals(req.approval_ids)

    return {"allowed": True, "execution": "PERFORMED"}
