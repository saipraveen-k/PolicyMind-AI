"""
Task 3 (Hard): Decision Making with Justification
Agent must analyze all information and make a final decision with confidence and justification.
"""

import asyncio
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from environment.env import PolicyMindEnvironment
from environment.models import Action, ActionType, EvaluationResult, Decision


class HardTaskGrader:
    """
    Grader for the hard task - decision making with justification.
    Evaluates the quality, accuracy, and reasoning of the final decision.
    """
    
    def __init__(self):
        self.decision_weights = {
            "decision_correctness": 0.4,  # 40% weight for correct decision
            "confidence_accuracy": 0.2,   # 20% weight for confidence calibration
            "justification_quality": 0.2,   # 20% weight for justification quality
            "rule_application": 0.1,       # 10% weight for proper rule application
            "efficiency": 0.1              # 10% weight for efficiency
        }
        
        self.justification_keywords = [
            "because", "since", "due to", "according to", "based on",
            "policy", "coverage", "documentation", "requirements",
            "meets", "exceeds", "within", "complies", "satisfies"
        ]
    
    def evaluate_decision(self, 
                         ground_truth: Dict[str, Any],
                         decision: Decision) -> Dict[str, float]:
        """
        Evaluate the final decision against ground truth.
        
        Args:
            ground_truth: Ground truth data
            decision: The decision made by the agent
            
        Returns:
            Dictionary with evaluation metrics
        """
        # Extract ground truth values
        gt_decision = ground_truth.get("decision", "")
        gt_confidence = ground_truth.get("confidence", 0.0)
        gt_applicable_rules = set(ground_truth.get("applicable_rules", []))
        
        # Evaluate decision correctness
        decision_correct = self._evaluate_decision_correctness(decision.decision, gt_decision)
        
        # Evaluate confidence accuracy
        confidence_accuracy = self._evaluate_confidence_accuracy(decision.confidence, gt_confidence)
        
        # Evaluate justification quality
        justification_score = self._evaluate_justification_quality(decision.justification)
        
        # Evaluate rule application
        applied_rules = set(decision.applied_rules) if decision.applied_rules else set()
        rule_application_score = self._evaluate_rule_application(applied_rules, gt_applicable_rules)
        
        return {
            "decision_correctness": decision_correct,
            "confidence_accuracy": confidence_accuracy,
            "justification_quality": justification_score,
            "rule_application": rule_application_score,
            "applied_rules_count": len(applied_rules),
            "gt_rules_count": len(gt_applicable_rules),
            "rules_overlap": len(applied_rules & gt_applicable_rules)
        }
    
    def _evaluate_decision_correctness(self, predicted: str, ground_truth: str) -> float:
        """
        Evaluate if the decision matches ground truth.
        
        Args:
            predicted: Predicted decision
            ground_truth: Ground truth decision
            
        Returns:
            Correctness score between 0 and 1
        """
        if not predicted or not ground_truth:
            return 0.0
        
        # Exact match
        if predicted.lower().strip() == ground_truth.lower().strip():
            return 1.0
        
        # Partial match for decision categories
        predicted_lower = predicted.lower()
        gt_lower = ground_truth.lower()
        
        # Check for approval/rejection patterns
        approval_words = ["approved", "accept", "grant", "authorize"]
        rejection_words = ["rejected", "deny", "decline", "refuse"]
        review_words = ["review", "investigate", "pending", "needs"]
        
        predicted_category = None
        gt_category = None
        
        for word in approval_words:
            if word in predicted_lower:
                predicted_category = "approved"
            if word in gt_lower:
                gt_category = "approved"
        
        for word in rejection_words:
            if word in predicted_lower:
                predicted_category = "rejected"
            if word in gt_lower:
                gt_category = "rejected"
        
        for word in review_words:
            if word in predicted_lower:
                predicted_category = "review"
            if word in gt_lower:
                gt_category = "review"
        
        if predicted_category and gt_category:
            return 1.0 if predicted_category == gt_category else 0.0
        
        # Fallback to string similarity
        return 0.0
    
    def _evaluate_confidence_accuracy(self, predicted_confidence: float, gt_confidence: float) -> float:
        """
        Evaluate how well the confidence matches ground truth.
        
        Args:
            predicted_confidence: Predicted confidence score
            gt_confidence: Ground truth confidence score
            
        Returns:
            Confidence accuracy score between 0 and 1
        """
        # Calculate absolute difference
        diff = abs(predicted_confidence - gt_confidence)
        
        # Convert to accuracy score (smaller difference = higher score)
        accuracy = max(0.0, 1.0 - diff)
        
        return accuracy
    
    def _evaluate_justification_quality(self, justification: str) -> float:
        """
        Evaluate the quality of the justification.
        
        Args:
            justification: The justification text
            
        Returns:
            Justification quality score between 0 and 1
        """
        if not justification:
            return 0.0
        
        score = 0.0
        
        # Length score (minimum 20 characters for meaningful justification)
        length_score = min(1.0, len(justification) / 100)
        score += length_score * 0.3
        
        # Keyword score (presence of justification keywords)
        justification_lower = justification.lower()
        keyword_count = sum(1 for keyword in self.justification_keywords if keyword in justification_lower)
        keyword_score = min(1.0, keyword_count / 3)  # At least 3 keywords for full score
        score += keyword_score * 0.3
        
        # Structure score (has reasoning components)
        has_cause = any(word in justification_lower for word in ["because", "since", "due to"])
        has_reference = any(word in justification_lower for word in ["policy", "according", "based on"])
        has_conclusion = any(word in justification_lower for word in ["therefore", "thus", "concludes"])
        
        structure_score = (has_cause + has_reference + has_conclusion) / 3
        score += structure_score * 0.4
        
        return min(1.0, score)
    
    def _evaluate_rule_application(self, applied_rules: Set[str], gt_rules: Set[str]) -> float:
        """
        Evaluate how well the agent applied relevant rules.
        
        Args:
            applied_rules: Rules applied by the agent
            gt_rules: Ground truth applicable rules
            
        Returns:
            Rule application score between 0 and 1
        """
        if not gt_rules:
            return 1.0  # No rules to apply, perfect score
        
        if not applied_rules:
            return 0.0  # Failed to apply any rules
        
        # Calculate precision and recall for rule application
        true_positives = len(applied_rules & gt_rules)
        false_positives = len(applied_rules - gt_rules)
        false_negatives = len(gt_rules - applied_rules)
        
        precision = true_positives / len(applied_rules) if applied_rules else 0
        recall = true_positives / len(gt_rules) if gt_rules else 0
        
        # F1 score for balanced evaluation
        if precision + recall > 0:
            f1_score = 2 * (precision * recall) / (precision + recall)
        else:
            f1_score = 0.0
        
        return f1_score
    
    def _calculate_efficiency_score(self, episode_history: List[Dict[str, Any]]) -> float:
        """
        Calculate efficiency score based on action sequence.
        
        Args:
            episode_history: History of actions and observations
            
        Returns:
            Efficiency score between 0 and 1
        """
        total_actions = len(episode_history)
        
        # Expected optimal sequence for hard task:
        # 1. Extract key information
        # 2. Match relevant rules
        # 3. Make decision
        optimal_actions = 3
        
        if total_actions <= optimal_actions:
            return 1.0
        elif total_actions <= optimal_actions + 2:
            return 0.8
        elif total_actions <= optimal_actions + 4:
            return 0.6
        else:
            return max(0.2, 1.0 - (total_actions - optimal_actions) * 0.1)
    
    def grade_episode(self, 
                     environment: PolicyMindEnvironment,
                     episode_history: List[Dict[str, Any]]) -> EvaluationResult:
        """
        Grade the complete episode for the hard task.
        
        Args:
            environment: The environment instance
            episode_history: History of actions and observations
            
        Returns:
            EvaluationResult with detailed scoring
        """
        # Get ground truth and decision
        ground_truth = environment.current_document.ground_truth
        decision = environment.state.observation.current_decision
        
        if not decision:
            # No decision made
            return EvaluationResult(
                task_id=f"{environment.current_document.document_id}_hard",
                score=0.0,
                correctness=0.0,
                completeness=0.0,
                reasoning_quality=0.0,
                feedback="No decision was made. Task requires a final decision with justification.",
                passed=False
            )
        
        # Evaluate decision quality
        decision_metrics = self.evaluate_decision(ground_truth, decision)
        
        # Calculate efficiency score
        efficiency_score = self._calculate_efficiency_score(episode_history)
        
        # Calculate final weighted score
        final_score = (
            decision_metrics["decision_correctness"] * self.decision_weights["decision_correctness"] +
            decision_metrics["confidence_accuracy"] * self.decision_weights["confidence_accuracy"] +
            decision_metrics["justification_quality"] * self.decision_weights["justification_quality"] +
            decision_metrics["rule_application"] * self.decision_weights["rule_application"] +
            efficiency_score * self.decision_weights["efficiency"]
        )
        
        # Determine reasoning quality
        reasoning_quality = (
            decision_metrics["justification_quality"] * 0.5 +
            decision_metrics["rule_application"] * 0.3 +
            efficiency_score * 0.2
        )
        
        # Generate feedback
        if final_score >= 0.8:
            feedback = "Excellent decision-making with strong justification and proper rule application."
        elif final_score >= 0.6:
            feedback = "Good decision with adequate justification and mostly correct rule application."
        elif final_score >= 0.4:
            feedback = "Acceptable decision but justification or rule application needs improvement."
        else:
            feedback = "Poor decision-making. Significant issues with accuracy, justification, or rule application."
        
        # Add specific feedback
        if decision_metrics["decision_correctness"] < 0.5:
            feedback += " Decision was incorrect."
        if decision_metrics["justification_quality"] < 0.5:
            feedback += " Justification was weak or insufficient."
        if decision_metrics["rule_application"] < 0.5:
            feedback += " Rule application was inaccurate."
        
        return EvaluationResult(
            task_id=f"{environment.current_document.document_id}_hard",
            score=final_score,
            correctness=decision_metrics["decision_correctness"],
            completeness=decision_metrics["rule_application"],
            reasoning_quality=reasoning_quality,
            feedback=feedback,
            passed=final_score >= 0.6
        )


