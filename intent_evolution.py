"""
Intent Evolution Tracker
Replay-based timeline of how intents change over time

Not analytics - pure deterministic state transitions
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict


class EvolutionEvent:
    """Deterministic intent lifecycle event."""

    CREATED = "created"
    ACTIVATED = "activated"
    STRENGTHENED = "strengthened"
    WEAKENED = "weakened"
    MODIFIED = "modified"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"

    def __init__(self, event_type: str, intent_id: str, timestamp: datetime, metadata: Optional[Dict] = None):
        self.event_type = event_type
        self.intent_id = intent_id
        self.timestamp = timestamp
        self.metadata = metadata or {}

    def to_dict(self) -> Dict:
        return {
            "event_type": self.event_type,
            "intent_id": self.intent_id,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }


class IntentEvolutionTracker:
    def __init__(self, audit_log_path: str = "intent_audit.jsonl"):
        self.audit_log_path = audit_log_path
        self.events = self._load_events()

    def _load_events(self) -> List[EvolutionEvent]:
        events = []
        try:
            with open(self.audit_log_path, "r") as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        events.append(
                            EvolutionEvent(
                                data["event_type"],
                                data["intent_id"],
                                datetime.fromisoformat(data["timestamp"]),
                                data.get("metadata", {})
                            )
                        )
        except FileNotFoundError:
            pass
        return sorted(events, key=lambda e: e.timestamp)

    def record_event(self, event: EvolutionEvent):
        with open(self.audit_log_path, "a") as f:
            f.write(json.dumps(event.to_dict()) + "\n")
        self.events.append(event)

    def get_intent_timeline(self, intent_id: str) -> List[Dict]:
        return [
            {
                "timestamp": e.timestamp.isoformat(),
                "event": e.event_type,
                "details": e.metadata
            }
            for e in self.events if e.intent_id == intent_id
        ]

    def get_intent_lifecycle(self, intent_id: str) -> Dict:
        events = [e for e in self.events if e.intent_id == intent_id]
        if not events:
            return None

        first, last = events[0], events[-1]

        strength_history = [e.metadata["strength"] for e in events if "strength" in e.metadata]
        modifications = len([e for e in events if e.event_type == EvolutionEvent.MODIFIED])

        status_events = [
            e for e in events if e.event_type in {
                EvolutionEvent.COMPLETED,
                EvolutionEvent.ARCHIVED,
                EvolutionEvent.PAUSED,
                EvolutionEvent.ACTIVATED
            }
        ]

        status = status_events[-1].event_type if status_events else "active"

        return {
            "intent_id": intent_id,
            "first_appeared": first.timestamp.isoformat(),
            "last_active": last.timestamp.isoformat(),
            "status": status,
            "duration_days": (last.timestamp - first.timestamp).days,
            "strength_history": strength_history,
            "modifications": modifications,
            "total_events": len(events)
        }

    def compute_intent_strength_trend(self, intent_id: str, window_days: int = 14) -> str:
        cutoff = datetime.utcnow() - timedelta(days=window_days)
        recent = [
            e.metadata["strength"]
            for e in self.events
            if e.intent_id == intent_id and e.timestamp >= cutoff and "strength" in e.metadata
        ]

        if len(recent) < 2:
            return "insufficient_data"

        mid = len(recent) // 2
        diff = sum(recent[mid:]) / len(recent[mid:]) - sum(recent[:mid]) / mid

        if diff > 0.1:
            return "strengthening"
        if diff < -0.1:
            return "weakening"
        return "stable"


# CLI TEST
if __name__ == "__main__":
    tracker = IntentEvolutionTracker("test_intent_audit.jsonl")
    intent_id = "user_alice_intent_1"

    tracker.record_event(EvolutionEvent(EvolutionEvent.CREATED, intent_id, datetime.utcnow() - timedelta(days=20), {"strength": 0.3}))
    tracker.record_event(EvolutionEvent(EvolutionEvent.STRENGTHENED, intent_id, datetime.utcnow() - timedelta(days=15), {"strength": 0.6}))
    tracker.record_event(EvolutionEvent(EvolutionEvent.STRENGTHENED, intent_id, datetime.utcnow() - timedelta(days=8), {"strength": 0.85}))
    tracker.record_event(EvolutionEvent(EvolutionEvent.COMPLETED, intent_id, datetime.utcnow(), {"final_strength": 0.9}))

    print(json.dumps(tracker.get_intent_lifecycle(intent_id), indent=2))
    print("Trend:", tracker.compute_intent_strength_trend(intent_id))
