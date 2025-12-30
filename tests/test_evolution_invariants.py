from datetime import datetime, timedelta
from intent_evolution import IntentEvolutionTracker, EvolutionEvent

tracker = IntentEvolutionTracker("ci_test_audit.jsonl")
intent_id = "ci_user_intent_1"

tracker.record_event(EvolutionEvent(
    EvolutionEvent.CREATED,
    intent_id,
    datetime.utcnow() - timedelta(days=10),
    {"strength": 0.3}
))

tracker.record_event(EvolutionEvent(
    EvolutionEvent.STRENGTHENED,
    intent_id,
    datetime.utcnow() - timedelta(days=5),
    {"strength": 0.7}
))

lifecycle_1 = tracker.get_intent_lifecycle(intent_id)
lifecycle_2 = tracker.get_intent_lifecycle(intent_id)

assert lifecycle_1 == lifecycle_2, "Replay must be deterministic"

print("✅ Evolution replay invariant passed")
