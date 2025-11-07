"""
Enhanced hiring plan generator with async support.
"""

from typing import Dict, Any
from .base_generator import BaseGenerator
from ..hiring_plan import HiringPlanGenerator
from ..core.cache import cached


class EnhancedHiringPlanGenerator(BaseGenerator):
    """Enhanced hiring plan generator with caching and async support."""

    def __init__(self):
        super().__init__()
        self.legacy_generator = HiringPlanGenerator()

    @cached(ttl=3600)
    def generate(self, job_description: Dict[str, Any], hiring_goals: Dict[str, Any]) -> Dict[str, Any]:
        """Generate hiring plan with caching."""
        self._log_start("hiring plan")
        result = self.legacy_generator.generate(job_description, hiring_goals)
        self._log_complete("hiring plan")
        return result
