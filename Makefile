# PolicyMind AI - Makefile for Common Tasks
# ==========================================

.PHONY: help install dev clean test lint format type-check validate docker-build docker-run docs

# Default target
help:
	@echo "PolicyMind AI - Available Commands"
	@echo "==================================="
	@echo ""
	@echo "Installation:"
	@echo "  install       - Install production dependencies"
	@echo "  dev           - Install development dependencies"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  test          - Run tests with coverage"
	@echo "  lint          - Run linters (flake8, isort)"
	@echo "  format        - Format code with Black"
	@echo "  type-check    - Run type checking with mypy"
	@echo "  validate      - Validate OpenEnv configuration"
	@echo "  check-all     - Run all quality checks"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build  - Build Docker image"
	@echo "  docker-run    - Run Docker container"
	@echo "  docker-clean  - Remove Docker artifacts"
	@echo ""
	@echo "Documentation:"
	@echo "  docs          - Build documentation"
	@echo "  docs-clean    - Clean documentation build"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean         - Remove build artifacts and cache"
	@echo ""

# Python interpreter
PYTHON ?= python3
PIP ?= pip

# Installation
install:
	@echo "Installing production dependencies..."
	$(PIP) install -r requirements.txt

dev: install
	@echo "Installing development dependencies..."
	$(PIP) install pre-commit pytest pytest-cov black flake8 mypy isort

# Testing
test:
	@echo "Running tests..."
	$(PYTHON) -m pytest --cov=environment --cov=tasks --cov-report=html --cov-report=term

test-verbose:
	$(PYTHON) -m pytest -v --tb=short

# Code quality
lint:
	@echo "Running linters..."
	$(PYTHON) -m flake8 environment/ tasks/ inference.py --max-line-length=88 --extend-ignore=E203,W503
	$(PYTHON) -m isort --check-only environment/ tasks/ inference.py

format:
	@echo "Formatting code..."
	$(PYTHON) -m black environment/ tasks/ inference.py --line-length=88
	$(PYTHON) -m isort environment/ tasks/ inference.py --profile black

type-check:
	@echo "Running type checker..."
	$(PYTHON) -m mypy environment/ tasks/ --ignore-missing-imports

validate:
	@echo "Validating OpenEnv configuration..."
	@if command -v openenv >/dev/null 2>&1; then \
		openenv validate; \
	else \
		echo "OpenEnv CLI not installed. Skipping validation."; \
	fi

check-all: lint format type-check validate
	@echo "All checks passed!"

# Docker
docker-build:
	@echo "Building Docker image..."
	docker build -t policymind-ai .

docker-run:
	@echo "Running Docker container..."
	docker run -it -e HF_TOKEN=$(HF_TOKEN) policymind-ai

docker-clean:
	@echo "Cleaning Docker artifacts..."
	docker rmi policymind-ai 2>/dev/null || true

# Documentation
docs:
	@echo "Building documentation..."
	@if [ -d "docs/source" ]; then \
		cd docs && $(PYTHON) -m sphinx -b html source build; \
	else \
		echo "Sphinx documentation not configured. Using docs/ directly."; \
	fi

docs-clean:
	@echo "Cleaning documentation build..."
	rm -rf docs/build/

# Cleanup
clean:
	@echo "Cleaning project..."
	# Python artifacts
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	# Build artifacts
	rm -rf build/ dist/ .eggs/
	rm -rf .pytest_cache/ .mypy_cache/
	rm -rf htmlcov/ .coverage
	rm -rf docs/build/
	# Virtual environments
	rm -rf venv/ .venv/ ENV/
	# IDE
	rm -rf .idea/ .vscode/
	@echo "Cleanup complete!"

# Pre-commit hooks
pre-commit-install:
	@echo "Installing pre-commit hooks..."
	$(PYTHON) -m pre_commit install

pre-commit-run:
	@echo "Running pre-commit hooks..."
	$(PYTHON) -m pre_commit run --all-files

# Quick validation for CI
ci-check:
	$(PYTHON) -c "from environment.env import PolicyMindEnvironment; print('Environment import: OK')"
	$(PYTHON) -c "from environment.models import Observation, Action, Reward; print('Models import: OK')"
	$(PYTHON) -c "from tasks.task_easy import EasyTaskGrader; print('Task graders import: OK')"
	@echo "CI checks passed!"

# Run inference
run:
	@echo "Running inference..."
	$(PYTHON) inference.py

# Security scan
security:
	@echo "Running security scan..."
	@if command -v bandit >/dev/null 2>&1; then \
		bandit -r environment/ tasks/ -ll; \
	else \
		echo "Bandit not installed. Install with: pip install bandit"; \
	fi

# Show coverage
coverage:
	$(PYTHON) -m coverage report -m
	$(PYTHON) -m coverage html
	@echo "Coverage report generated in htmlcov/"

# Version info
version:
	@echo "PolicyMind AI v1.0.0"
	@echo "Python: $$(python --version 2>&1)"
	@echo "Pip: $$(pip --version 2>&1)"