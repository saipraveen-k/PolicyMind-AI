"""
Pydantic models for PolicyMind AI OpenEnv Environment.
Defines the core data structures for observations, actions, and rewards.
"""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
from enum import Enum


class ActionType(str, Enum):
    """Types of actions the agent can take."""
    EXTRACT = "extract"
    MATCH_RULES = "match_rules"
    MAKE_DECISION = "make_decision"
    QUERY = "query"


class DocumentType(str, Enum):
    """Types of documents in the environment."""
    INSURANCE_CLAIM = "insurance_claim"
    POLICY_DOCUMENT = "policy_document"
    LEGAL_CONTRACT = "legal_contract"


class ExtractedField(BaseModel):
    """Represents an extracted field from a document."""
    field_name: str = Field(..., description="Name of the extracted field")
    value: Union[str, int, float, bool] = Field(..., description="Extracted value")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    source_text: str = Field(..., description="Original text snippet")


class MatchedRule(BaseModel):
    """Represents a matched policy rule."""
    rule_id: str = Field(..., description="Unique identifier for the rule")
    rule_text: str = Field(..., description="Full text of the rule")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Relevance to the case")
    matched_clauses: List[str] = Field(default_factory=list, description="Specific clauses that matched")


class Decision(BaseModel):
    """Represents a final decision made by the agent."""
    decision: str = Field(..., description="Final decision: Approved/Rejected/Needs Review")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in the decision")
    justification: str = Field(..., description="Detailed justification for the decision")
    applied_rules: List[str] = Field(default_factory=list, description="Rules that influenced the decision")


class Observation(BaseModel):
    """Observation model for the environment."""
    step: int = Field(..., description="Current step number")
    max_steps: int = Field(..., description="Maximum allowed steps")
    document_type: DocumentType = Field(..., description="Type of document being processed")
    document_text: str = Field(..., description="Full text of the document")
    policy_rules: List[str] = Field(default_factory=list, description="Available policy rules")
    task_type: str = Field(..., description="Current task: easy/medium/hard")
    extracted_fields: List[ExtractedField] = Field(default_factory=list, description="Fields extracted so far")
    matched_rules: List[MatchedRule] = Field(default_factory=list, description="Rules matched so far")
    current_decision: Optional[Decision] = Field(None, description="Current decision if made")
    memory: Dict[str, Any] = Field(default_factory=dict, description="Agent's memory across steps")
    hints: List[str] = Field(default_factory=list, description="Hints for the current task")
    error_message: Optional[str] = Field(None, description="Error message if action failed")


class Action(BaseModel):
    """Action model for the environment."""
    action_type: ActionType = Field(..., description="Type of action to perform")
    query: Optional[str] = Field(None, description="Query string for query actions")
    extraction_fields: Optional[List[str]] = Field(None, description="Fields to extract")
    decision_data: Optional[Dict[str, Any]] = Field(None, description="Decision data for decision actions")
    rule_keywords: Optional[List[str]] = Field(None, description="Keywords for rule matching")


class Reward(BaseModel):
    """Reward model for the environment."""
    total_reward: float = Field(..., description="Total reward for the episode")
    step_reward: float = Field(..., description="Reward for current step")
    component_rewards: Dict[str, float] = Field(default_factory=dict, description="Component breakdown")
    penalties: List[str] = Field(default_factory=list, description="Applied penalties")
    bonuses: List[str] = Field(default_factory=list, description="Applied bonuses")


class EnvironmentState(BaseModel):
    """Complete environment state."""
    observation: Observation
    action_count: int = Field(default=0, description="Total actions taken")
    episode_complete: bool = Field(default=False, description="Whether episode is complete")
    final_score: Optional[float] = Field(None, description="Final episode score")


class DocumentSample(BaseModel):
    """Sample document for the environment."""
    document_id: str = Field(..., description="Unique document identifier")
    document_type: DocumentType = Field(..., description="Type of document")
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Document content")
    ground_truth: Dict[str, Any] = Field(..., description="Ground truth for evaluation")
    difficulty: str = Field(..., description="Difficulty level: easy/medium/hard")


class PolicyRule(BaseModel):
    """Policy rule definition."""
    rule_id: str = Field(..., description="Unique rule identifier")
    category: str = Field(..., description="Rule category")
    title: str = Field(..., description="Rule title")
    description: str = Field(..., description="Rule description")
    conditions: List[str] = Field(..., description="Conditions for the rule")
    actions: List[str] = Field(..., description="Actions to take when conditions are met")
    priority: int = Field(default=1, description="Rule priority (higher = more important)")


class EvaluationResult(BaseModel):
    """Result of task evaluation."""
    task_id: str = Field(..., description="Task identifier")
    score: float = Field(..., ge=0.0, le=1.0, description="Task score")
    correctness: float = Field(..., ge=0.0, le=1.0, description="Correctness score")
    completeness: float = Field(..., ge=0.0, le=1.0, description="Completeness score")
    reasoning_quality: float = Field(..., ge=0.0, le=1.0, description="Reasoning quality score")
    feedback: str = Field(..., description="Detailed feedback")
    passed: bool = Field(..., description="Whether the task passed evaluation")
