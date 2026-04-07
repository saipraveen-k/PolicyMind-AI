#!/usr/bin/env python3
"""
Baseline inference script for PolicyMind AI OpenEnv Environment.
Uses OpenAI client to run the environment step-by-step with exact logging format.
"""

import asyncio
import json
import os
import sys
from typing import Dict, List, Any, Optional

import openai
from openai import OpenAI

# Add environment to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from environment.env import PolicyMindEnvironment
from environment.models import Action, ActionType


class PolicyMindInference:
    """
    Baseline inference agent for PolicyMind AI environment.
    Uses OpenAI API to make intelligent decisions.
    """
    
    def __init__(self):
        # Read environment variables
        self.api_base_url = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
        self.model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
        self.hf_token = os.getenv("HF_TOKEN", "")
        
        # Initialize OpenAI client
        self.client = OpenAI(
            api_key=self.hf_token if self.hf_token else os.getenv("OPENAI_API_KEY"),
            base_url=self.api_base_url
        )
        
        # System prompt for the agent
        self.system_prompt = """You are an AI assistant specialized in insurance claim processing and policy analysis. Your task is to:

1. Extract key information from insurance/policy documents
2. Match relevant policy rules to the document content
3. Make informed decisions with proper justification

You will interact with an environment that provides document content and policy rules. You must respond with valid JSON actions containing:
- action_type: one of "extract", "match_rules", "make_decision", "query"
- extraction_fields: list of fields to extract (for extract action)
- rule_keywords: list of keywords for rule matching (for match_rules action)
- decision_data: dictionary with decision, confidence, justification (for make_decision action)
- query: text query (for query action)

Be thorough, accurate, and provide clear reasoning for your decisions. Focus on real-world insurance processing scenarios."""
    
    async def run_inference(self, task_difficulty: str = "medium", max_steps: int = 10) -> float:
        """
        Run inference on the PolicyMind environment.
        
        Args:
            task_difficulty: Difficulty level (easy, medium, hard)
            max_steps: Maximum number of steps
            
        Returns:
            Final score normalized to [0,1]
        """
        print("[START]")
        
        # Initialize environment
        env = PolicyMindEnvironment(task_difficulty=task_difficulty, max_steps=max_steps)
        
        # Reset environment
        observation = await env.reset()
        
        total_reward = 0.0
        step_count = 0
        success = False
        
        try:
            # Main interaction loop
            for step in range(1, max_steps + 1):
                step_count = step
                
                # Generate action using OpenAI
                action = await self._generate_action(observation, task_difficulty)
                
                # Execute action
                observation, reward, done, info = await env.step(action)
                total_reward += reward.step_reward
                
                # Log step with exact format
                action_str = json.dumps(action.dict(), separators=(',', ':'))
                print(f"[STEP] step={step} action=\"{action_str}\" reward={reward.step_reward:.3f} done={done}")
                
                if done:
                    success = True
                    break
        
        except Exception as e:
            print(f"Error during inference: {e}")
            success = False
        
        # Calculate final score
        final_score = max(0.0, min(1.0, total_reward))
        
        print(f"[END] success={success} steps={step_count} score={final_score:.3f}")
        
        return final_score
    
    async def _generate_action(self, observation, task_difficulty: str) -> Action:
        """
        Generate an action using OpenAI based on current observation.
        
        Args:
            observation: Current environment observation
            task_difficulty: Current task difficulty
            
        Returns:
            Action object
        """
        # Prepare context for the AI
        context = self._prepare_context(observation, task_difficulty)
        
        # Generate response from OpenAI
        response = await self._call_openai(context)
        
        # Parse response into Action
        action = self._parse_action(response)
        
        return action
    
    def _prepare_context(self, observation, task_difficulty: str) -> str:
        """
        Prepare context for OpenAI API call.
        
        Args:
            observation: Current observation
            task_difficulty: Task difficulty level
            
        Returns:
            Formatted context string
        """
        # Extract key information
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

Hints:
{chr(10).join(f"- {hint}" for hint in observation.hints)}

Task: Based on the current state, determine the best action to take. Respond with a JSON object containing the action details."""
        
        return context
    
    async def _call_openai(self, context: str) -> str:
        """
        Call OpenAI API to get action recommendation.
        
        Args:
            context: Context for the API call
            
        Returns:
            API response text
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": context}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"OpenAI API call failed: {e}")
            # Fallback to simple action
            return '{"action_type": "query", "query": "Continue processing"}'
    
    def _parse_action(self, response: str) -> Action:
        """
        Parse OpenAI response into Action object.
        
        Args:
            response: OpenAI API response
            
        Returns:
            Action object
        """
        try:
            # Try to parse JSON from response
            if response.startswith("```json"):
                response = response[7:-3]  # Remove markdown code blocks
            elif response.startswith("```"):
                response = response[3:-3]
            
            action_data = json.loads(response)
            
            # Validate and create action
            action_type = ActionType(action_data.get("action_type", "query"))
            
            return Action(
                action_type=action_type,
                query=action_data.get("query"),
                extraction_fields=action_data.get("extraction_fields"),
                decision_data=action_data.get("decision_data"),
                rule_keywords=action_data.get("rule_keywords")
            )
        
        except Exception as e:
            print(f"Failed to parse action: {e}")
            # Fallback to query action
            return Action(
                action_type=ActionType.QUERY,
                query="Continue processing the document"
            )


async def main():
    """
    Main function to run inference.
    """
    # Get task difficulty from environment or use default
    task_difficulty = os.getenv("TASK_DIFFICULTY", "medium")
    max_steps = int(os.getenv("MAX_STEPS", "10"))
    
    print(f"Starting PolicyMind AI inference with task difficulty: {task_difficulty}")
    
    # Create inference agent
    agent = PolicyMindInference()
    
    # Run inference
    final_score = await agent.run_inference(
        task_difficulty=task_difficulty,
        max_steps=max_steps
    )
    
    print(f"Inference completed with final score: {final_score:.3f}")
    
    return final_score


if __name__ == "__main__":
    # Run the inference
    asyncio.run(main())
