# PolicyMind AI - API Documentation

## Overview

PolicyMind AI provides a comprehensive OpenEnv environment for insurance claim processing and policy analysis. This documentation covers all API interfaces, data models, and usage patterns.

## Core Components

### Environment Class: `PolicyMindEnvironment`

The main environment class that orchestrates the insurance claim processing simulation.

#### Constructor

```python
PolicyMindEnvironment(task_difficulty: str = "medium", max_steps: int = 10)
```

**Parameters:**
- `task_difficulty`: `"easy"`, `"medium"`, or `"hard"`
- `max_steps`: Maximum number of steps per episode (default: 10)

#### Methods

##### `async reset(task_difficulty: Optional[str] = None) -> Observation`

Resets the environment for a new episode.

**Parameters:**
- `task_difficulty`: Optional override for task difficulty

**Returns:** `Observation` object with initial state

**Example:**
```python
env = PolicyMindEnvironment(task_difficulty="medium")
observation = await env.reset()
print(f"Document type: {observation.document_type}")
print(f"Available rules: {len(observation.policy_rules)}")
```

##### `async step(action: Action) -> Tuple[Observation, Reward, bool, Dict]`

Executes one step in the environment.

**Parameters:**
- `action`: `Action` object to execute

**Returns:** Tuple of `(observation, reward, done, info)`

**Example:**
```python
action = Action(
    action_type=ActionType.EXTRACT,
    extraction_fields=["claim_id", "policy_number"]
)
observation, reward, done, info = await env.step(action)
print(f"Step reward: {reward.step_reward:.3f}")
print(f"Episode done: {done}")
```

##### `async state() -> EnvironmentState`

Returns the current complete environment state.

**Returns:** `EnvironmentState` object

**Example:**
```python
state = await env.state()
print(f"Action count: {state.action_count}")
print(f"Episode complete: {state.episode_complete}")
```

## Data Models

### Action Models

#### `ActionType` (Enum)

```python
class ActionType(str, Enum):
    EXTRACT = "extract"
    MATCH_RULES = "match_rules"
    MAKE_DECISION = "make_decision"
    QUERY = "query"
```

#### `Action`

```python
class Action(BaseModel):
    action_type: ActionType
    query: Optional[str] = None
    extraction_fields: Optional[List[str]] = None
    decision_data: Optional[Dict[str, Any]] = None
    rule_keywords: Optional[List[str]] = None
```

**Action Examples:**

```python
# Extract action
Action(
    action_type=ActionType.EXTRACT,
    extraction_fields=["claim_id", "incident_date", "estimated_cost"]
)

# Match rules action
Action(
    action_type=ActionType.MATCH_RULES,
    rule_keywords=["collision", "coverage", "damage"]
)

# Decision action
Action(
    action_type=ActionType.MAKE_DECISION,
    decision_data={
        "decision": "Approved",
        "confidence": 0.85,
        "justification": "Claim meets all coverage requirements...",
        "applied_rules": ["collision_coverage", "police_report_required"]
    }
)

# Query action
Action(
    action_type=ActionType.QUERY,
    query="Analyze all extracted information and determine claim status"
)
```

### Observation Models

#### `Observation`

```python
class Observation(BaseModel):
    step: int
    max_steps: int
    document_type: DocumentType
    document_text: str
    policy_rules: List[str]
    task_type: str
    extracted_fields: List[ExtractedField]
    matched_rules: List[MatchedRule]
    current_decision: Optional[Decision]
    memory: Dict[str, Any]
    hints: List[str]
    error_message: Optional[str]
```

#### `ExtractedField`

```python
class ExtractedField(BaseModel):
    field_name: str
    value: Union[str, int, float, bool]
    confidence: float
    source_text: str
```

#### `MatchedRule`

```python
class MatchedRule(BaseModel):
    rule_id: str
    rule_text: str
    relevance_score: float
    matched_clauses: List[str]
```

#### `Decision`

```python
class Decision(BaseModel):
    decision: str
    confidence: float
    justification: str
    applied_rules: List[str]
```

### Reward Models

#### `Reward`

```python
class Reward(BaseModel):
    total_reward: float
    step_reward: float
    component_rewards: Dict[str, float]
    penalties: List[str]
    bonuses: List[str]
```

## Task-Specific APIs

### Easy Task: Document Extraction

**Objective:** Extract structured fields from documents

**Expected Fields:**
```python
expected_fields = [
    "claim_id", "policy_number", "incident_date", "insured_name",
    "estimated_cost", "police_report_filed", "injuries_reported"
]
```

