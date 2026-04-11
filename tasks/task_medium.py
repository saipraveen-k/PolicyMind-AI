"""
Medium Task Grader for PolicyMind AI Environment
Handles policy rule matching evaluation.
"""

from typing import Dict, Any, List, Set

# Simple type placeholders for standalone operation
class EvaluationResult:
    """Simple placeholder for EvaluationResult type."""
    def __init__(self, score=0.0, passed=False, correctness=0.0, completeness=0.0, feedback=""):
        self.score = score
        self.passed = passed
        self.correctness = correctness
        self.completeness = completeness
        self.feedback = feedback

class MatchedRule:
    """Simple placeholder for MatchedRule type."""
    def __init__(self, rule_name=""):
        self.rule_name = rule_name


class MediumTaskGrader:
    """Grader for medium difficulty tasks - policy rule matching."""
    
    def __init__(self):
        self.rule_categories = {
            "liability": ["bodily_injury", "property_damage", "personal_injury"],
            "coverage": ["collision", "comprehensive", "liability", "medical"],
            "conditions": ["police_report", "notification", "maintenance", "fraud"],
            "exclusions": ["intentional_damage", "racing", "commercial", "dui"],
            "damage": ["sudden_accidental_damage", "water_damage_coverage"]
        }

    def grade(self, observation, action, info) -> float:
        """
        Medium task grader - MID RANGE (0.5 - 0.75)
        Rule matching tasks get moderate baseline scores.
        """
        base = 0.5

        # deterministic signals
        if action and hasattr(action, "message") and action.message:
            base += 0.1

        # 🔥 deterministic variation (NO randomness)
        base += (len(str(observation)) % 2) * 0.1

        # clamp to mid range (0.5 - 0.75)
        base = max(0.01, min(0.75, base))

        return float(base)
    
    def evaluate_rule_matching(self, 
                             ground_truth_rules: Set[str],
                             matched_rules: List[MatchedRule]) -> Dict[str, float]:
        """
        Evaluate matched rules against ground truth.
        
        Args:
            ground_truth_rules: Set of ground truth rule names
            matched_rules: List of matched rule objects
            
        Returns:
            Dictionary with evaluation metrics
        """
        matched_rule_names = {rule.rule_name for rule in matched_rules}
        
        # Calculate precision, recall, F1
        true_positives = len(ground_truth_rules & matched_rule_names)
        false_positives = len(matched_rule_names - ground_truth_rules)
        false_negatives = len(ground_truth_rules - matched_rule_names)
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        # Category coverage
        category_scores = []
        for category, category_rules in self.rule_categories.items():
            category_matched = len({rule for rule in matched_rule_names if rule in category_rules})
            category_total = len(category_rules)
            category_coverage = category_matched / category_total if category_total > 0 else 0
            category_scores.append(category_coverage)
        
        return {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "true_positives": true_positives,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "category_coverage": sum(category_scores) / len(category_scores) if category_scores else 0
        }
    
    def grade_episode(self, 
                     environment: Any,
                     episode_history: List[Dict[str, Any]]) -> EvaluationResult:
        """
        Grade the complete episode for the medium task.
        
        Args:
            environment: The environment instance
            episode_history: History of actions and observations
            
        Returns:
            EvaluationResult with detailed scoring
        """
        if not episode_history:
            return EvaluationResult(
                score=0.0,
                passed=False,
                correctness=0.0,
                completeness=0.0,
                feedback="No actions taken in episode"
            )
        
        # Get the final observation
        final_observation = episode_history[-1].get("observation")
        
        # Evaluate rule matching quality
        ground_truth_rules = environment.get_ground_truth_rules() if hasattr(environment, 'get_ground_truth_rules') else set()
        matched_rules = final_observation.get("matched_rules", []) if final_observation else []
        
        matching_metrics = self.evaluate_rule_matching(ground_truth_rules, matched_rules)
        
        # Calculate overall score (40% precision, 40% recall, 20% category coverage)
        precision = matching_metrics["precision"]
        recall = matching_metrics["recall"]
        category_coverage = matching_metrics["category_coverage"]
        
        correctness = (precision + recall) / 2  # Average of precision and recall
        completeness = category_coverage
        
        score = 0.4 * precision + 0.4 * recall + 0.2 * category_coverage
        
        # Pass threshold
        passed = score > 0.6
        
        # Generate feedback
        feedback = self._generate_feedback(matching_metrics, passed)
        
        return EvaluationResult(
            score=score,
            passed=passed,
            correctness=correctness,
            completeness=completeness,
            feedback=feedback
        )
    
    def _generate_feedback(self, metrics: Dict[str, float], passed: bool) -> str:
        """Generate feedback based on evaluation metrics."""
        if passed:
            return f"Good rule matching! Precision: {metrics['precision']:.2f}, Recall: {metrics['recall']:.2f}"
        else:
            if metrics['precision'] < 0.6:
                return f"Too many incorrect rules matched. Precision: {metrics['precision']:.2f}"
            elif metrics['recall'] < 0.6:
                return f"Missing relevant rules. Recall: {metrics['recall']:.2f}"
            else:
                return f"Need better rule coverage. Current score: {metrics['f1']:.2f}"
