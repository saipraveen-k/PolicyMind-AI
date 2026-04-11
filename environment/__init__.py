"""
PolicyMind AI Environment Package

This package contains the core environment implementation for the PolicyMind AI
OpenEnv environment, including the main environment class and Pydantic data models.

Modules:
    env: Main PolicyMindEnvironment class implementing the OpenEnv interface
    models: Pydantic models for Observation, Action, Reward, and EnvironmentState
"""

from environment.models import (
    Action,
    Observation,
    Reward,
    EnvironmentState,
    DocumentSample,
    MatchedRule,
    Decision,
)
from environment.env import PolicyMindEnvironment

__all__ = [
    "PolicyMindEnvironment",
    "Action",
    "Observation",
    "Reward",
    "EnvironmentState",
    "DocumentSample",
    "MatchedRule",
    "Decision",
]

__version__ = "1.0.0"