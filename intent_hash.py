import json
import hashlib
from typing import Dict, Any

def canonical_intent(intent: Dict[str, Any]) -> Dict[str, Any]:
    """
    Canonicalize intent so approvals bind to economic reality,
    not string formatting.
    """
    return {
        "action": intent.get("action"),
        "amount": int(intent.get("amount")),
        "currency": intent.get("currency"),
        "recipient": intent.get("recipient"),
    }

def intent_hash(intent: Dict[str, Any]) -> str:
    canonical = canonical_intent(intent)
    payload = json.dumps(canonical, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()
