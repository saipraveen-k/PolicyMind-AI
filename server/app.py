#!/usr/bin/env python3
"""
PolicyMind AI Server App - OpenEnv Compatible Backend
Provides FastAPI endpoints for OpenEnv validation and deployment.
"""

import os
import sys
from typing import Dict, Any, Optional
from fastapi import FastAPI
import uvicorn

# Add environment to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from environment.env import PolicyMindEnvironment
from environment.models import Action

# Initialize FastAPI app
app = FastAPI(title="PolicyMind AI - OpenEnv Server")

# Global environment instance
env_instance: Optional[PolicyMindEnvironment] = None


@app.post("/reset")
async def reset() -> Dict[str, Any]:
    """Reset the environment."""
    global env_instance
    
    try:
        # Create new environment instance with safe defaults
        env_instance = PolicyMindEnvironment(
            task_difficulty="medium",
            max_steps=10
        )
        
        # Reset environment
        observation = await env_instance.reset()
        
        # Return observation as dict (never None)
        obs_dict = observation.model_dump() if observation else {}
        
        return {
            "observation": obs_dict,
            "info": {}
        }
        
    except Exception:
        # Never crash - return empty observation
        return {
            "observation": {},
            "info": {}
        }


@app.post("/step")
async def step(action_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a step in the environment."""
    global env_instance
    
    try:
        if env_instance is None:
            return {
                "observation": {},
                "reward": {"step_reward": 0.0, "total_reward": 0.0},
                "done": False,
                "info": {"error": "Environment not reset. Call /reset first."}
            }
        
        # Create action from request
        action = Action(**action_data)
        
        # Execute step
        observation, reward, done, info = await env_instance.step(action)
        
        return {
            "observation": observation.model_dump() if observation else {},
            "reward": reward.model_dump() if reward else {"step_reward": 0.0, "total_reward": 0.0},
            "done": done,
            "info": info or {}
        }
        
    except Exception:
        # Never crash - return safe response
        return {
            "observation": {},
            "reward": {"step_reward": 0.0, "total_reward": 0.0},
            "done": False,
            "info": {"error": "Step execution failed"}
        }


@app.get("/state")
async def state() -> Dict[str, Any]:
    """Get current environment state."""
    global env_instance
    
    try:
        if env_instance is None:
            return {
                "state": {},
                "info": {"error": "Environment not initialized. Call /reset first."}
            }
        
        # Get current state
        current_state = await env_instance.state()
        
        return {
            "state": current_state.model_dump() if current_state else {},
            "info": {}
        }
        
    except Exception:
        # Never crash - return empty state
        return {
            "state": {},
            "info": {"error": "State retrieval failed"}
        }


@app.get("/")
async def root() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "PolicyMind AI Server is running",
        "endpoints": {
            "reset": "POST /reset",
            "step": "POST /step", 
            "state": "GET /state"
        }
    }


def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
