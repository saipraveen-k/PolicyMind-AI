"""
Task 2 (Medium): Policy Rule Matching
Agent must identify and match relevant policy clauses to the document content.
"""

import asyncio
import json
from typing import Dict, List, Any, Set, Optional
from environment.env import PolicyMindEnvironment
from environment.models import Action, ActionType, EvaluationResult, MatchedRule


class MediumTaskGrader:
    """
    Grader for the medium task - policy rule matching.
    Evaluates the accuracy and relevance of matched policy rules.
    """
    
    def __init__(self):
        self.rule_categories = {
            "coverage": ["collision_coverage", "comprehensive_coverage", "liability_coverage"],
            "documentation": ["police_report_required", "documentation_required"],
            "conditions": ["maintenance_required", "cooperation_clause"],
            "liability": ["no_fault_claim", "fault_determination"],
            "damage": ["sudden_accidental_damage", "water_damage_coverage"]
        }
    
    def evaluate_rule_matching(self, 
                             ground_truth_rules: Set[str],
                             matched_rules: List[MatchedRule]) -> Dict[str, float]:
        """
        Evaluate matched rules against ground truth.
        
        Args:
            ground_truth_rules: Set of ground truth rule IDs
            matched_rules: List of matched rule objects
            
        Returns:
            Dictionary with evaluation metrics
        """
        # Extract rule IDs from matched rules
        predicted_rules = set()
        rule_relevance = {}
        
        for rule in matched_rules:
            if isinstance(rule, dict):
                rule_id = rule.get("rule_id")
                relevance = rule.get("relevance_score", 0.0)
            else:
                rule_id = rule.rule_id
                relevance = rule.relevance_score
            
            if rule_id:
                predicted_rules.add(rule_id)
                rule_relevance[rule_id] = relevance
        
        # Calculate basic metrics
        true_positives = len(ground_truth_rules & predicted_rules)
        false_positives = len(predicted_rules - ground_truth_rules)
        false_negatives = len(ground_truth_rules - predicted_rules)
        
        # Calculate precision, recall, F1
        precision = true_positives / len(predicted_rules) if predicted_rules else 0
        recall = true_positives / len(ground_truth_rules) if ground_truth_rules else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        # Calculate category coverage
        category_coverage = self._calculate_category_coverage(ground_truth_rules, predicted_rules)
        
        # Calculate average relevance score for correctly matched rules
        avg_relevance = 0.0
        if true_positives > 0:
            correctly_matched_relevance = [rule_relevance[rule_id] for rule_id in ground_truth_rules & predicted_rules]
            avg_relevance = sum(correctly_matched_relevance) / len(correctly_matched_relevance)
        
        return {
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "true_positives": true_positives,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "category_coverage": category_coverage,
            "avg_relevance": avg_relevance,
            "total_predicted": len(predicted_rules),
            "total_ground_truth": len(ground_truth_rules)
        }
    
    def _calculate_category_coverage(self, ground_truth_rules: Set[str], predicted_rules: Set[str]) -> float:
        """
        Calculate how well different rule categories are covered.
        
        Args:
            ground_truth_rules: Set of ground truth rule IDs
            predicted_rules: Set of predicted rule IDs
            
        Returns:
            Category coverage score
        """
        category_scores = []
        
        for category, rule_list in self.rule_categories.items():
            gt_category_rules = set(rule_list) & ground_truth_rules
            pred_category_rules = set(rule_list) & predicted_rules
            
            if gt_category_rules:
                coverage = len(gt_category_rules & pred_category_rules) / len(gt_category_rules)
                category_scores.append(coverage)
        
        return sum(category_scores) / len(category_scores) if category_scores else 0
    
    def grade_episode(self, 
                     environment: PolicyMindEnvironment,
                     episode_history: List[Dict[str, Any]]) -> EvaluationResult:
        """
        Grade the complete episode for the medium task.
        
        Args:
            environment: The environment instance
            episode_history: History of actions and observations
            
        Returns:
            EvaluationResult with detailed scoring
        """
        # Get ground truth and matched rules
        ground_truth_rules = set(environment.current_document.ground_truth.get("applicable_rules", []))
        matched_rules = environment.state.observation.matched_rules
        
        # Evaluate rule matching quality
        metrics = self.evaluate_rule_matching(ground_truth_rules, matched_rules)
        
        # Calculate final score components
        f1_score = metrics["f1_score"] * 0.4  # 40% weight for F1 score
        category_score = metrics["category_coverage"] * 0.2  # 20% weight for category coverage
        relevance_score = metrics["avg_relevance"] * 0.2  # 20% weight for relevance
        efficiency_score = self._calculate_efficiency_score(episode_history) * 0.2  # 20% weight for efficiency
        
        final_score = f1_score + category_score + relevance_score + efficiency_score
        
        # Determine reasoning quality
        reasoning_quality = min(1.0, (metrics["precision"] + metrics["recall"]) / 2)
        
        # Generate feedback
        if final_score >= 0.8:
            feedback = "Excellent rule matching! All relevant policies identified with high precision."
        elif final_score >= 0.6:
            feedback = "Good rule matching with most relevant policies correctly identified."
        elif final_score >= 0.4:
            feedback = "Acceptable rule matching but some important policies were missed."
        else:
            feedback = "Poor rule matching. Many relevant policies were not identified."
        
        # Add specific feedback
        if metrics["false_positives"] > 0:
            feedback += f" {metrics['false_positives']} irrelevant rules were matched."
        if metrics["false_negatives"] > 0:
            feedback += f" {metrics['false_negatives']} relevant rules were missed."
        
        return EvaluationResult(
            task_id=f"{environment.current_document.document_id}_medium",
            score=final_score,
            correctness=metrics["precision"],
            completeness=metrics["recall"],
            reasoning_quality=reasoning_quality,
            feedback=feedback,
            passed=final_score >= 0.6
        )
    
    def _calculate_efficiency_score(self, episode_history: List[Dict[str, Any]]) -> float:
        """
        Calculate efficiency score based on number of actions taken.
        
        Args:
            episode_history: History of actions and observations
            
        Returns:
            Efficiency score between 0 and 1
        """
        total_actions = len(episode_history)
        optimal_actions = 3  # Expected optimal number of actions
        
        if total_actions <= optimal_actions:
            return 1.0
        elif total_actions <= optimal_actions * 2:
            return 0.8
        elif total_actions <= optimal_actions * 3:
            return 0.6
        else:
            return max(0.2, 1.0 - (total_actions - optimal_actions) * 0.1)


