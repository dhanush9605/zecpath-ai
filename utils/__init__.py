"""Utilities module for Zecpath AI.

Provides cross-cutting utilities including application logging, configuration
helpers, and security sanitization.
"""

from utils.logger import get_logger, setup_logger

__all__ = ["get_logger", "setup_logger"]
