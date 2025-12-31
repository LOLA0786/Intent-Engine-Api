from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class DecisionPayload(BaseModel):
    decision: Literal["ALLOW", "BLOCK", "REQUIRE_HUMAN"]
    evidence_id: str = Field(..., min_length=1)
    violations: Optional[List[str]] = None
    shadowed: Optional["DecisionPayload"] = None

class SignedDecision(BaseModel):
    payload: DecisionPayload
    signature: str
    key_provider: str
    key_version: Optional[str]
