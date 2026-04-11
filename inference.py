#!/usr/bin/env python3
"""
PolicyMind AI Inference Script - OpenEnv Hackathon Compliance
Uses OpenAI client to run environment step-by-step with EXACT logging format.
"""

import os
import sys

from openai import OpenAI

# Add environment to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from environment.env import PolicyMindEnvironment
from environment.models import Action

def main():
    """
    Main inference function following exact sample script behavior.
    """
    # Read environment variables
    api_base_url = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
    model_name = os.getenv("MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.2")
    hf_token = os.getenv("HF_TOKEN", "")
    task_difficulty = os.getenv("TASK_DIFFICULTY", "medium")
    max_steps = int(os.getenv("MAX_STEPS", "10"))

    # Use default HF_TOKEN if missing (prevent crash)
    if not hf_token:
        hf_token = ""

    # Initialize OpenAI client
    client = OpenAI(
        api_key=hf_token,
        base_url=api_base_url
    )

    # Environment name
    env_name = "policymind-ai"

    # Print exact START format
    print(f"[START] task={task_difficulty} env={env_name} model={model_name}")

    # Initialize environment
    env = PolicyMindEnvironment(task_difficulty=task_difficulty, max_steps=max_steps)

    # Reset environment
    try:
        import asyncio
        observation = asyncio.run(env.reset())
    except Exception:
        print("[END] success=false steps=0 rewards=")
        return 0.01

    rewards = []
    step_count = 0
    success = False

    try:
        # Main interaction loop
        for step in range(1, max_steps + 1):
            step_count = step

            # Generate action using OpenAI
            message = "continue"

            try:
                # Prepare context for the AI
                doc_preview = observation.document_text[:500] + "..." if len(observation.document_text) > 500 else observation.document_text
                extracted_fields = [f.field_name for f in observation.extracted_fields]
                matched_rules = [r.rule_id for r in observation.matched_rules]

                context = f"""Task Difficulty: {task_difficulty}
Current Step: {observation.step}/{observation.max_steps}
Document Type: {observation.document_type}

Document Content:
{doc_preview}

Available Policy Rules:
{chr(10).join(f"- {rule}" for rule in observation.policy_rules[:5])}

Already Extracted Fields: {extracted_fields}
Already Matched Rules: {matched_rules}

What action should you take next? Respond with a clear, actionable message."""

                # Call OpenAI API
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are an AI assistant specialized in insurance claim processing and policy analysis. Respond with clear, concise text describing what action you want to take."},
                        {"role": "user", "content": context}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )

                if response and response.choices and len(response.choices) > 0:
                    message = response.choices[0].message.content.strip()

            except Exception:
                # API failed
                message = "continue"
            
            # Remove any newlines or quotes that might break log formatting
            message = message.replace('\n', ' ').replace('\r', ' ').replace('"', '').replace("'", "")

            # Execute action
            try:
                import asyncio
                observation, reward, done, info = asyncio.run(env.step(Action(message=message)))
                step_reward = float(reward.step_reward)
                rewards.append(step_reward)
                step_error = None

                # Log step with exact format
                error_str = "null" if step_error is None else f'"{step_error}"'
                print(
                    f"[STEP] step={step} action={message} reward={step_reward:.2f} "
                    f"done={str(done).lower()} error={error_str}"
                )

                if done:
                    success = True
                    break

            except Exception as e:
                # Environment step failed
                step_error = str(e).replace('\n', ' ').replace('\r', ' ').replace('"', '').replace("'", "")
                if not step_error:
                    step_error = "unknown error"
                rewards.append(0.0)

                # Log step with error
                error_str = f'"{step_error}"'
                print(
                    f"[STEP] step={step} action=continue reward=0.00 "
                    f"done=false error={error_str}"
                )
                break

    except Exception:
        pass  # Silent error handling

    # Format rewards list
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])

    # Print exact END format
    print(f"[END] success={str(success).lower()} steps={step_count} rewards={rewards_str}")

    return 0.01

if __name__ == "__main__":
    main()
