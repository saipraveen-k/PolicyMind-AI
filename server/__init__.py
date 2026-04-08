"""
PolicyMind AI Server Package

This package contains the FastAPI server implementation for the PolicyMind AI
OpenEnv environment, providing HTTP endpoints for environment interaction.
"""

from server.app import app

__all__ = ["app"]
__version__ = "1.0.0"
