import asyncio
import json
import os
from typing import Dict, Any, Optional
from hfc.fabric import Client
from hfc.fabric_network.gateway import Gateway
from .ledger_base import LedgerBase

class FabricLedger(LedgerBase):
    def __init__(self):
        self.net_profile = os.getenv("FABRIC_CONNECTION", "./network.json")
        self.channel = os.getenv("CHANNEL_NAME", "mychannel")
        self.cc_name = os.getenv("CHAINCODE_NAME", "auditchain")
        self.wallet = os.getenv("FABRIC_WALLET", "./wallet")
        self.gateway: Optional[Gateway] = None
        self.client = Client(net_profile=self.net_profile)

    async def connect(self):
        if not self.gateway:
            self.gateway = Gateway()
            await self.gateway.connect(self.net_profile, {"wallet": self.wallet})

    async def submit_audit(self, intent, decision, user_id):
        try:
            await self.connect()
            network = await self.gateway.get_network(self.channel)
            contract = network.get_contract(self.cc_name)

            payload = json.dumps({
                "intent": intent,
                "decision": decision,
                "user_id": user_id,
                "timestamp": asyncio.get_event_loop().time()
            })

            resp = await contract.submit_transaction("appendAudit", payload)
            return resp.decode()
        except Exception as e:
            print(f"[Fabric] submit error: {e}")
            return None

    async def query_chain(self, tx_id):
        try:
            await self.connect()
            network = await self.gateway.get_network(self.channel)
            contract = network.get_contract(self.cc_name)
            data = await contract.evaluate_transaction("getAudit", tx_id)
            return json.loads(data.decode())
        except Exception as e:
            print(f"[Fabric] query error: {e}")
            return {}

    async def close(self):
        if self.gateway:
            await self.gateway.close()
