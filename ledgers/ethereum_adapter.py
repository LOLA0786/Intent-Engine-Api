import asyncio
import json
import os
from typing import Dict, Any, Optional
from web3 import AsyncWeb3
from eth_account import Account
from .ledger_base import LedgerBase

class EthereumLedger(LedgerBase):
    def __init__(self):
        self.w3 = AsyncWeb3(
            AsyncWeb3.AsyncHTTPProvider(
                os.getenv("ETHEREUM_RPC_URL", "http://localhost:8545")
            )
        )
        self.contract_addr = os.getenv("CONTRACT_ADDR")
        self.private_key = os.getenv("PRIVATE_KEY")
        self.account = Account.from_key(self.private_key)

        with open("abis/AuditChain.json", "r") as f:
            abi = json.load(f)["abi"]

        self.contract = self.w3.eth.contract(
            address=self.contract_addr,
            abi=abi
        )

    async def submit_audit(self, intent, decision, user_id):
        try:
            payload = json.dumps({
                "intent": intent,
                "decision": decision,
                "user_id": user_id,
                "timestamp": asyncio.get_event_loop().time()
            }).encode()

            nonce = await self.w3.eth.get_transaction_count(self.account.address)
            txn = await self.contract.functions.appendAudit(payload).build_transaction({
                "from": self.account.address,
                "nonce": nonce,
                "gas": 200000,
                "gasPrice": await self.w3.eth.gas_price
            })

            signed = self.account.sign_transaction(txn)
            receipt = await self.w3.eth.wait_for_transaction_receipt(
                await self.w3.eth.send_raw_transaction(signed.rawTransaction)
            )
            return receipt.transactionHash.hex()
        except Exception as e:
            print(f"[Ethereum] submit error: {e}")
            return None

    async def query_chain(self, tx_id):
        try:
            result = await self.contract.functions.getAudit(
                bytes.fromhex(tx_id[2:])
            ).call()
            return json.loads(result)
        except Exception as e:
            print(f"[Ethereum] query error: {e}")
            return {}

    async def close(self):
        await self.w3.close()
