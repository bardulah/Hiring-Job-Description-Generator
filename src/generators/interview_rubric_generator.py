"""
Enhanced interview rubric generator with async support.
"""

from typing import Dict, Any
from .base_generator import BaseGenerator
from ..interview_rubric import InterviewRubricGenerator
from ..core.cache import cached


class EnhancedInterviewRubricGenerator(BaseGenerator):
    """Enhanced interview rubric generator with caching and async support."""

    def __init__(self):
        super().__init__()
        self.legacy_generator = InterviewRubricGenerator()

    @cached(ttl=3600)
    def generate(self, job_description: Dict[str, Any], hiring_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate interview rubric with caching."""
        self._log_start("interview rubric")
        result = self.legacy_generator.generate(job_description, hiring_config)
        self._log_complete("interview rubric")
        return result
