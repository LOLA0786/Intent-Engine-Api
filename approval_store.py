import time
import uuid
from typing import Dict, List

# In-memory store (swap later with Redis / DB)
_APPROVALS: Dict[str, dict] = {}

REQUIRED_APPROVALS = 2
DUAL_AUTH_THRESHOLD = 250_000


def issue_approval(*, approver: str, scope: dict, valid_for_seconds: int) -> str:
    if not approver or not scope:
        raise ValueError("approver and scope required")

    approval_id = f"HAP-{uuid.uuid4().hex[:8]}"

    _APPROVALS[approval_id] = {
        "approver": approver,
        "scope": scope,
        "expires_at": time.time() + valid_for_seconds,
        "consumed": False,
        "created_at": time.time(),
    }

    return approval_id


def validate_and_collect_approvals(approval_ids: List[str], intent: dict) -> bool:
    now = time.time()
    valid = []

    for aid in approval_ids:
        rec = _APPROVALS.get(aid)
        if not rec:
            continue
        if rec["consumed"]:
            continue
        if rec["expires_at"] < now:
            continue
        if rec["scope"] != intent:
            continue
        valid.append(aid)

    return len(valid) >= REQUIRED_APPROVALS


def consume_approvals(approval_ids: List[str]) -> None:
    for aid in approval_ids:
        if aid in _APPROVALS:
            _APPROVALS[aid]["consumed"] = True
