import asyncio
from ledgers.worm_fallback import WORMFallback

async def main():
    ledger = WORMFallback()
    tx = await ledger.submit_audit(
        {"action": "transfer"},
        {"allow": True},
        "user123"
    )
    print("TX:", tx)
    data = await ledger.query_chain(tx)
    print("DATA:", data)

asyncio.run(main())
