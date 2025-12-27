import asyncio
import json
import os
from typing import Dict, Any, Optional
from pyqldb.driver import QldbDriver
from pyqldb.config.retry_policy import RetryPolicy
from .ledger_base import LedgerBase

class QLDBLedger(LedgerBase):
    def __init__(self):
        self.driver = QldbDriver(
            ledger_name=os.getenv("LEDGER_NAME", "IntentAudit"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            retry_policy=RetryPolicy(3)
        )

    async def submit_audit(self, intent, decision, user_id):
        payload = {
            "intent": intent,
            "decision": decision,
            "user_id": user_id,
            "timestamp": asyncio.get_event_loop().time()
        }
        try:
            result = self.driver.execute_lambda(
                lambda txn: txn.execute_statement(
                    "INSERT INTO Audits VALUE ?", payload
                )
            )
            return str(result[0]) if result else None
        except Exception as e:
            print(f"[QLDB] submit error: {e}")
            return None

    async def query_chain(self, doc_id):
        try:
            result = self.driver.execute_lambda(
                lambda txn: list(
                    txn.execute_statement(
                        "SELECT * FROM Audits WHERE metadata.id = ?",
                        doc_id
                    )
                )
            )
            return result[0][0] if result else {}
        except Exception as e:
            print(f"[QLDB] query error: {e}")
            return {}

    async def close(self):
        self.driver.shutdown()
