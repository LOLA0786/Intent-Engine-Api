import asyncio
import json
import os
import hashlib
from typing import Dict, Any, Optional
from cosmospy import Transaction
from cosmospy.aerial.client import LedgerClient
from cosmospy.aerial.wallet import LocalWallet
from .ledger_base import LedgerBase

class CosmosLedger(LedgerBase):
    """
    Cosmos adapter used as a PUBLIC HASH ANCHOR.
    Stores hash of audit payload on-chain (memo),
    full payload remains off-chain.
    """

    def __init__(self):
        self.rpc = os.getenv("COSMOS_RPC", "https://rpc.testnet.cosmos.network:443")
        self.chain_id = os.getenv("CHAIN_ID", "theta-testnet-001")
        self.mnemonic = os.getenv("MNEMONIC")

        if not self.mnemonic:
            raise RuntimeError("MNEMONIC env var required for CosmosLedger")

        self.client = LedgerClient(self.rpc)
        self.wallet = LocalWallet.from_mnemonic(self.mnemonic)

    async def submit_audit(
        self,
        intent: Dict[str, Any],
        decision: Dict[str, Any],
        user_id: str
    ) -> Optional[str]:
        try:
            payload = json.dumps({
                "intent": intent,
                "decision": decision,
                "user_id": user_id,
                "timestamp": asyncio.get_event_loop().time()
            }, sort_keys=True)

            # Canonical hash anchor
            payload_hash = hashlib.sha256(payload.encode()).hexdigest()

            tx = (
                Transaction()
                .with_messages({
                    "@type": "/cosmos.bank.v1beta1.MsgSend",
                    "from_address": self.wallet.address(),
                    "to_address": self.wallet.address(),
                    "amount": [{"denom": "uatom", "amount": "1"}]
                })
                .with_memo(f"uaal_audit:{payload_hash}")
                .with_gas(200000)
                .with_fee(5000)
            )

            signed = self.wallet.sign_transaction(tx, self.chain_id)
            tx_hash = self.client.broadcast_tx(signed)

            return tx_hash  # immutable proof
        except Exception as e:
            print(f"[Cosmos] submit error: {e}")
            return None

    async def query_chain(self, tx_hash: str) -> Dict[str, Any]:
        try:
            tx = self.client.get_tx(tx_hash)
            memo = tx.get("tx", {}).get("body", {}).get("memo", "")
            if memo.startswith("uaal_audit:"):
                return {"hash": memo.replace("uaal_audit:", "")}
            return {}
        except Exception as e:
            print(f"[Cosmos] query error: {e}")
            return {}

    async def close(self):
        pass  # stateless
