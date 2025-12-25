import random

class ShadowPPORouter:
    """
    Shadow PPO router.
    Does NOT execute actions.
    Only suggests a provider for comparison.
    """

    def suggest(self, state):
        # Placeholder logic (random for now)
        # Later replaced by PPO model.predict(...)
        providers = ["grok", "gpt", "local"]
        return random.choice(providers)
