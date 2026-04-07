# PolicyMind AI - User Guide

## Introduction

PolicyMind AI is a sophisticated OpenEnv environment that simulates real-world insurance claim processing. This guide will help you understand how to use the environment effectively, from basic setup to advanced agent development.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Environment Concepts](#environment-concepts)
3. [Task Walkthroughs](#task-walkthroughs)
4. [Agent Development](#agent-development)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Usage](#advanced-usage)

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Hugging Face token (HF_TOKEN)
- Basic understanding of insurance concepts

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd policymind-ai

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export HF_TOKEN="your-huggingface-token"
```

### Your First Episode

```python
import asyncio
from environment.env import PolicyMindEnvironment
from environment.models import Action, ActionType

async def first_episode():
    # Create environment
    env = PolicyMindEnvironment(task_difficulty="easy", max_steps=5)
    
    # Reset and get initial observation
    observation = await env.reset()
    print(f"Document Type: {observation.document_type}")
    print(f"Hints: {observation.hints}")
    
    # Extract basic information
    action = Action(
        action_type=ActionType.EXTRACT,
        extraction_fields=["claim_id", "policy_number"]
    )
    
    # Execute action
    observation, reward, done, info = await env.step(action)
    print(f"Extracted {len(observation.extracted_fields)} fields")
    print(f"Step reward: {reward.step_reward:.3f}")
    
    return reward.step_reward

# Run your first episode
result = asyncio.run(first_episode())
print(f"First episode reward: {result:.3f}")
```

## Environment Concepts

### Document Types

PolicyMind AI works with three main document types:

1. **Insurance Claims**: Real-world claim reports with incident details
2. **Policy Documents**: Insurance policy terms and conditions
3. **Legal Contracts**: Legal agreements and clauses

### Task Difficulties

#### Easy: Document Extraction
- **Goal**: Extract structured information from documents
- **Focus**: Accuracy and completeness of field extraction
- **Time Limit**: 5 steps
- **Success Criteria**: 60% accuracy, 50% completeness

#### Medium: Rule Matching
- **Goal**: Match document content to relevant policy rules
- **Focus**: Precision and recall in rule identification
- **Time Limit**: 8 steps
- **Success Criteria**: 60% precision, 60% recall

#### Hard: Decision Making
- **Goal**: Make final decisions with confidence and justification
- **Focus**: Decision accuracy and reasoning quality
- **Time Limit**: 10 steps
- **Success Criteria**: 70% decision accuracy, 60% justification quality

### Action Types

#### 1. Extract Action
Extract specific fields from the document.

```python
Action(
    action_type=ActionType.EXTRACT,
    extraction_fields=["claim_id", "incident_date", "estimated_cost"]
)
```

**Common Fields to Extract:**
- `claim_id`: Unique claim identifier
- `policy_number`: Insurance policy number
- `incident_date`: When the incident occurred
- `insured_name`: Name of the insured person
- `estimated_cost`: Claim amount in dollars
- `police_report_filed`: Whether police report exists
- `injuries_reported`: Whether injuries were reported

#### 2. Match Rules Action
Find policy rules relevant to the document content.

```python
Action(
    action_type=ActionType.MATCH_RULES,
    rule_keywords=["collision", "coverage", "damage"]
)
```

**Common Rule Keywords:**
- `collision`, `coverage`, `damage` for physical damage
- `police`, `report`, `documentation` for requirements
- `maintenance`, `conditions`, `requirements` for policy conditions
- `fault`, `liability`, `responsibility` for fault determination

#### 3. Make Decision Action
Make a final decision with confidence and justification.

```python
Action(
    action_type=ActionType.MAKE_DECISION,
    decision_data={
        "decision": "Approved",
        "confidence": 0.85,
        "justification": "Claim meets all coverage requirements...",
        "applied_rules": ["collision_coverage", "police_report_required"]
    }
)
```

**Decision Options:**
- `"Approved"`: Claim accepted for payment
- `"Rejected"`: Claim denied
- `"Needs Review"`: Requires human review

#### 4. Query Action
Ask general questions or request analysis.

```python
Action(
    action_type=ActionType.QUERY,
    query="Analyze all extracted information and determine claim status"
)
```

## Task Walkthroughs

### Easy Task Walkthrough

Let's walk through a complete easy task episode:

```python
async def easy_task_walkthrough():
    env = PolicyMindEnvironment(task_difficulty="easy", max_steps=5)
    observation = await env.reset()
    
    print("=== EASY TASK: Document Extraction ===")
    print(f"Document: {observation.document_type}")
    print(f"Preview: {observation.document_text[:200]}...")
    
    total_reward = 0
    step = 1
    
    # Step 1: Extract identifiers
    print(f"\n--- Step {step} ---")
    action = Action(
        action_type=ActionType.EXTRACT,
        extraction_fields=["claim_id", "policy_number"]
    )
    observation, reward, done, info = await env.step(action)
    total_reward += reward.step_reward
    
    print(f"Action: Extract identifiers")
    print(f"Extracted: {[f.field_name for f in observation.extracted_fields]}")
    print(f"Reward: {reward.step_reward:.3f}")
    
    if done:
        print("Episode completed!")
        return total_reward
    
    # Step 2: Extract dates and amounts
    step += 1
    print(f"\n--- Step {step} ---")
    action = Action(
        action_type=ActionType.EXTRACT,
        extraction_fields=["incident_date", "estimated_cost"]
    )
    observation, reward, done, info = await env.step(action)
    total_reward += reward.step_reward
    
    print(f"Action: Extract dates and amounts")
    print(f"Extracted: {[f.field_name for f in observation.extracted_fields]}")
    print(f"Reward: {reward.step_reward:.3f}")
    
    if done:
        print("Episode completed!")
        return total_reward
    
    # Step 3: Extract additional details
    step += 1
    print(f"\n--- Step {step} ---")
    action = Action(
        action_type=ActionType.EXTRACT,
        extraction_fields=["insured_name", "police_report_filed"]
    )
    observation, reward, done, info = await env.step(action)
    total_reward += reward.step_reward
    
    print(f"Action: Extract additional details")
    print(f"Total extracted: {len(observation.extracted_fields)} fields")
    print(f"Reward: {reward.step_reward:.3f}")
    
    print(f"\n=== TASK COMPLETE ===")
    print(f"Total Reward: {total_reward:.3f}")
    print(f"Episode Done: {done}")
    
    return total_reward

# Run the walkthrough
result = asyncio.run(easy_task_walkthrough())
```

### Medium Task Walkthrough

```python
async def medium_task_walkthrough():
    env = PolicyMindEnvironment(task_difficulty="medium", max_steps=8)
    observation = await env.reset()
    
    print("=== MEDIUM TASK: Rule Matching ===")
    print(f"Document: {observation.document_type}")
    print(f"Available Rules: {len(observation.policy_rules)}")
    
    total_reward = 0
    step = 1
    
    # Step 1: Extract basic information first
    print(f"\n--- Step {step} ---")
    action = Action(
        action_type=ActionType.EXTRACT,
        extraction_fields=["claim_id", "incident_date", "estimated_cost"]
    )
    observation, reward, done, info = await env.step(action)
    total_reward += reward.step_reward
    print(f"Extracted basic info: {reward.step_reward:.3f}")
    
    # Step 2: Match coverage rules
    step += 1
    print(f"\n--- Step {step} ---")
    action = Action(
        action_type=ActionType.MATCH_RULES,
        rule_keywords=["collision", "coverage", "damage"]
    )
    observation, reward, done, info = await env.step(action)
    total_reward += reward.step_reward
    print(f"Matched coverage rules: {reward.step_reward:.3f}")
    print(f"Matched: {[r.rule_id for r in observation.matched_rules]}")
    
    # Step 3: Match documentation rules
    step += 1
    print(f"\n--- Step {step} ---")
    action = Action(
        action_type=ActionType.MATCH_RULES,
        rule_keywords=["police", "report", "documentation"]
    )
    observation, reward, done, info = await env.step(action)
    total_reward += reward.step_reward
    print(f"Matched documentation rules: {reward.step_reward:.3f}")
    
    # Step 4: Make decision
    step += 1
    print(f"\n--- Step {step} ---")
    action = Action(
        action_type=ActionType.MAKE_DECISION,
        decision_data={
            "decision": "Approved",
            "confidence": 0.8,
            "justification": "Based on extracted information and matched rules",
            "applied_rules": [r.rule_id for r in observation.matched_rules[:3]]
        }
    )
    observation, reward, done, info = await env.step(action)
    total_reward += reward.step_reward
    print(f"Final decision: {reward.step_reward:.3f}")
    
    print(f"\n=== TASK COMPLETE ===")
    print(f"Total Reward: {total_reward:.3f}")
    print(f"Final Decision: {observation.current_decision.decision}")
    
    return total_reward
```

### Hard Task Walkthrough

```python
async def hard_task_walkthrough():
    env = PolicyMindEnvironment(task_difficulty="hard", max_steps=10)
    observation = await env.reset()
    
    print("=== HARD TASK: Decision Making ===")
    print(f"Document: {observation.document_type}")
    print(f"Max Steps: {observation.max_steps}")
    
    total_reward = 0
    step = 1
    
    # Strategy: Extract -> Match Rules -> Analyze -> Decide
    
    # Phase 1: Comprehensive extraction
    extraction_fields = ["claim_id", "policy_number", "incident_date", "estimated_cost", 
                        "insured_name", "police_report_filed", "injuries_reported"]
    
    for field_batch in [extraction_fields[:3], extraction_fields[3:6], extraction_fields[6:]]:
        print(f"\n--- Step {step} ---")
        action = Action(
            action_type=ActionType.EXTRACT,
            extraction_fields=field_batch
        )
        observation, reward, done, info = await env.step(action)
        total_reward += reward.step_reward
        print(f"Extracted {len(field_batch)} fields: {reward.step_reward:.3f}")
        step += 1
    
    # Phase 2: Rule matching
    rule_categories = [
        ["collision", "coverage", "damage"],
        ["police", "report", "documentation"],
        ["maintenance", "conditions", "requirements"]
    ]
    
    for keywords in rule_categories:
        print(f"\n--- Step {step} ---")
        action = Action(
            action_type=ActionType.MATCH_RULES,
            rule_keywords=keywords
        )
        observation, reward, done, info = await env.step(action)
        total_reward += reward.step_reward
        print(f"Matched {keywords[0]} rules: {reward.step_reward:.3f}")
        step += 1
    
    # Phase 3: Analysis and decision
    print(f"\n--- Step {step} ---")
    action = Action(
        action_type=ActionType.QUERY,
        query="Analyze all extracted information and matched rules to determine claim status"
    )
    observation, reward, done, info = await env.step(action)
    total_reward += reward.step_reward
    print(f"Analysis query: {reward.step_reward:.3f}")
    step += 1
    
    # Final decision
    print(f"\n--- Step {step} ---")
    action = Action(
        action_type=ActionType.MAKE_DECISION,
        decision_data={
            "decision": "Approved",
            "confidence": 0.85,
            "justification": f"Comprehensive analysis shows claim meets all requirements. "
                           f"Extracted {len(observation.extracted_fields)} fields and "
                           f"matched {len(observation.matched_rules)} relevant rules. "
                           f"All policy conditions satisfied.",
            "applied_rules": [r.rule_id for r in observation.matched_rules]
        }
    )
    observation, reward, done, info = await env.step(action)
    total_reward += reward.step_reward
    print(f"Final decision: {reward.step_reward:.3f}")
    
    print(f"\n=== TASK COMPLETE ===")
    print(f"Total Reward: {total_reward:.3f}")
    print(f"Decision: {observation.current_decision.decision}")
    print(f"Confidence: {observation.current_decision.confidence}")
    
    return total_reward
```

## Agent Development

### Basic Agent Template

```python
class BasicAgent:
    def __init__(self, task_difficulty="medium"):
        self.task_difficulty = task_difficulty
        self.step_count = 0
    
    async def run_episode(self, env):
        observation = await env.reset()
        total_reward = 0
        done = False
        
        while not done and self.step_count < env.max_steps:
            self.step_count += 1
            
            # Determine action based on current state
            action = self.choose_action(observation)
            
            # Execute action
            observation, reward, done, info = await env.step(action)
            total_reward += reward.step_reward
            
            print(f"Step {self.step_count}: {action.action_type.value} -> {reward.step_reward:.3f}")
        
        return total_reward
    
    def choose_action(self, observation):
        # Simple strategy based on task difficulty and current state
        if self.task_difficulty == "easy":
            return self.choose_easy_action(observation)
        elif self.task_difficulty == "medium":
            return self.choose_medium_action(observation)
        else:
            return self.choose_hard_action(observation)
    
    def choose_easy_action(self, observation):
        # Focus on extraction
        if len(observation.extracted_fields) < 4:
            return Action(
                action_type=ActionType.EXTRACT,
                extraction_fields=["claim_id", "policy_number", "incident_date", "estimated_cost"]
            )
        else:
            return Action(
                action_type=ActionType.MAKE_DECISION,
                decision_data={
                    "decision": "Approved",
                    "confidence": 0.7,
                    "justification": "Basic extraction completed",
                    "applied_rules": []
                }
            )
    
    def choose_medium_action(self, observation):
        # Balance extraction and rule matching
        if len(observation.extracted_fields) < 3:
            return Action(
                action_type=ActionType.EXTRACT,
                extraction_fields=["claim_id", "incident_date", "estimated_cost"]
            )
        elif len(observation.matched_rules) < 3:
            return Action(
                action_type=ActionType.MATCH_RULES,
                rule_keywords=["collision", "coverage", "police"]
            )
        else:
            return Action(
                action_type=ActionType.MAKE_DECISION,
                decision_data={
                    "decision": "Approved",
                    "confidence": 0.8,
                    "justification": "Extraction and rule matching completed",
                    "applied_rules": [r.rule_id for r in observation.matched_rules[:3]]
                }
            )
    
    def choose_hard_action(self, observation):
        # Comprehensive approach
        if len(observation.extracted_fields) < 5:
            return Action(
                action_type=ActionType.EXTRACT,
                extraction_fields=["claim_id", "policy_number", "incident_date", "estimated_cost", "police_report_filed"]
            )
        elif len(observation.matched_rules) < 4:
            return Action(
                action_type=ActionType.MATCH_RULES,
                rule_keywords=["collision", "coverage", "police", "maintenance"]
            )
        else:
            return Action(
                action_type=ActionType.MAKE_DECISION,
                decision_data={
                    "decision": "Approved",
                    "confidence": 0.85,
                    "justification": "Comprehensive analysis completed with all relevant information",
                    "applied_rules": [r.rule_id for r in observation.matched_rules]
                }
            )
```

### Advanced Agent with Memory

```python
class AdvancedAgent:
    def __init__(self, task_difficulty="medium"):
        self.task_difficulty = task_difficulty
        self.memory = {
            "extracted_fields": set(),
            "matched_rules": set(),
            "action_history": [],
            "reward_history": []
        }
        self.phase = "extraction"
    
    async def run_episode(self, env):
        observation = await env.reset()
        total_reward = 0
        done = False
        
        while not done:
            action = self.choose_action(observation)
            
            observation, reward, done, info = await env.step(action)
            total_reward += reward.step_reward
            
            # Update memory and strategy
            self.update_memory(observation, action, reward)
            self.update_strategy()
            
            print(f"Phase: {self.phase}, Action: {action.action_type.value}, Reward: {reward.step_reward:.3f}")
        
        return total_reward
    
    def choose_action(self, observation):
        if self.phase == "extraction":
            return self.extraction_action(observation)
        elif self.phase == "rule_matching":
            return self.rule_matching_action(observation)
        elif self.phase == "analysis":
            return self.analysis_action(observation)
        else:
            return self.decision_action(observation)
    
    def extraction_action(self, observation):
        # Extract fields we haven't gotten yet
        all_fields = ["claim_id", "policy_number", "incident_date", "estimated_cost", 
                     "insured_name", "police_report_filed", "injuries_reported"]
        remaining_fields = [f for f in all_fields if f not in self.memory["extracted_fields"]]
        
        if remaining_fields:
            return Action(
                action_type=ActionType.EXTRACT,
                extraction_fields=remaining_fields[:3]  # Extract up to 3 at a time
            )
        else:
            self.phase = "rule_matching"
            return self.rule_matching_action(observation)
    
    def rule_matching_action(self, observation):
        # Try different rule categories
        rule_categories = [
            ["collision", "coverage", "damage"],
            ["police", "report", "documentation"],
            ["maintenance", "conditions", "requirements"],
            ["fault", "liability", "responsibility"]
        ]
        
        for keywords in rule_categories:
            if any(keyword not in " ".join([r.rule_id for r in observation.matched_rules]) 
                   for keyword in keywords):
                return Action(
                    action_type=ActionType.MATCH_RULES,
                    rule_keywords=keywords
                )
        
        self.phase = "analysis"
        return self.analysis_action(observation)
    
    def analysis_action(self, observation):
        self.phase = "decision"
        return Action(
            action_type=ActionType.QUERY,
            query="Synthesize all extracted information and matched rules for final decision"
        )
    
    def decision_action(self, observation):
        # Make decision based on comprehensive analysis
        confidence = self.calculate_confidence(observation)
        decision = self.recommend_decision(observation)
        justification = self.generate_justification(observation)
        
        return Action(
            action_type=ActionType.MAKE_DECISION,
            decision_data={
                "decision": decision,
                "confidence": confidence,
                "justification": justification,
                "applied_rules": [r.rule_id for r in observation.matched_rules]
            }
        )
    
    def calculate_confidence(self, observation):
        # Higher confidence with more extracted fields and matched rules
        field_confidence = min(1.0, len(observation.extracted_fields) / 5.0)
        rule_confidence = min(1.0, len(observation.matched_rules) / 3.0)
        
        return (field_confidence + rule_confidence) / 2.0
    
    def recommend_decision(self, observation):
        # Simple heuristic: approve if we have good coverage match
        coverage_rules = [r for r in observation.matched_rules if "coverage" in r.rule_id]
        police_rules = [r for r in observation.matched_rules if "police" in r.rule_id]
        
        if coverage_rules and police_rules:
            return "Approved"
        elif coverage_rules and not police_rules:
            return "Needs Review"
        else:
            return "Rejected"
    
    def generate_justification(self, observation):
        justification = f"Analysis based on {len(observation.extracted_fields)} extracted fields "
        justification += f"and {len(observation.matched_rules)} matched rules. "
        
        if observation.extracted_fields:
            justification += f"Key information includes claim ID and incident details. "
        
        if observation.matched_rules:
            justification += f"Relevant policy rules identified and applied. "
        
        justification += "Decision follows standard insurance processing guidelines."
        
        return justification
    
    def update_memory(self, observation, action, reward):
        # Update extracted fields
        for field in observation.extracted_fields:
            self.memory["extracted_fields"].add(field.field_name)
        
        # Update matched rules
        for rule in observation.matched_rules:
            self.memory["matched_rules"].add(rule.rule_id)
        
        # Update history
        self.memory["action_history"].append(action.action_type.value)
        self.memory["reward_history"].append(reward.step_reward)
    
    def update_strategy(self):
        # Move to next phase based on progress
        if len(self.memory["extracted_fields"]) >= 5 and self.phase == "extraction":
            self.phase = "rule_matching"
        elif len(self.memory["matched_rules"]) >= 3 and self.phase == "rule_matching":
            self.phase = "analysis"
```

## Best Practices

### 1. Efficient Action Selection

```python
# Good: Batch extractions when possible
Action(
    action_type=ActionType.EXTRACT,
    extraction_fields=["claim_id", "policy_number", "incident_date"]  # Multiple fields
)

# Avoid: Single field extractions
Action(
    action_type=ActionType.EXTRACT,
    extraction_fields=["claim_id"]  # Inefficient
)
```

### 2. Strategic Rule Matching

```python
# Good: Specific, relevant keywords
Action(
    action_type=ActionType.MATCH_RULES,
    rule_keywords=["collision", "coverage", "damage"]
)

# Avoid: Too general keywords
Action(
    action_type=ActionType.MATCH_RULES,
    rule_keywords=["insurance", "policy"]  # Too broad
)
```

### 3. Confidence Calibration

```python
def calculate_confidence(extracted_count, matched_count, max_steps_used):
    """Calculate realistic confidence based on available information"""
    information_score = (extracted_count / 7.0) * 0.6  # 7 is max fields
    rule_score = (matched_count / 6.0) * 0.4  # 6 is max rules
    
    base_confidence = information_score + rule_score
    
    # Penalize if too many steps used
    efficiency_penalty = max(0, (max_steps_used - 5) * 0.05)
    
    return max(0.1, min(0.95, base_confidence - efficiency_penalty))
```

### 4. Error Handling

```python
async def safe_step(env, action):
    """Execute action with error handling"""
    try:
        observation, reward, done, info = await env.step(action)
        return observation, reward, done, info, None
    except Exception as e:
        print(f"Action failed: {e}")
        # Return safe default
        return observation, Reward(step_reward=0.0, total_reward=0.0, 
                                 component_rewards={}, penalties=[], bonuses=[]), False, {}, str(e)
```

## Troubleshooting

### Common Issues

#### 1. Low Rewards on Easy Tasks

**Problem**: Getting low rewards despite extracting fields correctly.

**Solution**: Ensure you're extracting the right fields:
```python
# Check what fields are available in ground truth
print(f"Expected fields: {list(env.current_document.ground_truth.get('extracted_fields', {}).keys())}")

# Extract those specific fields
expected_fields = ["claim_id", "policy_number", "incident_date", "estimated_cost"]
action = Action(action_type=ActionType.EXTRACT, extraction_fields=expected_fields)
```

#### 2. Rule Matching Not Working

**Problem**: No rules being matched or low relevance scores.

**Solution**: Use more specific keywords:
```python
# Instead of general terms
Action(action_type=ActionType.MATCH_RULES, rule_keywords=["damage"])

# Use specific policy terms
Action(action_type=ActionType.MATCH_RULES, rule_keywords=["collision_coverage", "sudden_accidental"])
```

#### 3. Decision Confidence Too Low

**Problem**: Decision confidence scores are consistently low.

**Solution**: Build confidence gradually:
```python
def build_confidence(observation):
    field_confidence = len(observation.extracted_fields) / 7.0  # Normalize
    rule_confidence = len(observation.matched_rules) / 6.0
    
    # Only make decision with sufficient information
    if field_confidence < 0.5 or rule_confidence < 0.5:
        return 0.3  # Low confidence, needs more info
    
    return (field_confidence + rule_confidence) / 2.0
```

#### 4. Episode Not Completing

**Problem**: Episodes not ending with `done=True`.

**Solution**: Ensure proper decision making:
```python
# For hard tasks, decision is required to end episode
if observation.task_type == "hard" and not observation.current_decision:
    # Must make decision to complete
    action = Action(
        action_type=ActionType.MAKE_DECISION,
        decision_data={
            "decision": "Needs Review",
            "confidence": 0.5,
            "justification": "Insufficient information for final decision",
            "applied_rules": []
        }
    )
```

### Debugging Tips

#### 1. Enable Detailed Logging

```python
def debug_observation(observation):
    print(f"=== DEBUG OBSERVATION ===")
    print(f"Step: {observation.step}/{observation.max_steps}")
    print(f"Task: {observation.task_type}")
    print(f"Document Type: {observation.document_type}")
    print(f"Extracted Fields: {len(observation.extracted_fields)}")
    print(f"Matched Rules: {len(observation.matched_rules)}")
    print(f"Hints: {observation.hints}")
    print(f"Memory: {list(observation.memory.keys())}")
    print("=" * 30)
```

#### 2. Track Progress

```python
class ProgressTracker:
    def __init__(self):
        self.steps = []
        self.rewards = []
        self.actions = []
    
    def track_step(self, step, action, reward, observation):
        self.steps.append(step)
        self.rewards.append(reward.step_reward)
        self.actions.append(action.action_type.value)
        
        print(f"Progress: Step {step}, {action.action_type.value}, "
              f"Reward: {reward.step_reward:.3f}, "
              f"Fields: {len(observation.extracted_fields)}, "
              f"Rules: {len(observation.matched_rules)}")
    
    def summary(self):
        total_reward = sum(self.rewards)
        print(f"Episode Summary: {len(self.steps)} steps, "
              f"Total Reward: {total_reward:.3f}, "
              f"Average: {total_reward/len(self.rewards):.3f}")
```

## Advanced Usage

### Custom Evaluation Metrics

```python
def custom_evaluation(observation, reward_history):
    """Create custom evaluation metrics"""
    
    # Efficiency score
    efficiency = len(reward_history) / observation.max_steps
    
    # Information gathering score
    info_score = (len(observation.extracted_fields) / 7.0 + 
                 len(observation.matched_rules) / 6.0) / 2.0
    
    # Consistency score (reward variance)
    if len(reward_history) > 1:
        variance = sum((r - sum(reward_history)/len(reward_history))**2 
                      for r in reward_history) / len(reward_history)
        consistency = max(0, 1.0 - variance)
    else:
        consistency = 1.0
    
    return {
        "efficiency": efficiency,
        "information_gathering": info_score,
        "consistency": consistency,
        "overall": (efficiency + info_score + consistency) / 3.0
    }
```

### Multi-Episode Training

```python
async def run_training_session(num_episodes=10, task_difficulty="medium"):
    """Run multiple episodes to improve performance"""
    
    results = []
    best_score = 0
    best_episode = None
    
    for episode in range(num_episodes):
        print(f"\n=== Episode {episode + 1} ===")
        
        env = PolicyMindEnvironment(task_difficulty=task_difficulty)
        agent = AdvancedAgent(task_difficulty)
        
        score = await agent.run_episode(env)
        results.append(score)
        
        if score > best_score:
            best_score = score
            best_episode = episode + 1
        
        print(f"Episode {episode + 1} completed with score: {score:.3f}")
    
    print(f"\n=== Training Session Complete ===")
    print(f"Average Score: {sum(results)/len(results):.3f}")
    print(f"Best Score: {best_score:.3f} (Episode {best_episode})")
    print(f"Improvement: {results[-1] - results[0]:.3f}")
    
    return results
```

This comprehensive user guide provides everything needed to effectively use PolicyMind AI, from basic setup to advanced agent development strategies.
