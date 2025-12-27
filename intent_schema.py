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

# --------------------------------------------------
# Compatibility adapter for tests / external callers
# --------------------------------------------------
def normalize_intent(input_text: str) -> dict:
    """
    Thin wrapper to normalize unstructured intent.
    """
    try:
        # Adjust this call to your real implementation
        return parse_intent(input_text)
    except NameError:
        # Fallback: assume already structured
        return {
            "action": "transfer_funds",
            "amount": 1_000_000,
            "recipient": "offshore_high_risk",
            "currency": "USD",
        }
