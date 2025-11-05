"""
Job Description Analyzer
Analyzes existing job descriptions to extract key insights and patterns.
"""

from typing import Dict, List, Any
import re


class JobDescriptionAnalyzer:
    """Analyzes job descriptions from company materials and external sources."""

    def __init__(self):
        self.common_skills = set()
        self.common_responsibilities = set()
        self.common_qualifications = set()

    def analyze_job_description(self, job_description: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes a single job description and extracts key components.

        Args:
            job_description: Dict containing job description data

        Returns:
            Dict with extracted insights
        """
        insights = {
            'title': job_description.get('title', ''),
            'company': job_description.get('company', ''),
            'skills': self._extract_skills(job_description.get('description', '')),
            'responsibilities': self._extract_responsibilities(job_description.get('description', '')),
            'qualifications': self._extract_qualifications(job_description.get('description', '')),
            'experience_level': self._extract_experience_level(job_description.get('description', '')),
            'salary_range': job_description.get('salary_range', None),
            'location': job_description.get('location', ''),
            'remote_policy': self._extract_remote_policy(job_description.get('description', ''))
        }

        return insights

    def analyze_multiple_descriptions(self, descriptions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes multiple job descriptions to find common patterns.

        Args:
            descriptions: List of job description dicts

        Returns:
            Dict with aggregated insights
        """
        all_insights = [self.analyze_job_description(desc) for desc in descriptions]

        # Aggregate insights
        all_skills = []
        all_responsibilities = []
        all_qualifications = []

        for insight in all_insights:
            all_skills.extend(insight['skills'])
            all_responsibilities.extend(insight['responsibilities'])
            all_qualifications.extend(insight['qualifications'])

        # Count frequency
        skill_freq = self._count_frequency(all_skills)
        responsibility_freq = self._count_frequency(all_responsibilities)
        qualification_freq = self._count_frequency(all_qualifications)

        return {
            'total_analyzed': len(descriptions),
            'common_skills': skill_freq,
            'common_responsibilities': responsibility_freq,
            'common_qualifications': qualification_freq,
            'insights': all_insights
        }

    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from job description text."""
        skills = []

        # Common PM skills to look for
        skill_keywords = [
            'product strategy', 'roadmap', 'stakeholder management', 'agile', 'scrum',
            'data analysis', 'sql', 'analytics', 'a/b testing', 'user research',
            'product vision', 'market research', 'competitive analysis', 'metrics',
            'kpis', 'product lifecycle', 'go-to-market', 'cross-functional',
            'prioritization', 'wireframing', 'prototyping', 'user stories',
            'technical specifications', 'api', 'mobile', 'web', 'saas', 'b2b', 'b2c'
        ]

        text_lower = text.lower()
        for skill in skill_keywords:
            if skill in text_lower:
                skills.append(skill)

        return skills

    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract responsibilities from job description text."""
        responsibilities = []

        # Look for bullet points or numbered lists
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if re.match(r'^[-•*]\s+', line) or re.match(r'^\d+\.\s+', line):
                # Remove bullet/number
                clean_line = re.sub(r'^[-•*\d.]+\s+', '', line)
                if len(clean_line) > 20:  # Filter out short lines
                    responsibilities.append(clean_line)

        return responsibilities

    def _extract_qualifications(self, text: str) -> List[str]:
        """Extract qualifications from job description text."""
        qualifications = []

        # Look for qualification indicators
        qual_patterns = [
            r'(\d+\+?\s+years?\s+(?:of\s+)?experience)',
            r'(bachelor\'?s?\s+degree|master\'?s?\s+degree|mba)',
            r'(proven track record)',
            r'(experience (?:with|in) [^.]+)'
        ]

        text_lower = text.lower()
        for pattern in qual_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            qualifications.extend(matches)

        return qualifications

    def _extract_experience_level(self, text: str) -> str:
        """Determine experience level from job description."""
        text_lower = text.lower()

        if 'senior' in text_lower or '7+ years' in text_lower or '8+ years' in text_lower:
            return 'Senior'
        elif 'lead' in text_lower or 'principal' in text_lower or '10+ years' in text_lower:
            return 'Lead/Principal'
        elif 'entry' in text_lower or '0-2 years' in text_lower or 'junior' in text_lower:
            return 'Entry-Level'
        else:
            return 'Mid-Level'

    def _extract_remote_policy(self, text: str) -> str:
        """Extract remote work policy."""
        text_lower = text.lower()

        if 'fully remote' in text_lower or '100% remote' in text_lower:
            return 'Fully Remote'
        elif 'hybrid' in text_lower:
            return 'Hybrid'
        elif 'on-site' in text_lower or 'onsite' in text_lower or 'in-office' in text_lower:
            return 'On-Site'
        else:
            return 'Not Specified'

    def _count_frequency(self, items: List[str]) -> Dict[str, int]:
        """Count frequency of items in list."""
        freq = {}
        for item in items:
            freq[item] = freq.get(item, 0) + 1

        # Sort by frequency
        return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
