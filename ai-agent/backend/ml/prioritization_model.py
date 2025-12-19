import random

class PrioritizationModel:
    """
    A lightweight model to score task priority.
    """
    def predict(self, task):
        """
        Returns a priority score (0-1) and label (low, medium, high, critical).
        """
        # Rules-based + simple heuristics
        # Features: deadline proximity, keywords
        
        score = 0.5
        
        # Keyword boosting
        title = task.get('title', '').lower()
        if 'urgent' in title or 'asap' in title:
            score += 0.3
        if 'meeting' in title:
            score += 0.2
            
        # Deadline boosting (mock logic as we rely on strings/None for now)
        if task.get('due_date'):
            # In real system, calc delta
            score += 0.2
            
        # Random noise to simulate ML "thinking" for finding hidden patterns
        score += random.uniform(-0.05, 0.05)
        
        score = min(max(score, 0), 1)
        
        if score > 0.8:
            return score, 'critical'
        elif score > 0.6:
            return score, 'high'
        elif score > 0.4:
            return score, 'medium'
        else:
            return score, 'low'
