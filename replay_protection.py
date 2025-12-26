import redis
import hashlib
import os
from datetime import datetime
from typing import Optional

class ReplayProtector:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(
            os.getenv("REDIS_URL", "redis://localhost:6379"),
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=True,
            socket_connect_timeout=2,
            retry_on_timeout=True
        )
        self.ttl = 1800  # 30 min

    def generate_nonce(self, user_id: str, tenant_id: str, timestamp: str) -> str:
        """Generate unique nonce."""
        payload = f"{timestamp}{user_id}{tenant_id}"
        return hashlib.sha256(payload.encode()).hexdigest()[:32]

    async def check_and_cache_nonce(self, nonce: str, user_id: str, tenant_id: str) -> bool:
        """Check if nonce used; cache if new. Returns True if fresh."""
        key = f"nonce:{tenant_id}:{user_id}:{nonce}"
        try:
            if self.redis_client.exists(key):
                return False  # Replay
            self.redis_client.setex(key, self.ttl, "used")
            return True
        except Exception:
            # Fail-closed: Assume replay on error
            return False

# Global instance
protector = ReplayProtector()
