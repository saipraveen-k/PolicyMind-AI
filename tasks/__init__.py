"""
PolicyMind AI Tasks Package

This package contains the task graders for evaluating agent performance
across different difficulty levels in the PolicyMind AI environment.

Modules:
    task_easy: Grader for document information extraction tasks
    task_medium: Grader for policy rule matching tasks
    task_hard: Grader for decision making with justification tasks
"""

from tasks.task_easy import EasyTaskGrader
from tasks.task_medium import MediumTaskGrader
from tasks.task_hard import HardTaskGrader

__all__ = [
    "EasyTaskGrader",
    "MediumTaskGrader",
    "HardTaskGrader",
]

__version__ = "1.0.0"