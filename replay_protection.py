"""
Replay protection primitives.
Fail-closed by default.
"""

import time

# Simple in-memory blacklist for local / pilot
_BLACKLIST = set()
_REPLAY_LOG = []

def record_replay_attempt(nonce: str, actor_id: str = None):
    """
    Record a replay attempt for audit / alerting.
    """
    _REPLAY_LOG.append({
        "nonce": nonce,
        "actor_id": actor_id,
        "timestamp": time.time()
    })
    _BLACKLIST.add(nonce)

def is_blacklisted(nonce: str) -> bool:
    """
    Check if nonce has already been used.
    """
    return nonce in _BLACKLIST


class ReplayProtection:
    """
    One-time nonce checker.
    """
    def __init__(self):
        self._seen = set()

    def check(self, nonce: str) -> bool:
        if nonce in self._seen or is_blacklisted(nonce):
            record_replay_attempt(nonce)
            return False
        self._seen.add(nonce)
        return True
