#!/usr/bin/env python3
"""
Test script to verify deterministic behavior of updated graders.
This demonstrates that the same inputs produce identical outputs.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tasks.task_easy import EasyTaskGrader
from tasks.task_medium import MediumTaskGrader
from tasks.task_hard import HardTaskGrader

def test_deterministic_graders():
    """Test that all graders produce deterministic outputs."""
    
    print("🧪 Testing Deterministic Graders")
    print("=" * 50)
    
    # Create grader instances
    easy_grader = EasyTaskGrader()
    medium_grader = MediumTaskGrader()
    hard_grader = HardTaskGrader()
    
    # Test inputs
    test_observation = {"document_type": "insurance_claim", "content": "Test claim document"}
    test_action = type('Action', (), {'message': 'Test action message for evaluation'})()
    test_info = {}
    
    print("\n📊 Testing Easy Task Grader:")
    print("-" * 30)
    easy_scores = []
    for i in range(5):
        score = easy_grader.grade(test_observation, test_action, test_info)
        easy_scores.append(score)
        print(f"Run {i+1}: {score}")
    
    print(f"✅ All scores identical: {len(set(easy_scores)) == 1}")
    print(f"✅ Score range (0.01-0.99): {all(0.01 <= s <= 0.99 for s in easy_scores)}")
    
    print("\n📊 Testing Medium Task Grader:")
    print("-" * 30)
    medium_scores = []
    for i in range(5):
        score = medium_grader.grade(test_observation, test_action, test_info)
        medium_scores.append(score)
        print(f"Run {i+1}: {score}")
    
    print(f"✅ All scores identical: {len(set(medium_scores)) == 1}")
    print(f"✅ Score range (0.01-0.99): {all(0.01 <= s <= 0.99 for s in medium_scores)}")
    
    print("\n📊 Testing Hard Task Grader:")
    print("-" * 30)
    hard_scores = []
    for i in range(5):
        score = hard_grader.grade(test_observation, test_action, test_info)
        hard_scores.append(score)
        print(f"Run {i+1}: {score}")
    
    print(f"✅ All scores identical: {len(set(hard_scores)) == 1}")
    print(f"✅ Score range (0.01-0.99): {all(0.01 <= s <= 0.99 for s in hard_scores)}")
    
    print("\n🧪 Testing Different Inputs (Variation):")
    print("=" * 50)
    
    # Different observation
    different_observation = {"document_type": "policy_document", "content": "Different policy document"}
    
    easy_score_1 = easy_grader.grade(test_observation, test_action, test_info)
    easy_score_2 = easy_grader.grade(different_observation, test_action, test_info)
    
    print(f"Easy grader - Same input: {easy_score_1}")
    print(f"Easy grader - Different input: {easy_score_2}")
    print(f"✅ Scores vary logically: {easy_score_1 != easy_score_2}")
    
    medium_score_1 = medium_grader.grade(test_observation, test_action, test_info)
    medium_score_2 = medium_grader.grade(different_observation, test_action, test_info)
    
    print(f"Medium grader - Same input: {medium_score_1}")
    print(f"Medium grader - Different input: {medium_score_2}")
    print(f"✅ Scores vary logically: {medium_score_1 != medium_score_2}")
    
    hard_score_1 = hard_grader.grade(test_observation, test_action, test_info)
    hard_score_2 = hard_grader.grade(different_observation, test_action, test_info)
    
    print(f"Hard grader - Same input: {hard_score_1}")
    print(f"Hard grader - Different input: {hard_score_2}")
    print(f"✅ Scores vary logically: {hard_score_1 != hard_score_2}")
    
    print("\n📋 Final Verification:")
    print("=" * 50)
    
    all_scores = easy_scores + medium_scores + hard_scores
    all_deterministic = all(len(set(scores)) == 1 for scores in [easy_scores, medium_scores, hard_scores])
    all_in_range = all(0.01 <= s <= 0.99 for s in all_scores)
    
    print(f"✅ All graders deterministic: {all_deterministic}")
    print(f"✅ All scores in range (0.01-0.99): {all_in_range}")
    print(f"✅ No randomness imports: {not any('random' in open(f'./tasks/task_{task}.py').read() for task in ['easy', 'medium', 'hard'])}")
    
    return all_deterministic and all_in_range

if __name__ == "__main__":
    success = test_deterministic_gradings()
    if success:
        print("\n🎉 PHASE 2 VALIDATION WILL PASS!")
    else:
        print("\n❌ Issues detected - please review")