#!/usr/bin/env python3
"""
Test script to verify inference.py produces exact OpenEnv format.
"""

import subprocess
import sys
import os

def test_inference_format():
    """Test that inference.py produces exact OpenEnv format."""
    
    print("Testing inference.py format...")
    
    # Run inference with test environment
    env_vars = {
        "API_BASE_URL": "https://router.huggingface.co/v1",
        "MODEL_NAME": "mistralai/Mistral-7B-Instruct-v0.2",
        "HF_TOKEN": "",
        "TASK_DIFFICULTY": "medium",
        "MAX_STEPS": "3"
    }
    
    # Set environment and run
    for key, value in env_vars.items():
        os.environ[key] = value
    
    try:
        result = subprocess.run(
            [sys.executable, "inference.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout
        error = result.stderr
        
        print("=== INFERENCE OUTPUT ===")
        print("STDOUT:")
        print(output)
        
        if error:
            print("STDERR:")
            print(error)
        
        # Check for exact format compliance
        lines = output.strip().split('\n')
        
        start_found = any("[START]" in line for line in lines)
        step_format_ok = True
        end_found = False
        
        for line in lines:
            if "[STEP]" in line:
                # Check step format: [STEP] step=<n> action=<string> reward=<0.00> done=<true|false> error=<msg|null>
                parts = line.split()
                if len(parts) >= 4:
                    step_part = parts[0].strip()
                    action_part = parts[1].strip()
                    reward_part = parts[2].strip()
                    done_part = parts[3].strip()
                    
                    # Check exact format
                    if (step_part.startswith("[STEP] step=") and 
                        action_part.startswith("action=") and
                        reward_part.startswith("reward=") and
                        done_part.startswith("done=")):
                        
                        # Check reward format (2 decimal places)
                        try:
                            reward_val = float(reward_part.split("=")[1])
                            if abs(reward_val - round(reward_val, 2)) < 0.001:
                                print(f"❌ Reward format error: {reward_part}")
                                step_format_ok = False
                        except:
                            print(f"❌ Reward parse error: {reward_part}")
                            step_format_ok = False
                        
                        # Check done format (lowercase true/false)
                        done_val = done_part.split("=")[1].strip().lower()
                        if done_val not in ["true", "false"]:
                            print(f"❌ Done format error: {done_part}")
                            step_format_ok = False
                    else:
                        print(f"❌ Step format error: {line}")
                        step_format_ok = False
            elif "[END]" in line:
                end_found = True
                # Check end format: [END] success=<true|false> steps=<n> rewards=<r1,r2,...>
                if "success=" in line and "steps=" in line and "rewards=" in line:
                    success_part = line.split("success=")[1].split()[0]
                    steps_part = line.split("steps=")[1].split()[0]
                    rewards_part = line.split("rewards=")[1]
                    
                    # Check success format (lowercase true/false)
                    if success_part.strip().lower() not in ["true", "false"]:
                        print(f"❌ End success format error: {success_part}")
                    else:
                        print(f"✅ End format OK: success={success_part}")
                
                # Check for no extra output
                if line.strip() and not line.startswith("[") and line.strip() != "":
                    print(f"❌ Extra output: {line}")
        
        print(f"\n=== FORMAT CHECK RESULTS ===")
        print(f"✅ START line found: {start_found}")
        print(f"✅ STEP format OK: {step_format_ok}")
        print(f"✅ END line found: {end_found}")
        
        overall_ok = start_found and step_format_ok and end_found
        print(f"✅ Overall format compliance: {overall_ok}")
        
        return overall_ok
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    test_inference_format()
