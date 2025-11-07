"""
Enhanced timeline generator with async support.
"""

from typing import Dict, Any, Optional
from .base_generator import BaseGenerator
from ..timeline import HiringTimelineGenerator
from ..core.cache import cached


class EnhancedTimelineGenerator(BaseGenerator):
    """Enhanced timeline generator with caching and async support."""

    def __init__(self):
        super().__init__()
        self.legacy_generator = HiringTimelineGenerator()

    @cached(ttl=3600)
    def generate(self, job_description: Dict[str, Any], hiring_plan: Dict[str, Any],
                start_date: Optional[str] = None) -> Dict[str, Any]:
        """Generate timeline with caching."""
        self._log_start("timeline")
        result = self.legacy_generator.generate(job_description, hiring_plan, start_date)
        self._log_complete("timeline")
        return result
