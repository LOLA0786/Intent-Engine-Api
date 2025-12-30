from datetime import datetime
from intent_strength import IntentStrengthCalculator
from intent_evolution import IntentEvolutionTracker, EvolutionEvent

def attach_intent_strength(intent_a, intent_b, registry=None):
    calculator = IntentStrengthCalculator(registry or {})
    return calculator.calculate_strength(intent_a, intent_b, datetime.utcnow())

def record_strength_event(intent_id, strength, tracker=None):
    tracker = tracker or IntentEvolutionTracker()
    tracker.record_event(
        EvolutionEvent(
            EvolutionEvent.STRENGTHENED,
            intent_id,
            datetime.utcnow(),
            {"strength": strength}
        )
    )
