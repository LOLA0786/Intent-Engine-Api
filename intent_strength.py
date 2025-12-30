"""
Intent Strength Scoring - Deterministic strength calculation
Part of IntentHub Tier 1 implementation

Replaces vague 'confidence' with measurable 'intent_strength'
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import math


class IntentStrengthCalculator:
    """
    Deterministic intent strength scoring.
    All scores are reproducible given same inputs.
    """
    
    # Weights for strength components
    WEIGHTS = {
        'similarity': 0.35,
        'mutual_signals': 0.30,
        'recency': 0.20,
        'specificity': 0.15
    }
    
    # Recency decay parameters
    RECENCY_HALF_LIFE_DAYS = 14  # Strength halves every 2 weeks
    
    def __init__(self, intent_registry: Dict):
        """
        Args:
            intent_registry: Loaded intent_registry.json
        """
        self.registry = intent_registry
    
    def calculate_strength(
        self, 
        intent_a: Dict, 
        intent_b: Dict,
        timestamp: Optional[datetime] = None
    ) -> float:
        """
        Calculate intent strength between two intents.
        
        Args:
            intent_a: First intent object
            intent_b: Second intent object
            timestamp: Evaluation time (for replay)
        
        Returns:
            Float between 0.0 and 1.0
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        similarity = self._calculate_similarity(intent_a, intent_b)
        mutual = self._calculate_mutual_signals(intent_a, intent_b)
        recency = self._calculate_recency(intent_a, intent_b, timestamp)
        specificity = self._calculate_specificity(intent_a, intent_b)
        
        # Weighted sum
        strength = (
            similarity * self.WEIGHTS['similarity'] +
            mutual * self.WEIGHTS['mutual_signals'] +
            recency * self.WEIGHTS['recency'] +
            specificity * self.WEIGHTS['specificity']
        )
        
        return round(strength, 4)
    
    def _calculate_similarity(self, intent_a: Dict, intent_b: Dict) -> float:
        """Semantic overlap of keywords/categories."""
        keywords_a = set(intent_a.get('keywords', []))
        keywords_b = set(intent_b.get('keywords', []))
        
        if not keywords_a or not keywords_b:
            return 0.0
        
        # Jaccard similarity
        intersection = len(keywords_a & keywords_b)
        union = len(keywords_a | keywords_b)
        
        keyword_sim = intersection / union if union > 0 else 0.0
        
        # Category match bonus
        category_match = 1.0 if intent_a.get('category') == intent_b.get('category') else 0.5
        
        return (keyword_sim * 0.7) + (category_match * 0.3)
    
    def _calculate_mutual_signals(self, intent_a: Dict, intent_b: Dict) -> float:
        """
        Check for complementary signals:
        - Seeking <-> Offering
        - Learning <-> Teaching
        """
        type_a = intent_a.get('type', 'general')
        type_b = intent_b.get('type', 'general')
        
        # Complementary pairs
        complementary = {
            ('seeking', 'offering'): 1.0,
            ('offering', 'seeking'): 1.0,
            ('learning', 'teaching'): 0.9,
            ('teaching', 'learning'): 0.9,
            ('building', 'building'): 0.7,  # Collaboration
        }
        
        pair = (type_a, type_b)
        return complementary.get(pair, 0.5)
    
    def _calculate_recency(
        self, 
        intent_a: Dict, 
        intent_b: Dict, 
        timestamp: datetime
    ) -> float:
        """
        Exponential decay based on intent age.
        Recent intents = higher strength.
        """
        def age_score(intent_timestamp: str) -> float:
            created = datetime.fromisoformat(intent_timestamp.replace('Z', '+00:00'))
            age_days = (timestamp - created).days
            
            # Exponential decay: 0.5^(age/half_life)
            decay = math.pow(0.5, age_days / self.RECENCY_HALF_LIFE_DAYS)
            return max(0.1, decay)  # Floor at 0.1
        
        score_a = age_score(intent_a.get('created_at', timestamp.isoformat()))
        score_b = age_score(intent_b.get('created_at', timestamp.isoformat()))
        
        # Average recency
        return (score_a + score_b) / 2
    
    def _calculate_specificity(self, intent_a: Dict, intent_b: Dict) -> float:
        """
        Reward specific, detailed intents.
        Penalize vague "interested in AI" type intents.
        """
        def specificity_score(intent: Dict) -> float:
            desc = intent.get('description', '')
            keywords = intent.get('keywords', [])
            
            # More keywords = more specific
            keyword_score = min(len(keywords) / 10.0, 1.0)
            
            # Longer descriptions = more specific (up to a point)
            desc_score = min(len(desc.split()) / 50.0, 1.0)
            
            return (keyword_score * 0.6) + (desc_score * 0.4)
        
        spec_a = specificity_score(intent_a)
        spec_b = specificity_score(intent_b)
        
        # Both should be specific for high strength
        return min(spec_a, spec_b)
    
    def explain_strength(
        self, 
        intent_a: Dict, 
        intent_b: Dict,
        timestamp: Optional[datetime] = None
    ) -> Dict:
        """
        Return detailed breakdown for transparency.
        
        Returns:
            {
                'strength': 0.82,
                'components': {
                    'similarity': 0.75,
                    'mutual_signals': 0.90,
                    'recency': 0.85,
                    'specificity': 0.80
                },
                'explanation': 'High match due to complementary types...'
            }
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        similarity = self._calculate_similarity(intent_a, intent_b)
        mutual = self._calculate_mutual_signals(intent_a, intent_b)
        recency = self._calculate_recency(intent_a, intent_b, timestamp)
        specificity = self._calculate_specificity(intent_a, intent_b)
        
        strength = self.calculate_strength(intent_a, intent_b, timestamp)
        
        # Generate explanation
        explanation_parts = []
        if mutual >= 0.8:
            explanation_parts.append("Strong complementary match")
        if similarity >= 0.7:
            explanation_parts.append("High keyword overlap")
        if recency >= 0.7:
            explanation_parts.append("Both intents are recent")
        if specificity < 0.4:
            explanation_parts.append("Could be more specific")
        
        return {
            'strength': strength,
            'components': {
                'similarity': round(similarity, 4),
                'mutual_signals': round(mutual, 4),
                'recency': round(recency, 4),
                'specificity': round(specificity, 4)
            },
            'explanation': '; '.join(explanation_parts) if explanation_parts else 'Standard match',
            'timestamp': timestamp.isoformat()
        }


# CLI for testing
if __name__ == '__main__':
    import sys
    
    # Example intents
    intent_a = {
        'id': 'intent_001',
        'type': 'learning',
        'category': 'ai',
        'keywords': ['react', 'typescript', 'frontend'],
        'description': 'Looking to build modern web apps with React and TypeScript',
        'created_at': '2024-12-20T10:00:00Z'
    }
    
    intent_b = {
        'id': 'intent_002',
        'type': 'teaching',
        'category': 'ai',
        'keywords': ['react', 'nextjs', 'typescript'],
        'description': 'Experienced React developer willing to mentor on modern frontend',
        'created_at': '2024-12-25T15:30:00Z'
    }
    
    calculator = IntentStrengthCalculator({})
    
    result = calculator.explain_strength(intent_a, intent_b)
    
    print(json.dumps(result, indent=2))
    print(f"\n✓ Intent strength: {int(result['strength'] * 100)}%")
