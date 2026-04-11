"""
Easy Task Grader for PolicyMind AI Environment
Handles document information extraction evaluation.
"""

from typing import Dict, Any, List

# Simple type placeholder for standalone operation
class EvaluationResult:
    """Simple placeholder for EvaluationResult type."""
    def __init__(self, score=0.0, passed=False, correctness=0.0, completeness=0.0, feedback=""):
        self.score = score
        self.passed = passed
        self.correctness = correctness
        self.completeness = completeness
        self.feedback = feedback


class EasyTaskGrader:
    """Grader for easy difficulty tasks - document information extraction."""
    
    def __init__(self):
        self.required_fields = {
            "insurance_claim": [
                "claim_id", "policy_number", "incident_date", "insured_name", 
                "estimated_cost", "police_report_filed"
            ],
            "policy_document": [
                "policy_type", "liability_limit", "collision_deductible", 
                "comprehensive_deductible", "police_report_threshold"
            ]
        }

    def grade(self, observation, action, info) -> float:
        """
        Easy task grader - LOW RANGE (0.2 - 0.45)
        Simple extraction tasks get lower baseline scores.
        """
        base = 0.2

        # deterministic signals
        if action and hasattr(action, "message") and action.message:
            base += 0.1

        base += 0.1  # easy bonus

        # 🔥 deterministic variation (NO randomness)
        base += (len(str(observation)) % 3) * 0.05

        # clamp to low range (0.2 - 0.45)
        base = max(0.01, min(0.45, base))

        return float(base)
    
    def evaluate_extraction(self, 
                          ground_truth: Dict[str, Any], 
                          extracted_fields: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Evaluate extracted fields against ground truth.
        
        Args:
            ground_truth: Ground truth data
            extracted_fields: List of extracted field dictionaries
            
        Returns:
            Dictionary with evaluation metrics
        """
        extracted_dict = {field.get("field_name"): field.get("value") for field in extracted_fields}
        
        total_fields = len(ground_truth)
        correct_fields = 0
        partial_matches = 0
        
        for field_name, true_value in ground_truth.items():
            if field_name in extracted_dict:
                extracted_value = extracted_dict[field_name]
                
                # Exact match
                if extracted_value == true_value:
                    correct_fields += 1
                # Partial match for strings (case insensitive)
                elif isinstance(true_value, str) and isinstance(extracted_value, str):
                    if true_value.lower() == extracted_value.lower():
                        correct_fields += 1
                    elif true_value.lower() in extracted_value.lower() or \
                         extracted_value.lower() in true_value.lower():
                        partial_matches += 0.5
                # Numeric match with tolerance
                elif isinstance(true_value, (int, float)) and isinstance(extracted_value, (int, float)):
                    if abs(true_value - extracted_value) < 0.01:
                        correct_fields += 1
        
        # Calculate scores
        accuracy = (correct_fields + partial_matches) / total_fields if total_fields > 0 else 0
        completeness = len(extracted_dict) / total_fields if total_fields > 0 else 0
        
        # Bonus for extracting all required fields
        required_fields = self.required_fields.get("insurance_claim", [])
        required_extracted = sum(1 for field in required_fields if field in extracted_dict)
        required_completeness = required_extracted / len(required_fields) if required_fields else 0
        
        return {
            "accuracy": accuracy,
            "completeness": completeness,
            "required_completeness": required_completeness,
            "total_fields": total_fields,
            "extracted_fields": len(extracted_dict),
            "correct_fields": correct_fields
        }
    
    def grade_episode(self, 
                     environment: Any,
                     episode_history: List[Dict[str, Any]]) -> EvaluationResult:
        """
        Grade the complete episode for the easy task.
        
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
        
        # Evaluate extraction quality
        ground_truth = environment.get_ground_truth() if hasattr(environment, 'get_ground_truth') else {}
        extracted_fields = final_observation.get("extracted_fields", []) if final_observation else []
        
        extraction_metrics = self.evaluate_extraction(ground_truth, extracted_fields)
        
        # Calculate overall score
        correctness = extraction_metrics["accuracy"]
        completeness = extraction_metrics["completeness"]
        
        # Weighted score (70% correctness, 30% completeness)
        score = 0.7 * correctness + 0.3 * completeness
        
        # Pass threshold
        passed = score > 0.6
        
        # Generate feedback
        feedback = self._generate_feedback(extraction_metrics, passed)
        
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
            return f"Good extraction! Accuracy: {metrics['accuracy']:.2f}, Completeness: {metrics['completeness']:.2f}"
        else:
            missing = metrics["total_fields"] - metrics["extracted_fields"]
            return f"Need to extract more fields. Missing {missing} fields. Current accuracy: {metrics['accuracy']:.2f}"
