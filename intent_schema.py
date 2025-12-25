from pydantic import BaseModel, Field, Extra
from typing import Optional, Dict, Any, Literal


# -----------------------------
# SECURITY-CRITICAL CORE
# -----------------------------
class IntentCore(BaseModel):
    action: Literal[
        "process_payment",
        "engage_legal_counsel",
        "read_prescription"
    ]
    amount: Optional[float] = Field(default=None, ge=0)
    country: Optional[str] = None
    risk: Optional[Literal["low", "medium", "high"]] = None
    sensitive: bool = False

    class Config:
        extra = Extra.forbid  # 🔒 core is strict


# -----------------------------
# FLEXIBLE EXTENSIONS (LOG ONLY)
# -----------------------------
class IntentEnvelope(BaseModel):
    core: IntentCore
    payload: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = Extra.allow  # payload can evolve freely
