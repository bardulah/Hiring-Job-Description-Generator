"""
Enhanced job description generator with async support.
"""

from typing import Dict, Any
from .base_generator import BaseGenerator
from ..job_description import JobDescriptionGenerator
from ..core.cache import cached


class EnhancedJobDescriptionGenerator(BaseGenerator):
    """Enhanced job description generator with caching and async support."""

    def __init__(self):
        super().__init__()
        self.legacy_generator = JobDescriptionGenerator()

    @cached(ttl=3600)
    def generate(self, analysis: Dict[str, Any], company_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate job description with caching."""
        self._log_start("job description")
        result = self.legacy_generator.generate(analysis, company_info)
        self._log_complete("job description")
        return result
