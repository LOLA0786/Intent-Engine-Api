import json
import os
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from .ledger_base import LedgerBase

class WORMFallback(LedgerBase):
    def __init__(self):
        self.file = os.getenv("WORM_FILE", "./audits.worm")

    async def submit_audit(self, intent, decision, user_id):
        try:
            payload = json.dumps({
                "intent": intent,
                "decision": decision,
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            })
            h = hashlib.sha256(payload.encode()).hexdigest()
            with open(self.file, "a") as f:
                f.write(f"{h}:{payload}\n")
            return h
        except Exception as e:
            print(f"[WORM] submit error: {e}")
            return None

    async def query_chain(self, hash_id):
        try:
            with open(self.file, "r") as f:
                for line in f:
                    h, payload = line.strip().split(":", 1)
                    if h == hash_id:
                        return json.loads(payload)
            return {}
        except Exception as e:
            print(f"[WORM] query error: {e}")
            return {}

    async def close(self):
        pass
