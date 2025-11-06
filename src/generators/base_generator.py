"""
Base generator class with common functionality.
"""

import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any
from ..core.logging_config import get_logger
from ..core.cache import cached

logger = get_logger(__name__)


class BaseGenerator(ABC):
    """Base class for all generators."""

    def __init__(self):
        self.logger = logger

    @abstractmethod
    def generate(self, *args, **kwargs) -> Dict[str, Any]:
        """Synchronous generation method. Must be implemented by subclasses."""
        pass

    async def generate_async(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Asynchronous generation method.
        Default implementation runs sync method in executor.
        Subclasses can override for true async implementation.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.generate(*args, **kwargs))

    def _log_start(self, name: str):
        """Log generation start."""
        self.logger.info(f"Starting {name} generation")

    def _log_complete(self, name: str):
        """Log generation complete."""
        self.logger.info(f"Completed {name} generation")
