"""
Task 1 (Easy): Document Information Extraction
Agent must extract structured fields from insurance/policy documents.
"""

import asyncio
import json
import re
from typing import Dict, List, Any, Optional
from environment.env import PolicyMindEnvironment
from environment.models import Action, ActionType, EvaluationResult


class EasyTaskGrader:
    """
    Grader for the easy task - document information extraction.
    Evaluates the accuracy and completeness of extracted information.
    """
    
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
        # Convert extracted fields to dictionary
        extracted_dict = {}
        for field in extracted_fields:
            if isinstance(field, dict):
                field_name = field.get("field_name")
                field_value = field.get("value")
            else:
                # Handle ExtractedField objects
                field_name = field.field_name
                field_value = field.value
            
            if field_name:
                extracted_dict[field_name] = field_value
        
        # Calculate metrics
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
                     environment: PolicyMindEnvironment,
                     episode_history: List[Dict[str, Any]]) -> EvaluationResult:
        """
        Grade the complete episode for the easy task.
        
        Args:
            environment: The environment instance
            episode_history: History of actions and observations
            
        Returns:
            EvaluationResult with detailed scoring
        """
        # Get ground truth and extracted fields
        ground_truth = environment.current_document.ground_truth.get("extracted_fields", {})
        extracted_fields = environment.state.observation.extracted_fields
        
        # Evaluate extraction quality
        metrics = self.evaluate_extraction(ground_truth, [field.dict() if hasattr(field, 'dict') else field for field in extracted_fields])
        
        # Calculate final score
        accuracy_score = metrics["accuracy"] * 0.5  # 50% weight
        completeness_score = metrics["completeness"] * 0.3  # 30% weight
        required_score = metrics["required_completeness"] * 0.2  # 20% weight
        
        final_score = accuracy_score + completeness_score + required_score
        
        # Determine reasoning quality based on action efficiency
        total_actions = len(episode_history)
        efficiency_bonus = max(0, 1.0 - (total_actions - 3) * 0.1)  # Bonus for efficiency
        reasoning_quality = min(1.0, efficiency_bonus)
        
        # Generate feedback
        if final_score >= 0.9:
            feedback = "Outstanding extraction! All key fields identified accurately."
        elif final_score >= 0.7:
            feedback = "Good extraction with most fields correctly identified."
        elif final_score >= 0.5:
            feedback = "Acceptable extraction but some important fields missed."
        else:
            feedback = "Poor extraction. Many key fields were missed or incorrect."
        
        # Add specific feedback
        if metrics["extracted_fields"] < metrics["total_fields"] * 0.5:
            feedback += f" Only {metrics['extracted_fields']}/{metrics['total_fields']} fields were extracted."
        
        return EvaluationResult(
            task_id=f"{environment.current_document.document_id}_easy",
            score=final_score,
            correctness=metrics["accuracy"],
            completeness=metrics["completeness"],
            reasoning_quality=reasoning_quality,
            feedback=feedback,
            passed=final_score >= 0.6
        )


async def run_easy_task_example():
    """
    Example run of the easy task to demonstrate functionality.
    """
    print("=== Running Easy Task Example ===")
    
    # Initialize environment
    env = PolicyMindEnvironment(task_difficulty="easy", max_steps=5)
    grader = EasyTaskGrader()
    
    # Reset environment
    observation = await env.reset()
    print(f"Document Type: {observation.document_type}")
    print(f"Task: Extract structured information from policy document")
    print(f"Document Preview: {observation.document_text[:200]}...")
    
    episode_history = []
    total_reward = 0
    
    # Simulate agent actions
    for step in range(1, 4):
        print(f"\n--- Step {step} ---")
        
        if step == 1:
            # Extract basic identifiers
            action = Action(
                action_type=ActionType.EXTRACT,
                extraction_fields=["policy_type", "liability_limit", "collision_deductible"]
            )
        elif step == 2:
            # Extract more detailed information
            action = Action(
                action_type=ActionType.EXTRACT,
                extraction_fields=["comprehensive_deductible", "police_report_threshold"]
            )
        else:
            # Final extraction
            action = Action(
                action_type=ActionType.EXTRACT,
                extraction_fields=["notification_period_days"]
            )
        
        # Execute action
        observation, reward, done, info = await env.step(action)
        total_reward += reward.step_reward
        
        print(f"Action: {action.action_type}")
        if action.extraction_fields:
            print(f"Extracting: {action.extraction_fields}")
        print(f"Step Reward: {reward.step_reward:.3f}")
        print(f"Extracted Fields: {[f.field_name for f in observation.extracted_fields]}")
        
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
    print(f"Passed: {evaluation.passed}")
    print(f"Feedback: {evaluation.feedback}")
    
    return evaluation


if __name__ == "__main__":
    # Run the example
    asyncio.run(run_easy_task_example())
