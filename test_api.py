import sys
import time
import requests

BASE_URL = "https://saipraveen-k-policymind-ai.hf.space"

def test_api():
    print("TESTING /reset")
    try:
        # Initial request might take longer if space is waking up
        res = requests.post(f"{BASE_URL}/reset", json={}, timeout=120)
        print(f"Reset Status: {res.status_code}")
        data = res.json()
        print(f"Reset Keys: {list(data.keys())}")
    except Exception as e:
        print(f"Reset failed: {e}")
        return

    rewards = []
    print("\nTESTING /step")
    for i in range(6):
        try:
            res = requests.post(f"{BASE_URL}/step", json={"action": {"message": "continue"}}, timeout=30)
            print(f"Step {i+1} Status: {res.status_code}")
            data = res.json()
            # Extract step_reward assuming data.get("reward") is dict
            reward_data = data.get("reward", {})
            r = reward_data.get("step_reward", data.get("reward"))
            d = data.get("done")
            print(f"Step {i+1} Reward: {r}, Done: {d}")
            rewards.append(r)
            if d:
                break
        except Exception as e:
            print(f"Step {i+1} failed: {e}")
            
    print("\nREWARDS:", rewards)

if __name__ == "__main__":
    test_api()