async def run_medium_task_example():
    """
    Example run of the medium task to demonstrate functionality.
    """
    print("=== Running Medium Task Example ===")
    
    # Initialize environment
    env = PolicyMindEnvironment(task_difficulty="medium", max_steps=8)
    grader = MediumTaskGrader()
    
    # Reset environment
    observation = await env.reset()
    print(f"Document Type: {observation.document_type}")
    print(f"Task: Match relevant policy rules to claim document")
    print(f"Available Rules: {len(observation.policy_rules)}")
    print(f"Document Preview: {observation.document_text[:200]}...")
    
    episode_history = []
    total_reward = 0
    
    # Simulate agent actions
    for step in range(1, 6):
        print(f"\n--- Step {step} ---")
        
        if step == 1:
            # Extract basic information first
            action = Action(
                action_type=ActionType.EXTRACT,
                extraction_fields=["claim_id", "incident_date", "estimated_cost"]
            )
        elif step == 2:
            # Match coverage-related rules
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
                rule_keywords=["maintenance", "conditions", "requirements"]
            )
        else:
            # Final decision
            action = Action(
                action_type=ActionType.MAKE_DECISION,
                decision_data={
                    "decision": "Approved",
                    "confidence": 0.85,
                    "justification": "Claim meets all coverage requirements with proper documentation",
                    "applied_rules": ["collision_coverage", "police_report_required"]
                }
            )
        
        # Execute action
        observation, reward, done, info = await env.step(action)
        total_reward += reward.step_reward
        
        print(f"Action: {action.action_type}")
        if action.rule_keywords:
            print(f"Matching keywords: {action.rule_keywords}")
        if action.decision_data:
            print(f"Decision: {action.decision_data.get('decision')}")
        print(f"Step Reward: {reward.step_reward:.3f}")
        print(f"Matched Rules: {[r.rule_id for r in observation.matched_rules]}")
        
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
    print(f"Correctness (Precision): {evaluation.correctness:.3f}")
    print(f"Completeness (Recall): {evaluation.completeness:.3f}")
    print(f"Reasoning Quality: {evaluation.reasoning_quality:.3f}")
    print(f"Passed: {evaluation.passed}")
    print(f"Feedback: {evaluation.feedback}")
    
    return evaluation


if __name__ == "__main__":
    # Run the example
    asyncio.run(run_medium_task_example())
