#!/usr/bin/env python3
"""
Test script to verify distinct score ranges for all graders.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tasks.task_easy import EasyTaskGrader
from tasks.task_medium import MediumTaskGrader
from tasks.task_hard import HardTaskGrader

def test_distinct_score_ranges():
    """Test that each grader produces distinct score ranges."""
    
    print("🧪 Testing Distinct Score Ranges")
    print("=" * 50)
    
    # Create grader instances
    easy_grader = EasyTaskGrader()
    medium_grader = MediumTaskGrader()
    hard_grader = HardTaskGrader()
    
    # Test with various inputs
    test_cases = [
        ({"doc": "short"}, type('Action', (), {'message': 'test'})()),
        ({"document_type": "insurance_claim", "content": "Test claim document with more content"}, type('Action', (), {'message': 'Test action message for evaluation'})()),
        ({"data": "very long observation string " * 10}, type('Action', (), {'message': 'A longer action message for testing purposes'})()),
        (None, None),
    ]
    
    print("\n📊 Score Distribution Analysis:")
    print("-" * 30)
    
    easy_scores = []
    medium_scores = []
    hard_scores = []
    
    for obs, act in test_cases:
        easy_score = easy_grader.grade(obs, act, {})
        medium_score = medium_grader.grade(obs, act, {})
        hard_score = hard_grader.grade(obs, act, {})
        
        easy_scores.append(easy_score)
        medium_scores.append(medium_score)
        hard_scores.append(hard_score)
        
        print(f"Input: obs={str(obs)[:30]}...")
        print(f"  Easy:   {easy_score:.2f}")
        print(f"  Medium: {medium_score:.2f}")
        print(f"  Hard:   {hard_score:.2f}")
        print()
    
    # Analyze ranges
    easy_min, easy_max = min(easy_scores), max(easy_scores)
    medium_min, medium_max = min(medium_scores), max(medium_scores)
    hard_min, hard_max = min(hard_scores), max(hard_scores)
    
    print("📈 Score Range Summary:")
    print("-" * 30)
    print(f"Easy:   [{easy_min:.2f}, {easy_max:.2f}]")
    print(f"Medium: [{medium_min:.2f}, {medium_max:.2f}]")
    print(f"Hard:   [{hard_min:.2f}, {hard_max:.2f}]")
    
    # Check for overlaps
    print("\n🔍 Overlap Detection:")
    print("-" * 30)
    
    easy_medium_overlap = easy_max >= medium_min
    medium_hard_overlap = medium_max >= hard_min
    easy_hard_overlap = easy_max >= hard_min
    
    print(f"Easy-Medium overlap: {easy_medium_overlap}")
    print(f"Medium-Hard overlap: {medium_hard_overlap}")
    print(f"Easy-Hard overlap: {easy_hard_overlap}")
    
    # Check if ranges are distinct (no overlap)
    all_distinct = not (easy_medium_overlap or medium_hard_overlap or easy_hard_overlap)
    
    print(f"\n✅ All ranges distinct: {all_distinct}")
    
    # Verify scores are in valid range
    all_valid = all(0.01 <= s <= 0.99 for s in easy_scores + medium_scores + hard_scores)
    print(f"✅ All scores in (0.01, 0.99): {all_valid}")
    
    # Verify determinism
    print("\n🔄 Determinism Test:")
    print("-" * 30)
    test_obs = {"test": "data"}
    test_act = type('Action', (), {'message': 'test message'})()
    
    easy_deterministic = len(set(easy_grader.grade(test_obs, test_act, {}) for _ in range(5))) == 1
    medium_deterministic = len(set(medium_grader.grade(test_obs, test_act, {}) for _ in range(5))) == 1
    hard_deterministic = len(set(hard_grader.grade(test_obs, test_act, {}) for _ in range(5))) == 1
    
    print(f"Easy deterministic: {easy_deterministic}")
    print(f"Medium deterministic: {medium_deterministic}")
    print(f"Hard deterministic: {hard_deterministic}")
    
    return all_distinct and all_valid and easy_deterministic and medium_deterministic and hard_deterministic

if __name__ == "__main__":
    print("🔍 DISTINCT SCORE RANGE VALIDATION")
    print("=" * 50)
    
    success = test_distinct_score_ranges()
    
    print("\n📋 Final Results:")
    print("=" * 50)
    
    if success:
        print("✅ All checks passed!")
        print("✅ Score ranges are distinct")
        print("✅ No overlap between tasks")
        print("✅ All scores in valid range")
        print("✅ All graders are deterministic")
        print("\n🎉 PHASE 2 VALIDATION WILL PASS!")
    else:
        print("❌ Some checks failed - please review")