**Example Usage:**
```python
# Extract basic information
action = Action(
    action_type=ActionType.EXTRACT,
    extraction_fields=["claim_id", "policy_number", "incident_date"]
)
observation, reward, done, info = await env.step(action)

# Check extracted fields
for field in observation.extracted_fields:
    print(f"{field.field_name}: {field.value} (confidence: {field.confidence})")
```

### Medium Task: Rule Matching

**Objective:** Match relevant policy rules to document content

**Available Rules:**
- `collision_coverage`: Coverage for collision damage
- `police_report_required`: Documentation requirements
- `sudden_accidental_damage`: Damage type criteria
- `water_damage_coverage`: Water damage policies
- `maintenance_required`: Maintenance conditions
- `no_fault_claim`: Fault determination

**Example Usage:**
```python
# Match coverage rules
action = Action(
    action_type=ActionType.MATCH_RULES,
    rule_keywords=["collision", "coverage", "damage"]
)
observation, reward, done, info = await env.step(action)

# Review matched rules
for rule in observation.matched_rules:
    print(f"Rule: {rule.rule_id} (relevance: {rule.relevance_score})")
```

### Hard Task: Decision Making

**Objective:** Make final decisions with confidence and justification

**Decision Options:**
- `"Approved"`: Claim accepted for payment
- `"Rejected"`: Claim denied
- `"Needs Review"`: Requires human review

**Example Usage:**
```python
# Make final decision
action = Action(
    action_type=ActionType.MAKE_DECISION,
    decision_data={
        "decision": "Approved",
        "confidence": 0.85,
        "justification": "Claim is approved because the incident meets collision coverage requirements. The police report confirms the other party was at fault, and the estimated cost is within policy limits.",
        "applied_rules": ["collision_coverage", "police_report_required", "no_fault_claim"]
    }
)
observation, reward, done, info = await env.step(action)

# Review decision
if observation.current_decision:
    decision = observation.current_decision
    print(f"Decision: {decision.decision}")
    print(f"Confidence: {decision.confidence}")
    print(f"Justification: {decision.justification}")
```

## Error Handling

### Common Errors

#### Environment Errors

```python
try:
    observation = await env.reset()
except Exception as e:
    print(f"Environment reset failed: {e}")
    # Handle error appropriately
```

#### Action Execution Errors

```python
try:
    observation, reward, done, info = await env.step(action)
except ValueError as e:
    print(f"Invalid action: {e}")
    # Use fallback action
    fallback_action = Action(action_type=ActionType.QUERY, query="Continue processing")
    observation, reward, done, info = await env.step(fallback_action)
except Exception as e:
    print(f"Step execution failed: {e}")
    # Handle critical error
```

#### API Validation Errors

```python
# Validate action before execution
def validate_action(action: Action) -> bool:
    if action.action_type == ActionType.EXTRACT:
        return action.extraction_fields is not None
    elif action.action_type == ActionType.MATCH_RULES:
        return action.rule_keywords is not None
    elif action.action_type == ActionType.MAKE_DECISION:
        return action.decision_data is not None
    return True

# Usage
if validate_action(action):
    observation, reward, done, info = await env.step(action)
else:
    print("Invalid action structure")
```

## Performance Considerations

### Memory Usage

- **Environment**: ~50MB base memory
- **Documents**: ~10MB per document
- **Rules**: ~5MB for rule database
- **Total**: < 100MB typical usage

### Execution Time

- **Reset**: ~100ms
- **Step Execution**: ~200-500ms (depends on action complexity)
- **Full Episode**: ~2-5 seconds

### Optimization Tips

```python
# Batch extractions when possible
action = Action(
    action_type=ActionType.EXTRACT,
    extraction_fields=["claim_id", "policy_number", "incident_date", "estimated_cost"]
)

# Use specific rule keywords
action = Action(
    action_type=ActionType.MATCH_RULES,
    rule_keywords=["collision", "coverage"]  # More specific than just "damage"
)

# Make decisions only when sufficient information is available
if len(observation.extracted_fields) >= 3 and len(observation.matched_rules) >= 2:
    # Ready for decision
    decision_action = Action(action_type=ActionType.MAKE_DECISION, ...)
```

## Integration Examples

### Basic Agent Loop