async def run_hard_task_example():
    """
    Example run of the hard task to demonstrate functionality.
    """
    print("=== Running Hard Task Example ===")
    
    # Initialize environment
    env = PolicyMindEnvironment(task_difficulty="hard", max_steps=10)
    grader = HardTaskGrader()
    
    # Reset environment
    observation = await env.reset()
    print(f"Document Type: {observation.document_type}")
    print(f"Task: Make final decision with confidence and justification")
    print(f"Document Preview: {observation.document_text[:200]}...")
    
    episode_history = []
    total_reward = 0
    
    # Simulate agent actions
    for step in range(1, 7):
        print(f"\n--- Step {step} ---")
        
        if step == 1:
            # Extract comprehensive information
            action = Action(
                action_type=ActionType.EXTRACT,
                extraction_fields=["claim_id", "incident_date", "estimated_cost", "police_report_filed", "injuries_reported"]
            )
        elif step == 2:
            # Match coverage rules
            action = Action(
                action_type=ActionType.MATCH_RULES,
                rule_keywords=["collision", "coverage", "damage"]
            )
        elif step == 3:
            # Match documentation rules
            action = Action(
                action_type=ActionType.MATCH_RULES,
                rule_keywords=["police", "report", "documentation"]
            )
        elif step == 4:
            # Match condition rules
            action = Action(
                action_type=ActionType.MATCH_RULES,
                rule_keywords=["maintenance", "requirements", "conditions"]
            )
        elif step == 5:
            # Analyze and prepare decision
            action = Action(
                action_type=ActionType.QUERY,
                query="Analyze all extracted information and matched rules to determine claim approval status"
            )
        else:
            # Make final decision
            action = Action(
                action_type=ActionType.MAKE_DECISION,
                decision_data={
                    "decision": "Approved",
                    "confidence": 0.85,
                    "justification": "Claim is approved because the incident meets collision coverage requirements. The police report was filed and confirms the other party was at fault. The estimated cost of $4,250 is within policy limits, and there are no maintenance issues or injuries reported. According to policy rules collision_coverage and police_report_required, all conditions are satisfied.",
                    "applied_rules": ["collision_coverage", "police_report_required", "no_fault_claim"]
                }
            )
        
        # Execute action
        observation, reward, done, info = await env.step(action)
        total_reward += reward.step_reward
        
        print(f"Action: {action.action_type}")
        if action.extraction_fields:
            print(f"Extracting: {action.extraction_fields}")
        elif action.rule_keywords:
            print(f"Matching keywords: {action.rule_keywords}")
        elif action.query:
            print(f"Query: {action.query}")
        elif action.decision_data:
            print(f"Decision: {action.decision_data.get('decision')} (confidence: {action.decision_data.get('confidence')})")
        print(f"Step Reward: {reward.step_reward:.3f}")
        
        episode_history.append({
            "step": step,
            "action": action.dict(),
            "observation": observation.dict(),
            "reward": reward.step_reward
        })
        
        if done:
            break
    
    # Grade the episode
    evaluation = grader.grade_episode(env, episode_history)
    
    print(f"\n=== Episode Results ===")
    print(f"Total Reward: {total_reward:.3f}")
    print(f"Final Score: {evaluation.score:.3f}")
    print(f"Correctness: {evaluation.correctness:.3f}")
    print(f"Completeness: {evaluation.completeness:.3f}")
    print(f"Reasoning Quality: {evaluation.reasoning_quality:.3f}")
    print(f"Passed: {evaluation.passed}")
    print(f"Feedback: {evaluation.feedback}")
    
    return evaluation


if __name__ == "__main__":
    # Run the example
    asyncio.run(run_hard_task_example())
