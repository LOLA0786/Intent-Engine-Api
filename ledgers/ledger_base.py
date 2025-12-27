from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class LedgerBase(ABC):
    @abstractmethod
    async def submit_audit(
        self,
        intent: Dict[str, Any],
        decision: Dict[str, Any],
        user_id: str
    ) -> Optional[str]:
        pass

    @abstractmethod
    async def query_chain(self, id_: str) -> Dict[str, Any]:
        pass

    async def close(self):
        pass


def get_ledger(ledger_type: str) -> "LedgerBase":
    """
    Lazy-loaded ledger factory.
    Only imports the backend actually requested.
    """

    ledger_type = ledger_type.lower()

    if ledger_type == "fabric":
        from .fabric_integration import FabricLedger
        return FabricLedger()

    if ledger_type in ("quorum", "besu", "ethereum"):
        from .ethereum_adapter import EthereumLedger
        return EthereumLedger()

    if ledger_type == "qldb":
        from .qldb_adapter import QLDBLedger
        return QLDBLedger()

    if ledger_type == "cosmos":
        from .cosmos_adapter import CosmosLedger
        return CosmosLedger()

    if ledger_type == "worm":
        from .worm_fallback import WORMFallback
        return WORMFallback()

    # Safe default: no external deps
    from .worm_fallback import WORMFallback
    return WORMFallback()