```python
async def run_basic_agent():
    env = PolicyMindEnvironment(task_difficulty="medium", max_steps=8)
    observation = await env.reset()
    
    total_reward = 0
    done = False
    step_count = 0
    
    while not done and step_count < 8:
        step_count += 1
        
        # Simple strategy based on current state
        if step_count <= 2:
            # Extract information first
            action = Action(
                action_type=ActionType.EXTRACT,
                extraction_fields=["claim_id", "incident_date", "estimated_cost"]
            )
        elif step_count <= 4:
            # Match rules
            action = Action(
                action_type=ActionType.MATCH_RULES,
                rule_keywords=["collision", "coverage", "police"]
            )
        else:
            # Make decision
            action = Action(
                action_type=ActionType.MAKE_DECISION,
                decision_data={
                    "decision": "Approved",
                    "confidence": 0.8,
                    "justification": "Based on extracted information and matched rules",
                    "applied_rules": ["collision_coverage"]
                }
            )
        
        observation, reward, done, info = await env.step(action)
        total_reward += reward.step_reward
        
        print(f"Step {step_count}: Reward = {reward.step_reward:.3f}")
    
    print(f"Episode completed. Total reward: {total_reward:.3f}")
    return total_reward
```

### Advanced Agent with Memory

```python
class AdvancedAgent:
    def __init__(self):
        self.memory = {}
        self.strategy_phase = "extraction"
    
    async def run_episode(self, env):
        observation = await env.reset()
        total_reward = 0
        done = False
        step_count = 0
        
        while not done and step_count < env.max_steps:
            step_count += 1
            
            # Determine action based on current state and memory
            action = await self._determine_action(observation, step_count)
            
            observation, reward, done, info = await env.step(action)
            total_reward += reward.step_reward
            
            # Update memory
            await self._update_memory(observation, action, reward)
            
            print(f"Step {step_count}: {action.action_type.value} -> Reward: {reward.step_reward:.3f}")
        
        return total_reward
    
    async def _determine_action(self, observation, step_count):
        # Extract phase
        if len(observation.extracted_fields) < 4:
            return Action(
                action_type=ActionType.EXTRACT,
                extraction_fields=["claim_id", "policy_number", "incident_date", "estimated_cost"]
            )
        
        # Rule matching phase
        elif len(observation.matched_rules) < 3:
            return Action(
                action_type=ActionType.MATCH_RULES,
                rule_keywords=["collision", "coverage", "police", "damage"]
            )
        
        # Decision phase
        else:
            return Action(
                action_type=ActionType.MAKE_DECISION,
                decision_data={
                    "decision": "Approved",
                    "confidence": 0.85,
                    "justification": "Comprehensive analysis shows claim meets all requirements",
                    "applied_rules": [r.rule_id for r in observation.matched_rules[:3]]
                }
            )
    
    async def _update_memory(self, observation, action, reward):
        self.memory[f"step_{len(self.memory)+1}"] = {
            "action": action.dict(),
            "reward": reward.step_reward,
            "extracted_count": len(observation.extracted_fields),
            "matched_count": len(observation.matched_rules)
        }
```

## Testing and Validation

### Unit Test Example

```python
import pytest
from environment.env import PolicyMindEnvironment
from environment.models import Action, ActionType

@pytest.mark.asyncio
async def test_environment_reset():
    env = PolicyMindEnvironment(task_difficulty="easy")
    observation = await env.reset()
    
    assert observation.step == 0
    assert observation.max_steps == 5
    assert observation.task_type == "easy"
    assert len(observation.document_text) > 0
    assert len(observation.policy_rules) > 0

@pytest.mark.asyncio
async def test_extract_action():
    env = PolicyMindEnvironment(task_difficulty="easy")
    observation = await env.reset()
    
    action = Action(
        action_type=ActionType.EXTRACT,
        extraction_fields=["claim_id", "policy_number"]
    )
    
    new_observation, reward, done, info = await env.step(action)
    
    assert reward.step_reward >= 0
    assert len(new_observation.extracted_fields) >= len(observation.extracted_fields)
    assert new_observation.step == 1

@pytest.mark.asyncio
async def test_full_episode():
    env = PolicyMindEnvironment(task_difficulty="easy", max_steps=3)
    observation = await env.reset()
    
    total_reward = 0
    done = False
    
    # Extract action
    action = Action(
        action_type=ActionType.EXTRACT,
        extraction_fields=["claim_id", "policy_number"]
    )
    observation, reward, done, info = await env.step(action)
    total_reward += reward.step_reward
    
    # Decision action
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

This API documentation provides comprehensive coverage of all PolicyMind AI interfaces, making it easy for developers to integrate and extend the environment.
