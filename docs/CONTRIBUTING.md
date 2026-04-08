# PolicyMind AI - Contributing Guide

## Welcome to PolicyMind AI!

Thank you for your interest in contributing to PolicyMind AI, a real-world OpenEnv environment for insurance claim processing and policy analysis. This guide will help you get started with contributing to the project.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Contributing Types](#contributing-types)
3. [Development Workflow](#development-workflow)
4. [Code Standards](#code-standards)
5. [Testing Requirements](#testing-requirements)
6. [Documentation](#documentation)
7. [Submitting Changes](#submitting-changes)
8. [Community Guidelines](#community-guidelines)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of OpenEnv environments
- Experience with insurance concepts (helpful but not required)

### Quick Setup

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/saipraveen-k/PolicyMind-AI.git
   cd policymind-ai
   ```

2. **Set Up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your HF_TOKEN
   ```

3. **Verify Setup**
   ```bash
   # Run tests
   pytest
   
   # Check code formatting
   black --check .
   
   # Validate environment
   python -c "import environment.env; print('Setup successful!')"
   ```

## Contributing Types

### 1. Bug Fixes

Help us fix bugs and improve stability:

- **Small fixes**: Typos, formatting, minor logic errors
- **Medium fixes**: Functionality issues, edge cases, error handling
- **Large fixes**: Architectural problems, performance issues

#### Bug Fix Process
1. Check existing issues for the bug
2. Create new issue with detailed description
3. Fork and create fix branch
4. Write tests that reproduce the bug
5. Implement the fix
6. Ensure all tests pass
7. Submit pull request

### 2. Feature Development

Add new capabilities to the environment:

#### Feature Categories
- **New document types**: Medical reports, damage assessments
- **New actions**: Validation, clarification, analysis
- **New policy rules**: Additional insurance domains
- **New difficulty levels**: Expert, custom scenarios
- **Enhanced graders**: Improved evaluation metrics
- **Performance improvements**: Memory, speed optimizations

#### Feature Proposal Process
1. Check roadmap and existing issues
2. Create feature proposal issue
3. Discuss with maintainers
4. Get approval before implementation
5. Follow development workflow

### 3. Documentation

Improve project documentation:

#### Documentation Types
- **User guides**: Tutorials, examples, walkthroughs
- **API documentation**: Method descriptions, examples
- **Development guides**: Architecture, contribution guidelines
- **README improvements**: Installation, usage, deployment
- **Code comments**: Complex logic, important decisions

#### Documentation Standards
- Use clear, concise language
- Include code examples
- Update for new features
- Follow markdown formatting
- Include diagrams where helpful

### 4. Testing and Quality

Improve test coverage and code quality:

#### Testing Contributions
- **Unit tests**: Individual components and functions
- **Integration tests**: Component interactions
- **Performance tests**: Memory, timing constraints
- **Edge case tests**: Error conditions, boundary values
- **Regression tests**: Prevent future breakage

#### Quality Improvements
- **Code coverage**: Increase test coverage
- **Type hints**: Add static type annotations
- **Error handling**: Improve exception handling
- **Performance**: Optimize critical paths
- **Security**: Identify and fix vulnerabilities

## Development Workflow

### 1. Branch Strategy

```bash
# Main branches
main          # Stable, production-ready code
develop       # Integration branch for features

# Feature branches
feature/new-action-types
feature/medical-documents
bugfix/memory-leak
hotfix/critical-issue

# Release branches
release/v1.1.0
```

### 2. Development Steps

```bash
# 1. Sync with latest main
git checkout main
git pull upstream main

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Make changes
# ... implement your feature ...

# 4. Run development checks
pytest
black .
flake8 .
mypy environment/

# 5. Commit changes
git add .
git commit -m "feat: add new feature description"

# 6. Push to your fork
git push origin feature/your-feature-name

# 7. Create pull request
```

### 3. Commit Message Standards

Use conventional commit format:

```bash
# Features
feat: add medical document type support
feat: implement validation action type

# Bug fixes
fix: resolve memory leak in document loading
fix: correct reward calculation for medium tasks

# Documentation
docs: update API documentation for new actions
docs: add troubleshooting guide

# Testing
test: add integration tests for new features
test: improve coverage for environment methods

# Performance
perf: optimize rule matching algorithm
perf: reduce memory usage for large documents

# Refactoring
refactor: simplify action validation logic
refactor: improve code organization in models

# Build/CI
ci: add automated testing for new features
build: update Docker configuration
```

## Code Standards

### 1. Code Style

Follow PEP 8 and project-specific standards:

```python
# Import organization
import asyncio
import json
import os
from typing import Dict, List, Any, Optional

import pydantic
from openai import OpenAI

from environment.models import (
    Observation, Action, Reward,
    ExtractedField, MatchedRule
)

# Class definitions
class PolicyMindEnvironment:
    """
    Main environment class for insurance claim processing.
    
    This class simulates real-world insurance claim processing by
    presenting agents with authentic documents and policy rules.
    
    Attributes:
        task_difficulty: Current difficulty level
        max_steps: Maximum steps per episode
        
    Example:
        >>> env = PolicyMindEnvironment(task_difficulty="medium")
        >>> observation = await env.reset()
    """
    
    def __init__(self, task_difficulty: str = "medium", max_steps: int = 10):
        """Initialize environment with specified parameters."""
        
    async def reset(self, task_difficulty: Optional[str] = None) -> Observation:
        """
        Reset environment for new episode.
        
        Args:
            task_difficulty: Optional difficulty override
            
        Returns:
            Initial observation
            
        Raises:
            ValueError: If difficulty is not supported
        """
        pass
```

### 2. Type Hints

Use comprehensive type hints:

```python
from typing import Dict, List, Any, Optional, Tuple, Union

def extract_fields(
    self, 
    field_names: List[str],
    confidence_threshold: float = 0.8
) -> List[ExtractedField]:
    """Extract specified fields with confidence filtering."""
    pass

async def process_action(
    self, 
    action: Action
) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
    """Process agent action and return results."""
    pass
```

### 3. Error Handling

Implement robust error handling:

```python
class PolicyMindError(Exception):
    """Base exception for PolicyMind environment errors."""
    pass

class InvalidActionError(PolicyMindError):
    """Raised when an invalid action is provided."""
    pass

class DocumentNotFoundError(PolicyMindError):
    """Raised when a requested document cannot be found."""
    pass

# Usage in methods
async def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict]:
    try:
        self._validate_action(action)
        return await self._execute_action(action)
    except ValidationError as e:
        raise InvalidActionError(f"Action validation failed: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during step: {e}")
        return self._create_safe_fallback()
```

### 4. Documentation Standards

```python
def calculate_reward(
    self, 
    action: Action, 
    observation: Observation
) -> Reward:
    """
    Calculate reward for the given action and observation.
    
    This method implements a multi-component reward system that provides
    incremental feedback based on action quality and task progress.
    
    Args:
        action: The action that was executed
        observation: The resulting observation
        
    Returns:
        Reward object containing total reward, component breakdown,
        and any applied penalties or bonuses
        
    Raises:
        InvalidActionError: If the action type is not supported
        CalculationError: If reward calculation fails
        
    Example:
        >>> env = PolicyMindEnvironment()
        >>> action = Action(action_type=ActionType.EXTRACT, extraction_fields=["claim_id"])
        >>> reward = env.calculate_reward(action, observation)
        >>> print(f"Total reward: {reward.total_reward}")
    """
    pass
```

## Testing Requirements

### 1. Test Coverage

Maintain high test coverage:

- **Unit tests**: 90%+ coverage for core logic
- **Integration tests**: All major workflows
- **Edge cases**: Error conditions, boundary values
- **Performance tests**: Memory and timing constraints

### 2. Test Structure

```python
# tests/unit/test_environment.py
import pytest
from environment.env import PolicyMindEnvironment
from environment.models import Action, ActionType

class TestPolicyMindEnvironment:
    """Test suite for PolicyMindEnvironment class."""
    
    @pytest.fixture
    def env(self):
        """Create test environment fixture."""
        return PolicyMindEnvironment(task_difficulty="easy", max_steps=3)
    
    @pytest.mark.asyncio
    async def test_reset_functionality(self, env):
        """Test environment reset functionality."""
        observation = await env.reset()
        
        assert observation.step == 0
        assert observation.max_steps == 3
        assert observation.task_type == "easy"
        assert len(observation.document_text) > 0
    
    @pytest.mark.asyncio
    async def test_extract_action(self, env):
        """Test field extraction action."""
        observation = await env.reset()
        
        action = Action(
            action_type=ActionType.EXTRACT,
            extraction_fields=["claim_id", "policy_number"]
        )
        
        new_observation, reward, done, info = await env.step(action)
        
        assert reward.step_reward >= 0
        assert len(new_observation.extracted_fields) >= len(observation.extracted_fields)
        assert new_observation.step == 1
    
    def test_invalid_action_handling(self, env):
        """Test handling of invalid actions."""
        with pytest.raises(InvalidActionError):
            # This should raise an error
            pass
```

### 3. Test Data Management

```python
# tests/fixtures/test_data.py
import json
from pathlib import Path

class TestDataManager:
    """Manage test data fixtures."""
    
    @staticmethod
    def load_sample_document(doc_id: str):
        """Load sample document for testing."""
        fixtures_path = Path(__file__).parent / "fixtures"
        with open(fixtures_path / f"{doc_id}.json", "r") as f:
            return json.load(f)
    
    @staticmethod
    def create_test_observation():
        """Create test observation object."""
        from environment.models import Observation, DocumentType
        return Observation(
            step=1,
            max_steps=5,
            document_type=DocumentType.INSURANCE_CLAIM,
            document_text="Test document content",
            policy_rules=["Test rule 1", "Test rule 2"],
            task_type="easy"
        )
```

### 4. Performance Testing

```python
# tests/performance/test_memory_usage.py
import pytest
import psutil
import asyncio
from environment.env import PolicyMindEnvironment

class TestMemoryUsage:
    """Test memory usage constraints."""
    
    @pytest.mark.asyncio
    async def test_memory_below_limit(self):
        """Test memory usage stays under 8GB limit."""
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Run multiple episodes
        for episode in range(10):
            env = PolicyMindEnvironment(task_difficulty="medium")
            observation = await env.reset()
            
            # Simulate episode
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
        
        assert memory_increase < 100, f"Memory increased by {memory_increase:.2f}MB"
```

### 5. Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=environment --cov=tasks --cov-report=html

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/performance/

# Run with markers
pytest -m "not performance"  # Skip slow performance tests
pytest -m "unit"            # Only unit tests
pytest -m "integration"      # Only integration tests

# Run specific test file
pytest tests/unit/test_environment.py

# Run with verbose output
pytest -v

# Run with specific Python version
python3.9 -m pytest
```

## Documentation

### 1. Code Documentation

- **Docstrings**: All public methods and classes
- **Type hints**: All function parameters and return values
- **Comments**: Complex logic and important decisions
- **Examples**: Usage examples in docstrings

### 2. User Documentation

- **README.md**: Project overview, installation, usage
- **USER_GUIDE.md**: Comprehensive user instructions
- **API_DOCUMENTATION.md**: Complete API reference
- **TROUBLESHOOTING.md**: Common issues and solutions

### 3. Developer Documentation

- **DEVELOPMENT_GUIDE.md**: Architecture and development
- **CONTRIBUTING.md**: Contribution guidelines (this file)
- **CHANGELOG.md**: Version history and changes
- **ARCHITECTURE.md**: High-level architecture overview

### 4. Documentation Standards

```markdown
# Heading Level 1

## Heading Level 2

### Heading Level 3

- **Bold text** for emphasis
- `Code` for inline code
- [Links](url) for references
- ```python
  # Code blocks with syntax highlighting
  def example():
      pass
  ```

> **Note**: Important information
> 
> **Warning**: Critical warnings

| Column 1 | Column 2 |
|----------|----------|
| Cell 1   | Cell 2   |
```

## Submitting Changes

### 1. Pull Request Process

1. **Create Pull Request**
   - Use descriptive title
   - Provide detailed description
   - Link to relevant issues
   - Add appropriate labels

2. **PR Description Template**
   ```markdown
   ## Description
   Brief description of changes made
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation
   - [ ] Performance improvement
   - [ ] Other
   
   ## Testing
   - [ ] All tests pass
   - [ ] New tests added
   - [ ] Manual testing completed
   
   ## Checklist
   - [ ] Code follows project standards
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No breaking changes
   - [ ] Performance impact considered
   
   ## Issues
   Closes #123
   Related to #456
   ```

3. **Review Process**
   - Automated checks must pass
   - At least one maintainer review required
   - Address all review comments
   - Update based on feedback

### 2. Release Process

1. **Preparation**
   - Update version numbers
   - Update CHANGELOG.md
   - Ensure all tests pass
   - Update documentation

2. **Release**
   - Create release branch
   - Tag with version number
   - Create GitHub release
   - Update documentation

3. **Post-Release**
   - Monitor for issues
   - Address any problems
   - Plan next release

## Community Guidelines

### 1. Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Assume good intentions
- Follow professional standards

### 2. Communication

- **GitHub Issues**: Bug reports, feature requests, questions
- **Discussions**: General questions, ideas, collaboration
- **Pull Requests**: Code changes, reviews, feedback

### 3. Getting Help

1. **Check Documentation**: Review existing docs first
2. **Search Issues**: Look for similar problems
3. **Create Issue**: Provide detailed information
4. **Join Discussion**: Ask questions in discussions

### 4. Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- Project documentation
- Community highlights

## Development Resources

### 1. Useful Tools

- **IDE**: VS Code, PyCharm with Python plugins
- **Testing**: pytest, coverage.py
- **Code Quality**: black, flake8, mypy
- **Documentation**: mkdocs, sphinx
- **CI/CD**: GitHub Actions

### 2. Learning Resources

- [OpenEnv Documentation](https://openenv.ai)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io)
- [AsyncIO Documentation](https://docs.python.org/3/library/asyncio.html)
- [Testing Best Practices](https://docs.pytest.org)

### 3. Project Templates

```python
# New action type template
class NewActionType(str, Enum):
    EXTRACT = "extract"
    MATCH_RULES = "match_rules"
    MAKE_DECISION = "make_decision"
    QUERY = "query"
    NEW_ACTION = "new_action"  # Add new type

# New task grader template
class NewTaskGrader:
    """Grader for new task type."""
    
    def __init__(self):
        self.required_score = 0.7
        
    def evaluate_episode(self, environment, episode_history):
        """Evaluate completed episode."""
        # Implementation here
        pass
    
    def grade_episode(self, environment, episode_history):
        """Generate comprehensive evaluation."""
        # Implementation here
        pass
```

## Questions?

If you have questions about contributing:

1. **Check this guide** first
2. **Search existing issues** and discussions
3. **Create a new issue** with your question
4. **Join the discussion** for general questions

Thank you for contributing to PolicyMind AI! Your contributions help make this project better for everyone.
