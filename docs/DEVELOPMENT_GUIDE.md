# PolicyMind AI - Development Guide

## Overview

This development guide provides comprehensive information for developers who want to extend, modify, or contribute to the PolicyMind AI OpenEnv environment. It covers architecture, coding standards, testing procedures, and contribution guidelines.

## Table of Contents

1. [Architecture](#architecture)
2. [Development Setup](#development-setup)
3. [Code Structure](#code-structure)
4. [Adding New Features](#adding-new-features)
5. [Testing](#testing)
6. [Code Quality](#code-quality)
7. [Performance Optimization](#performance-optimization)
8. [Deployment](#deployment)
9. [Contributing](#contributing)

## Architecture

### High-Level Architecture

```
PolicyMind AI Environment
    |
    |-- Core Environment (env.py)
    |   |-- Document Management
    |   |-- State Management
    |   |-- Step Execution
    |   |-- Reward Calculation
    |
    |-- Data Models (models.py)
    |   |-- Pydantic Models
    |   |-- Type Definitions
    |   |-- Validation Logic
    |
    |-- Task Evaluators (tasks/)
    |   |-- Easy Task Grader
    |   |-- Medium Task Grader
    |   |-- Hard Task Grader
    |
    |-- Inference Engine (inference.py)
    |   |-- OpenAI Integration
    |   |-- Action Generation
    |   |-- Logging Compliance
    |
    |-- Configuration (openenv.yaml)
    |   |-- Environment Spec
    |   |-- Task Definitions
    |   |-- Validation Rules
```

### Core Components

#### Environment Engine (`environment/env.py`)

The main environment class that orchestrates the entire simulation:

```python
class PolicyMindEnvironment:
    """
    Main environment class for insurance claim processing simulation.
    
    Key Responsibilities:
    - Document and rule management
    - State transitions and episode control
    - Action execution and validation
    - Reward calculation and feedback
    """
    
    def __init__(self, task_difficulty: str = "medium", max_steps: int = 10):
        # Initialize with difficulty-specific settings
        # Load documents and policy rules
        # Set up state tracking
        
    async def reset(self, task_difficulty: Optional[str] = None) -> Observation:
        # Reset environment state
        # Select appropriate document
        # Initialize observation
        
    async def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict]:
        # Validate and execute action
        # Update environment state
        # Calculate rewards
        # Check episode completion
        
    async def state(self) -> EnvironmentState:
        # Return complete environment state
```

#### Data Models (`environment/models.py`)

Pydantic models provide type safety and validation:

```python
# Core Models
class Observation(BaseModel):
    """Environment observation returned to agent"""
    
class Action(BaseModel):
    """Agent action with validation"""
    
class Reward(BaseModel):
    """Reward structure with component breakdown"""

# Supporting Models
class ExtractedField(BaseModel):
    """Field extraction result with confidence"""
    
class MatchedRule(BaseModel):
    """Policy rule matching result"""
    
class Decision(BaseModel):
    """Final decision with justification"""
```

#### Task Evaluators (`tasks/`)

Deterministic graders for each difficulty level:

```python
class EasyTaskGrader:
    """Evaluates document extraction accuracy"""
    
    def evaluate_extraction(self, ground_truth, extracted_fields):
        # Calculate accuracy, completeness, precision
        
    def grade_episode(self, environment, episode_history):
        # Generate comprehensive evaluation

class MediumTaskGrader:
    """Evaluates rule matching quality"""
    
    def evaluate_rule_matching(self, ground_truth_rules, matched_rules):
        # Calculate precision, recall, F1 score
        
class HardTaskGrader:
    """Evaluates decision making quality"""
    
    def evaluate_decision(self, ground_truth, decision):
        # Evaluate correctness, confidence, justification
```

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Docker (for containerized development)
- IDE with Python support (VS Code, PyCharm, etc.)

### Local Development Setup

1. **Clone the Repository**
```bash
git clone <repository-url>
cd policymind-ai
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Development Dependencies**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available
```

4. **Set Up Environment Variables**
```bash
# Create .env file
cat > .env << EOF
HF_TOKEN=your-huggingface-token
API_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-3.5-turbo
EOF

# Load environment variables
source .env  # On Windows: set /a .env
```

5. **Verify Setup**
```bash
python -c "import environment.env; print('Environment import successful')"
python -c "import environment.models; print('Models import successful')"
python inference.py --help  # Should show usage
```

### Docker Development Setup

1. **Build Development Image**
```bash
docker build -t policymind-ai:dev .
```

2. **Run Development Container**
```bash
docker run -it --rm \
  -v $(pwd):/app \
  -e HF_TOKEN=your-token \
  policymind-ai:dev bash
```

3. **Install Additional Tools**
```bash
pip install black flake8 mypy pytest pytest-cov
```

## Code Structure

### Directory Layout

```
policymind-ai/
|-- environment/
|   |-- __init__.py
|   |-- env.py              # Main environment class
|   |-- models.py           # Pydantic models
|   |-- documents.py        # Document management (if separated)
|   |-- rules.py           # Policy rules (if separated)
|
|-- tasks/
|   |-- __init__.py
|   |-- task_easy.py        # Easy task grader
|   |-- task_medium.py      # Medium task grader
|   |-- task_hard.py        # Hard task grader
|   |-- base_grader.py      # Base grader class (if needed)
|
|-- tests/
|   |-- __init__.py
|   |-- test_environment.py
|   |-- test_models.py
|   |-- test_tasks.py
|   |-- test_inference.py
|   |-- integration/
|   |   |-- test_full_episode.py
|   |   |-- test_openenv_compliance.py
|
|-- docs/
|   |-- API_DOCUMENTATION.md
|   |-- USER_GUIDE.md
|   |-- DEVELOPMENT_GUIDE.md
|   |-- CONTRIBUTING.md
|
|-- scripts/
|   |-- setup_dev.sh
|   |-- run_tests.sh
|   -- validate_openenv.py
|
|-- inference.py            # Main inference script
|-- openenv.yaml           # OpenEnv configuration
|-- Dockerfile            # Docker configuration
|-- requirements.txt       # Production dependencies
|-- requirements-dev.txt   # Development dependencies
|-- README.md             # Project documentation
|-- .env.example          # Environment variables template
|-- .gitignore           # Git ignore rules
```

### Import Structure

```python
# Standard imports at top
import asyncio
import json
import os
from typing import Dict, List, Any, Optional, Tuple

# Third-party imports
import pydantic
from openai import OpenAI

# Local imports
from environment.models import (
    Observation, Action, Reward, 
    ExtractedField, MatchedRule, Decision
)
from environment.env import PolicyMindEnvironment
```

### Class Organization

```python
class PolicyMindEnvironment:
    """
    Main environment class for insurance claim processing.
    
    This class simulates real-world insurance claim processing by:
    1. Providing realistic document content
    2. Maintaining policy rule database
    3. Evaluating agent actions
    4. Providing structured feedback
    
    Attributes:
        task_difficulty: Current difficulty level
        max_steps: Maximum steps per episode
        current_document: Active document for episode
        current_rules: Applicable policy rules
        state: Current environment state
    """
    
    # Class constants
    DEFAULT_MAX_STEPS = 10
    SUPPORTED_DIFFICULTIES = ["easy", "medium", "hard"]
    
    def __init__(self, task_difficulty: str = "medium", max_steps: int = 10):
        """Initialize environment with specified parameters."""
        
    async def reset(self, task_difficulty: Optional[str] = None) -> Observation:
        """
        Reset environment for new episode.
        
        Args:
            task_difficulty: Optional difficulty override
            
        Returns:
            Initial observation for the episode
            
        Raises:
            ValueError: If task difficulty is not supported
        """
        
    async def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict]:
        """
        Execute one step in the environment.
        
        Args:
            action: Action to execute
            
        Returns:
            Tuple of (observation, reward, done, info)
            
        Raises:
            ValidationError: If action is invalid
            RuntimeError: If environment is not initialized
        """
        
    # Private methods
    def _initialize_documents(self) -> None:
        """Initialize document database."""
        
    def _initialize_policy_rules(self) -> None:
        """Initialize policy rule database."""
        
    def _select_document(self, difficulty: str) -> DocumentSample:
        """Select appropriate document for difficulty level."""
        
    def _execute_action(self, action: Action) -> Tuple[float, Dict, List, List]:
        """Execute action and return reward components."""
```

## Adding New Features

### Adding New Document Types

1. **Extend DocumentType Enum**
```python
# In environment/models.py
class DocumentType(str, Enum):
    INSURANCE_CLAIM = "insurance_claim"
    POLICY_DOCUMENT = "policy_document"
    LEGAL_CONTRACT = "legal_contract"
    MEDICAL_REPORT = "medical_report"  # New type
    DAMAGE_ASSESSMENT = "damage_assessment"  # New type
```

2. **Add Sample Documents**
```python
# In environment/env.py
def _initialize_documents(self):
    # Add new document samples
    self.documents["medical_report_1"] = DocumentSample(
        document_id="medical_report_1",
        document_type=DocumentType.MEDICAL_REPORT,
        title="Medical Examination Report",
        content="...",
        ground_truth={...},
        difficulty="medium"
    )
```

3. **Update Task Logic**
```python
# Update document selection logic
def _select_document(self, difficulty: str) -> DocumentSample:
    if difficulty == "easy":
        doc_options = [doc_id for doc_id, doc in self.documents.items() 
                     if doc.document_type in [DocumentType.POLICY_DOCUMENT]]
    # ... update other difficulty levels
```

### Adding New Action Types

1. **Extend ActionType Enum**
```python
# In environment/models.py
class ActionType(str, Enum):
    EXTRACT = "extract"
    MATCH_RULES = "match_rules"
    MAKE_DECISION = "make_decision"
    QUERY = "query"
    VALIDATE = "validate"  # New action type
    CLARIFY = "clarify"    # New action type
```

2. **Update Action Model**
```python
# In environment/models.py
class Action(BaseModel):
    action_type: ActionType
    query: Optional[str] = None
    extraction_fields: Optional[List[str]] = None
    decision_data: Optional[Dict[str, Any]] = None
    rule_keywords: Optional[List[str]] = None
    validation_target: Optional[str] = None  # For validate action
    clarification_question: Optional[str] = None  # For clarify action
```

3. **Implement Action Logic**
```python
# In environment/env.py
async def _execute_action(self, action: Action) -> Tuple[float, Dict, List, List]:
    if action.action_type == ActionType.VALIDATE:
        return await self._handle_validation(action)
    elif action.action_type == ActionType.CLARIFY:
        return await self._handle_clarification(action)
    # ... existing action handlers

async def _handle_validation(self, action: Action) -> Tuple[float, Dict, List, List]:
    """Handle validation of extracted information."""
    if not action.validation_target:
        return 0.0, {}, ["No validation target specified"], []
    
    # Implement validation logic
    validation_result = self._validate_field(action.validation_target)
    reward = 0.1 if validation_result else 0.0
    
    return reward, {"validation_reward": reward}, [], []

async def _handle_clarification(self, action: Action) -> Tuple[float, Dict, List, List]:
    """Handle clarification requests."""
    if not action.clarification_question:
        return 0.0, {}, ["No clarification question"], []
    
    # Provide clarification based on document content
    clarification = self._provide_clarification(action.clarification_question)
    
    # Store clarification in observation memory
    self.state.observation.memory[f"clarification_{len(self.state.observation.memory)}"] = clarification
    
    return 0.05, {"clarification_reward": 0.05}, [], []
```

### Adding New Policy Rules

1. **Define New Rule**
```python
# In environment/env.py
def _initialize_policy_rules(self):
    # Add new rule
    self.policy_rules.append(PolicyRule(
        rule_id="medical_necessity",
        category="coverage",
        title="Medical Necessity Requirement",
        description="Treatment must be medically necessary and appropriate",
        conditions=[
            "Treatment prescribed by licensed physician",
            "Treatment is standard for diagnosed condition",
            "No experimental or investigational procedures"
        ],
        actions=[
            "Verify medical license of prescribing physician",
            "Check treatment guidelines and standards",
            "Review FDA approval status"
        ],
        priority=2
    ))
```

2. **Update Rule Matching Logic**
```python
# Update rule matching to handle new categories
def _evaluate_rule_matching(self, ground_truth_rules: Set[str], matched_rules: List[MatchedRule]) -> Dict[str, float]:
    # Add medical category to evaluation
    category_scores = []
    
    for category, rule_list in self.rule_categories.items():
        gt_category_rules = set(rule_list) & ground_truth_rules
        pred_category_rules = set(rule_list) & set(r.rule_id for r in matched_rules)
        
        if gt_category_rules:
            coverage = len(gt_category_rules & pred_category_rules) / len(gt_category_rules)
            category_scores.append(coverage)
    
    return sum(category_scores) / len(category_scores) if category_scores else 0
```

### Adding New Difficulty Levels

1. **Update Environment Initialization**
```python
# In environment/env.py
def __init__(self, task_difficulty: str = "medium", max_steps: int = 10):
    if task_difficulty not in self.SUPPORTED_DIFFICULTIES:
        raise ValueError(f"Unsupported difficulty: {task_difficulty}")
    
    # Add new difficulty settings
    self.difficulty_settings = {
        "easy": {"max_steps": 5, "document_types": [DocumentType.POLICY_DOCUMENT]},
        "medium": {"max_steps": 8, "document_types": [DocumentType.INSURANCE_CLAIM]},
        "hard": {"max_steps": 10, "document_types": [DocumentType.INSURANCE_CLAIM]},
        "expert": {"max_steps": 15, "document_types": [DocumentType.INSURANCE_CLAIM, DocumentType.MEDICAL_REPORT]}
    }
```

2. **Create New Task Grader**
```python
# In tasks/task_expert.py
class ExpertTaskGrader:
    """Grader for expert-level tasks requiring multi-document analysis."""
    
    def __init__(self):
        self.required_accuracy = 0.9
        self.required_completeness = 0.85
        
    def evaluate_multi_document_analysis(self, documents, analysis_result):
        """Evaluate analysis across multiple documents."""
        # Implement expert-level evaluation
        pass
    
    def grade_episode(self, environment, episode_history):
        """Grade expert episode with strict criteria."""
        # Implement expert grading logic
        pass
```

## Testing

### Test Structure

```
tests/
|-- unit/
|   |-- test_models.py           # Test Pydantic models
|   |-- test_environment.py      # Test environment methods
|   |-- test_tasks.py           # Test task graders
|
|-- integration/
|   |-- test_full_episode.py    # Test complete episodes
|   |-- test_inference.py       # Test inference script
|   |-- test_openenv_compliance.py  # Test OpenEnv compliance
|
|-- performance/
|   |-- test_memory_usage.py    # Test memory constraints
|   |-- test_execution_time.py  # Test time constraints
|
|-- fixtures/
|   |-- sample_documents.json   # Test document data
|   |-- test_scenarios.json     # Test scenarios
```

### Unit Tests

```python
# tests/unit/test_models.py
import pytest
from pydantic import ValidationError
from environment.models import Action, ActionType, Observation

class TestActionModel:
    """Test Action model validation and behavior."""
    
    def test_valid_extract_action(self):
        """Test valid extract action creation."""
        action = Action(
            action_type=ActionType.EXTRACT,
            extraction_fields=["claim_id", "policy_number"]
        )
        
        assert action.action_type == ActionType.EXTRACT
        assert len(action.extraction_fields) == 2
        assert action.decision_data is None
    
    def test_invalid_extract_action(self):
        """Test extract action without required fields."""
        with pytest.raises(ValidationError):
            Action(action_type=ActionType.EXTRACT)  # Missing extraction_fields
    
    def test_valid_decision_action(self):
        """Test valid decision action creation."""
        decision_data = {
            "decision": "Approved",
            "confidence": 0.85,
            "justification": "Test justification",
            "applied_rules": ["collision_coverage"]
        }
        
        action = Action(
            action_type=ActionType.MAKE_DECISION,
            decision_data=decision_data
        )
        
        assert action.action_type == ActionType.MAKE_DECISION
        assert action.decision_data["decision"] == "Approved"
        assert action.decision_data["confidence"] == 0.85

# tests/unit/test_environment.py
import pytest
from environment.env import PolicyMindEnvironment
from environment.models import Action, ActionType

class TestPolicyMindEnvironment:
    """Test PolicyMindEnvironment class."""
    
    @pytest.mark.asyncio
    async def test_environment_initialization(self):
        """Test environment initialization with different difficulties."""
        env = PolicyMindEnvironment(task_difficulty="easy")
        assert env.task_difficulty == "easy"
        assert env.max_steps == 5
        assert len(env.documents) > 0
        assert len(env.policy_rules) > 0
    
    @pytest.mark.asyncio
    async def test_reset_functionality(self):
        """Test environment reset functionality."""
        env = PolicyMindEnvironment(task_difficulty="medium")
        
        # Reset with default difficulty
        observation = await env.reset()
        
        assert observation.step == 0
        assert observation.max_steps == 8
        assert observation.task_type == "medium"
        assert len(observation.document_text) > 0
        assert len(observation.policy_rules) > 0
    
    @pytest.mark.asyncio
    async def test_step_execution(self):
        """Test single step execution."""
        env = PolicyMindEnvironment(task_difficulty="easy")
        observation = await env.reset()
        
        action = Action(
            action_type=ActionType.EXTRACT,
            extraction_fields=["claim_id"]
        )
        
        new_observation, reward, done, info = await env.step(action)
        
        assert reward.step_reward >= 0
        assert isinstance(done, bool)
        assert isinstance(info, dict)
        assert new_observation.step == 1
    
    @pytest.mark.asyncio
    async def test_episode_completion(self):
        """Test complete episode execution."""
        env = PolicyMindEnvironment(task_difficulty="easy", max_steps=3)
        observation = await env.reset()
        
        total_reward = 0
        done = False
        step_count = 0
        
        while not done and step_count < 3:
            step_count += 1
            
            if step_count <= 2:
                action = Action(
                    action_type=ActionType.EXTRACT,
                    extraction_fields=["claim_id", "policy_number"]
                )
            else:
                action = Action(
                    action_type=ActionType.MAKE_DECISION,
                    decision_data={
                        "decision": "Approved",
                        "confidence": 0.8,
                        "justification": "Test decision",
                        "applied_rules": []
                    }
                )
            
            observation, reward, done, info = await env.step(action)
            total_reward += reward.step_reward
        
        assert done == True
        assert total_reward > 0
```

### Integration Tests

```python
# tests/integration/test_full_episode.py
import pytest
import asyncio
from environment.env import PolicyMindEnvironment
from environment.models import Action, ActionType
from tasks.task_easy import EasyTaskGrader
from tasks.task_medium import MediumTaskGrader
from tasks.task_hard import HardTaskGrader

class TestFullEpisode:
    """Test complete episode execution for all difficulty levels."""
    
    @pytest.mark.asyncio
    async def test_easy_episode_complete(self):
        """Test complete easy task episode."""
        env = PolicyMindEnvironment(task_difficulty="easy", max_steps=5)
        grader = EasyTaskGrader()
        
        observation = await env.reset()
        episode_history = []
        total_reward = 0
        
        # Execute complete episode
        for step in range(1, 6):
            action = Action(
                action_type=ActionType.EXTRACT,
                extraction_fields=["claim_id", "policy_number", "incident_date"]
            )
            
            observation, reward, done, info = await env.step(action)
            total_reward += reward.step_reward
            
            episode_history.append({
                "step": step,
                "action": action.dict(),
                "observation": observation.dict(),
                "reward": reward.step_reward
            })
            
            if done:
                break
        
        # Evaluate episode
        evaluation = grader.grade_episode(env, episode_history)
        
        assert evaluation.passed == True
        assert evaluation.score >= 0.6
        assert len(episode_history) <= 5
    
    @pytest.mark.asyncio
    async def test_medium_episode_complete(self):
        """Test complete medium task episode."""
        env = PolicyMindEnvironment(task_difficulty="medium", max_steps=8)
        grader = MediumTaskGrader()
        
        observation = await env.reset()
        episode_history = []
        
        # Strategy: Extract -> Match Rules -> Decide
        strategy_actions = [
            Action(
                action_type=ActionType.EXTRACT,
                extraction_fields=["claim_id", "incident_date", "estimated_cost"]
            ),
            Action(
                action_type=ActionType.MATCH_RULES,
                rule_keywords=["collision", "coverage"]
            ),
            Action(
                action_type=ActionType.MATCH_RULES,
                rule_keywords=["police", "report"]
            ),
            Action(
                action_type=ActionType.MAKE_DECISION,
                decision_data={
                    "decision": "Approved",
                    "confidence": 0.8,
                    "justification": "Medium task decision",
                    "applied_rules": ["collision_coverage", "police_report_required"]
                }
            )
        ]
        
        for i, action in enumerate(strategy_actions):
            observation, reward, done, info = await env.step(action)
            
            episode_history.append({
                "step": i + 1,
                "action": action.dict(),
                "observation": observation.dict(),
                "reward": reward.step_reward
            })
            
            if done:
                break
        
        # Evaluate episode
        evaluation = grader.grade_episode(env, episode_history)
        
        assert evaluation.passed == True
        assert evaluation.score >= 0.6
        assert len(episode_history) <= 8
```

### Performance Tests

```python
# tests/performance/test_memory_usage.py
import pytest
import psutil
import os
from environment.env import PolicyMindEnvironment

class TestMemoryUsage:
    """Test memory usage constraints."""
    
    @pytest.mark.asyncio
    async def test_memory_usage_below_limit(self):
        """Test that environment stays under memory limits."""
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Run multiple episodes
        for episode in range(10):
            env = PolicyMindEnvironment(task_difficulty="medium")
            observation = await env.reset()
            
            # Simulate episode steps
            for step in range(5):
                from environment.models import Action, ActionType
                action = Action(
                    action_type=ActionType.EXTRACT,
                    extraction_fields=["claim_id"]
                )
                observation, reward, done, info = await env.step(action)
                if done:
                    break
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Should stay under 100MB increase
        assert memory_increase < 100, f"Memory increased by {memory_increase:.2f}MB"
    
    @pytest.mark.asyncio
    async def test_memory_cleanup(self):
        """Test that memory is properly cleaned up after episodes."""
        process = psutil.Process(os.getpid())
        
        for episode in range(5):
            env = PolicyMindEnvironment(task_difficulty="easy")
            observation = await env.reset()
            
            # Environment should be garbage collected
            del env
        
        # Force garbage collection
        import gc
        gc.collect()
        
        # Memory should not continuously grow
        current_memory = process.memory_info().rss / 1024 / 1024
        assert current_memory < 500, f"Memory usage too high: {current_memory:.2f}MB"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=environment --cov=tasks --cov-report=html

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/performance/

# Run with specific markers
pytest -m "not performance"  # Skip performance tests
pytest -m "unit"            # Only unit tests
```

## Code Quality

### Code Formatting

Use Black for consistent code formatting:

```bash
# Format all Python files
black .

# Check formatting without making changes
black --check .

# Format specific files
black environment/env.py tasks/task_easy.py
```

### Linting

Use Flake8 for code linting:

```bash
# Run linting
flake8 .

# Run with specific configuration
flake8 --max-line-length=100 --ignore=E203,W503

# Run on specific files
flake8 environment/env.py
```

### Type Checking

Use MyPy for static type checking:

```bash
# Run type checking
mypy environment/

# Run with strict settings
mypy --strict environment/

# Check specific files
mypy environment/env.py environment/models.py
```

### Code Quality Standards

#### Naming Conventions

```python
# Classes: PascalCase
class PolicyMindEnvironment:
    pass

# Functions and variables: snake_case
def extract_fields_from_document():
    extracted_fields = []
    return extracted_fields

# Constants: UPPER_SNAKE_CASE
DEFAULT_MAX_STEPS = 10
SUPPORTED_DIFFICULTIES = ["easy", "medium", "hard"]

# Private methods: underscore prefix
def _initialize_documents(self):
    pass

def _calculate_reward(self, action):
    pass
```

#### Documentation Standards

```python
class PolicyMindEnvironment:
    """
    Main environment class for insurance claim processing simulation.
    
    This class provides a realistic simulation of insurance claim processing
    by presenting agents with authentic documents and policy rules.
    
    Attributes:
        task_difficulty: Current difficulty level ("easy", "medium", "hard")
        max_steps: Maximum number of steps allowed per episode
        current_document: The active document for the current episode
        current_rules: List of applicable policy rules
        state: Current environment state including observation and metadata
    
    Example:
        >>> env = PolicyMindEnvironment(task_difficulty="medium")
        >>> observation = await env.reset()
        >>> action = Action(action_type=ActionType.EXTRACT, extraction_fields=["claim_id"])
        >>> observation, reward, done, info = await env.step(action)
    """
    
    async def reset(self, task_difficulty: Optional[str] = None) -> Observation:
        """
        Reset the environment for a new episode.
        
        This method initializes a new episode by selecting an appropriate
        document based on the difficulty level and creating the initial
        observation.
        
        Args:
            task_difficulty: Optional difficulty level override. If not provided,
                uses the environment's current difficulty level.
        
        Returns:
            Observation: Initial observation containing the document content,
                available policy rules, and task-specific hints.
        
        Raises:
            ValueError: If the specified task difficulty is not supported.
            RuntimeError: If the environment fails to initialize properly.
        
        Example:
            >>> env = PolicyMindEnvironment()
            >>> obs = await env.reset(task_difficulty="easy")
            >>> print(f"Document type: {obs.document_type}")
        """
        pass
```

#### Error Handling Standards

```python
# Use specific exceptions
class PolicyMindError(Exception):
    """Base exception for PolicyMind environment errors."""
    pass

class InvalidActionError(PolicyMindError):
    """Raised when an invalid action is provided."""
    pass

class DocumentNotFoundError(PolicyMindError):
    """Raised when a requested document cannot be found."""
    pass

# Handle errors gracefully
async def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict]:
    try:
        # Validate action
        self._validate_action(action)
        
        # Execute action
        return await self._execute_action(action)
        
    except ValidationError as e:
        raise InvalidActionError(f"Action validation failed: {e}")
    except Exception as e:
        # Log error and provide safe fallback
        logger.error(f"Unexpected error during step execution: {e}")
        return self._create_safe_fallback()
```

## Performance Optimization

### Memory Optimization

```python
# Use lazy loading for large datasets
class DocumentManager:
    def __init__(self):
        self._documents = None
        self._document_cache = {}
    
    @property
    def documents(self):
        """Lazy load documents when first accessed."""
        if self._documents is None:
            self._documents = self._load_documents()
        return self._documents
    
    def get_document(self, doc_id: str):
        """Get document with caching."""
        if doc_id not in self._document_cache:
            self._document_cache[doc_id] = self.documents[doc_id]
        return self._document_cache[doc_id]

# Use generators for large datasets
def generate_rule_matches(self, keywords: List[str]):
    """Generate rule matches using generator for memory efficiency."""
    for rule in self.policy_rules:
        if any(keyword in rule.description.lower() for keyword in keywords):
            yield self._create_matched_rule(rule, keywords)
```

### Execution Time Optimization

```python
# Cache expensive computations
from functools import lru_cache

class PolicyMindEnvironment:
    @lru_cache(maxsize=128)
    def _calculate_document_similarity(self, doc_id1: str, doc_id2: str):
        """Cache document similarity calculations."""
        # Expensive similarity calculation
        pass
    
    # Use async for concurrent operations
    async def _process_multiple_actions(self, actions: List[Action]):
        """Process multiple actions concurrently."""
        tasks = [self._execute_action(action) for action in actions]
        results = await asyncio.gather(*tasks)
        return results
```

### Database Optimization

```python
# Use efficient data structures
from collections import defaultdict
import bisect

class RuleIndex:
    """Efficient rule indexing for fast lookups."""
    
    def __init__(self, rules: List[PolicyRule]):
        self.keyword_index = defaultdict(list)
        self.category_index = defaultdict(list)
        
        for rule in rules:
            # Index by keywords
            for keyword in self._extract_keywords(rule):
                bisect.insort(self.keyword_index[keyword], rule.priority)
            
            # Index by category
            bisect.insort(self.category_index[rule.category], rule.priority)
    
    def find_rules_by_keywords(self, keywords: List[str]) -> List[PolicyRule]:
        """Find rules efficiently using keyword index."""
        matching_rules = []
        for keyword in keywords:
            if keyword in self.keyword_index:
                matching_rules.extend(self.keyword_index[keyword])
        return matching_rules
```

## Deployment

### Docker Configuration

```dockerfile
# Multi-stage Dockerfile for optimal deployment
FROM python:3.9-slim as base

# Set up environment
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Development stage
FROM base as development
RUN pip install --no-cache-dir pytest black flake8 mypy
COPY requirements.txt requirements-dev.txt ./
RUN pip install -r requirements.txt -r requirements-dev.txt
COPY . .
CMD ["python", "-m", "pytest"]

# Production stage
FROM base as production
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "inference.py"]
```

### Environment Configuration

```python
# config/production.py
import os
from typing import Dict, Any

class ProductionConfig:
    """Production environment configuration."""
    
    # API Configuration
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    HF_TOKEN = os.getenv("HF_TOKEN")
    
    # Environment Configuration
    DEFAULT_TASK_DIFFICULTY = os.getenv("TASK_DIFFICULTY", "medium")
    DEFAULT_MAX_STEPS = int(os.getenv("MAX_STEPS", "10"))
    
    # Performance Configuration
    MAX_MEMORY_MB = int(os.getenv("MAX_MEMORY_MB", "8192"))
    MAX_EXECUTION_TIME = int(os.getenv("MAX_EXECUTION_TIME", "1200"))  # 20 minutes
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def validate(cls) -> Dict[str, Any]:
        """Validate configuration and return status."""
        issues = []
        
        if not cls.HF_TOKEN:
            issues.append("HF_TOKEN is required")
        
        if cls.DEFAULT_MAX_STEPS > 20:
            issues.append("MAX_STEPS should not exceed 20")
        
        if cls.MAX_MEMORY_MB > 16384:
            issues.append("MAX_MEMORY_MB exceeds recommended limit")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
```

### Health Checks

```python
# health_check.py
import asyncio
import os
from environment.env import PolicyMindEnvironment
from environment.models import Action, ActionType

async def health_check() -> Dict[str, Any]:
    """Perform comprehensive health check."""
    
    results = {
        "status": "healthy",
        "checks": {},
        "timestamp": asyncio.get_event_loop().time()
    }
    
    # Check environment variables
    env_vars = {
        "HF_TOKEN": os.getenv("HF_TOKEN"),
        "API_BASE_URL": os.getenv("API_BASE_URL"),
        "MODEL_NAME": os.getenv("MODEL_NAME")
    }
    
    results["checks"]["environment"] = {
        "status": "pass" if all(env_vars.values()) else "fail",
        "details": env_vars
    }
    
    # Check environment import
    try:
        env = PolicyMindEnvironment(task_difficulty="easy", max_steps=3)
        observation = await env.reset()
        
        # Test basic functionality
        action = Action(
            action_type=ActionType.EXTRACT,
            extraction_fields=["claim_id"]
        )
        new_observation, reward, done, info = await env.step(action)
        
        results["checks"]["environment"] = {
            "status": "pass",
            "details": {"reset": True, "step": True, "reward": reward.step_reward > 0}
        }
    except Exception as e:
        results["checks"]["environment"] = {
            "status": "fail",
            "details": {"error": str(e)}
        }
    
    # Check memory usage
    try:
        import psutil
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        
        results["checks"]["memory"] = {
            "status": "pass" if memory_mb < 512 else "warn",
            "details": {"memory_mb": memory_mb}
        }
    except ImportError:
        results["checks"]["memory"] = {
            "status": "skip",
            "details": {"message": "psutil not available"}
        }
    
    # Overall status
    failed_checks = [name for name, check in results["checks"].items() 
                    if check["status"] == "fail"]
    
    if failed_checks:
        results["status"] = "unhealthy"
        results["failed_checks"] = failed_checks
    
    return results

if __name__ == "__main__":
    import json
    result = asyncio.run(health_check())
    print(json.dumps(result, indent=2))
```

## Contributing

### Contribution Guidelines

1. **Code Style**: Follow PEP 8 and project standards
2. **Testing**: All contributions must include tests
3. **Documentation**: Update documentation for new features
4. **Performance**: Ensure changes don't violate memory/time constraints
5. **OpenEnv Compliance**: Maintain OpenEnv specification compliance

### Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch
3. **Implement** changes with tests
4. **Run** full test suite
5. **Update** documentation
6. **Submit** pull request with description

### Development Workflow

```bash
# 1. Set up development environment
git clone <your-fork>
cd policymind-ai
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 2. Create feature branch
git checkout -b feature/new-feature

# 3. Make changes
# ... implement feature ...

# 4. Run tests
pytest --cov=environment --cov=tasks

# 5. Check code quality
black .
flake8 .
mypy environment/

# 6. Commit and push
git add .
git commit -m "Add new feature: description"
git push origin feature/new-feature

# 7. Create pull request
```

This comprehensive development guide provides everything needed to contribute to and extend the PolicyMind AI project while maintaining high code quality and performance standards.
