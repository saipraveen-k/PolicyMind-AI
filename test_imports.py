#!/usr/bin/env python3
"""
Test script to verify that grader imports work correctly.
This tests the exact import pattern the validator uses.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_grader_imports():
    """Test that all grader classes can be imported successfully."""
    
    print("🧪 Testing Grader Imports")
    print("=" * 50)
    
    try:
        # Test the exact imports the validator uses
        from tasks.task_easy import EasyTaskGrader
        print("✅ EasyTaskGrader imported successfully")
        
        from tasks.task_medium import MediumTaskGrader
        print("✅ MediumTaskGrader imported successfully")
        
        from tasks.task_hard import HardTaskGrader
        print("✅ HardTaskGrader imported successfully")
        
        # Test that we can instantiate them
        easy_grader = EasyTaskGrader()
        medium_grader = MediumTaskGrader()
        hard_grader = HardTaskGrader()
        
        print("✅ All graders instantiated successfully")
        
        # Test that grade() method exists and is callable
        test_observation = {"test": "data"}
        test_action = type('Action', (), {'message': 'test message'})()
        test_info = {}
        
        easy_score = easy_grader.grade(test_observation, test_action, test_info)
        medium_score = medium_grader.grade(test_observation, test_action, test_info)
        hard_score = hard_grader.grade(test_observation, test_action, test_info)
        
        print(f"✅ Easy grader score: {easy_score}")
        print(f"✅ Medium grader score: {medium_score}")
        print(f"✅ Hard grader score: {hard_score}")
        
        # Verify scores are in valid range
        scores_valid = all(0.01 <= s <= 0.99 for s in [easy_score, medium_score, hard_score])
        print(f"✅ All scores in valid range (0.01-0.99): {scores_valid}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_tasks_package():
    """Test that the tasks package can be imported."""
    
    print("\n📦 Testing Tasks Package")
    print("-" * 30)
    
    try:
        import tasks
        print("✅ tasks package imported successfully")
        return True
    except Exception as e:
        print(f"❌ Tasks package import error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 VALIDATOR IMPORT TEST")
    print("=" * 50)
    
    imports_ok = test_grader_imports()
    package_ok = test_tasks_package()
    
    print("\n📋 Final Results:")
    print("=" * 50)
    print(f"✅ Grader imports: {'PASS' if imports_ok else 'FAIL'}")
    print(f"✅ Tasks package: {'PASS' if package_ok else 'FAIL'}")
    
    if imports_ok and package_ok:
        print("\n🎉 ALL IMPORTS WORKING - VALIDATOR WILL DETECT ALL GRADERS!")
    else:
        print("\n❌ Import issues detected - please review")