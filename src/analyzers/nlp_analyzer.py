"""
NLP-based job description analyzer.
Uses natural language processing for intelligent extraction.
"""

import re
from typing import Dict, List, Any, Set, Tuple, Optional
from collections import Counter
from ..core.models import JobDescription, AnalysisResult
from ..core.exceptions import AnalysisError, InsufficientDataError
from ..core.logging_config import get_logger
from ..core.config import config

logger = get_logger(__name__)


class NLPAnalyzer:
    """
    Advanced job description analyzer using NLP techniques.
    Gracefully degrades if spaCy is not available.
    """

    def __init__(self):
        self.use_spacy = config.get('analysis.use_nlp', True)
        self.skill_threshold = config.get('analysis.skill_threshold', 0.3)

        # Try to load spaCy
        self.nlp = None
        if self.use_spacy:
            try:
                import spacy
                try:
                    self.nlp = spacy.load('en_core_web_sm')
                    logger.info("Loaded spaCy model successfully")
                except OSError:
                    logger.warning("spaCy model not found. Run: python -m spacy download en_core_web_sm")
                    logger.info("Falling back to rule-based extraction")
            except ImportError:
                logger.warning("spaCy not installed. Using rule-based extraction")

        # Enhanced skill patterns
        self.skill_patterns = self._build_skill_patterns()
        self.experience_patterns = self._build_experience_patterns()

    def _build_skill_patterns(self) -> Dict[str, List[str]]:
        """Build comprehensive skill patterns."""
        return {
            'product_management': [
                'product strategy', 'product vision', 'roadmap', 'roadmapping',
                'product lifecycle', 'product development', 'product planning',
                'feature prioritization', 'backlog management', 'user stories',
                'product metrics', 'product analytics', 'kpis'
            ],
            'technical': [
                'sql', 'python', 'api', 'rest', 'graphql', 'json', 'xml',
                'cloud', 'aws', 'azure', 'gcp', 'kubernetes', 'docker',
                'microservices', 'system design', 'architecture', 'technical specifications',
                'data structures', 'algorithms', 'database', 'nosql'
            ],
            'analytics': [
                'data analysis', 'analytics', 'a/b testing', 'experimentation',
                'metrics', 'kpi', 'tableau', 'google analytics', 'mixpanel',
                'amplitude', 'sql', 'excel', 'statistics', 'data-driven',
                'quantitative analysis', 'cohort analysis', 'funnel analysis'
            ],
            'design': [
                'ux', 'ui', 'user experience', 'user interface', 'wireframing',
                'prototyping', 'figma', 'sketch', 'adobe xd', 'invision',
                'user research', 'usability testing', 'design thinking'
            ],
            'business': [
                'business strategy', 'market analysis', 'competitive analysis',
                'go-to-market', 'gtm', 'pricing', 'monetization', 'revenue',
                'p&l', 'roi', 'business case', 'financial modeling',
                'market research', 'customer segmentation'
            ],
            'agile': [
                'agile', 'scrum', 'kanban', 'sprint', 'jira', 'confluence',
                'standup', 'retrospective', 'sprint planning', 'agile methodologies'
            ],
            'leadership': [
                'stakeholder management', 'cross-functional', 'leadership',
                'team management', 'mentoring', 'coaching', 'influence',
                'communication', 'presentation', 'executive communication'
            ],
            'domain': [
                'saas', 'b2b', 'b2c', 'enterprise', 'consumer', 'mobile',
                'web', 'platform', 'marketplace', 'e-commerce', 'fintech',
                'healthtech', 'edtech', 'marketplace'
            ]
        }

    def _build_experience_patterns(self) -> List[Tuple[re.Pattern, str]]:
        """Build regex patterns for experience level detection."""
        return [
            (re.compile(r'(\d+)\+?\s*(?:to|\-|–)?\s*(\d+)?\s*years?'), 'years'),
            (re.compile(r'entry[- ]level|junior|associate', re.I), 'entry'),
            (re.compile(r'mid[- ]level|intermediate', re.I), 'mid'),
            (re.compile(r'senior|sr\.?', re.I), 'senior'),
            (re.compile(r'lead|principal|staff|director', re.I), 'lead'),
        ]

    def analyze_job_description(self, job_desc: JobDescription) -> Dict[str, Any]:
        """
        Analyze a single job description using NLP.

        Args:
            job_desc: JobDescription model

        Returns:
            Dict with extracted insights
        """
        try:
            text = job_desc.description
            text_lower = text.lower()

            # Extract skills using NLP or rules
            if self.nlp:
                skills = self._extract_skills_nlp(text)
            else:
                skills = self._extract_skills_rules(text_lower)

            # Extract responsibilities and qualifications
            responsibilities = self._extract_sections(text, ['responsibilities', 'duties', 'what you'])
            qualifications = self._extract_sections(text, ['qualifications', 'requirements', 'you have'])

            # Extract experience level
            experience_level = self._extract_experience_level(text)

            # Extract salary insights
            salary_info = self._extract_salary_info(job_desc.salary_range, text)

            # Detect remote policy
            remote_policy = self._extract_remote_policy(text_lower)

            # Detect company size and stage
            company_info = self._extract_company_info(text_lower)

            insights = {
                'title': job_desc.title,
                'company': job_desc.company,
                'skills': skills,
                'skills_by_category': self._categorize_skills(skills),
                'responsibilities': responsibilities,
                'qualifications': qualifications,
                'experience_level': experience_level,
                'experience_years': self._extract_years_experience(text),
                'salary_range': salary_info,
                'location': job_desc.location or 'Not specified',
                'remote_policy': remote_policy,
                'company_info': company_info,
                'required_education': self._extract_education(text),
                'nice_to_have': self._extract_nice_to_have(text)
            }

            logger.debug(f"Analyzed job: {job_desc.title} at {job_desc.company}")
            return insights

        except Exception as e:
            logger.error(f"Error analyzing job description: {e}")
            raise AnalysisError(f"Failed to analyze job description: {e}")

    def analyze_multiple_descriptions(self, descriptions: List[JobDescription]) -> AnalysisResult:
        """
        Analyze multiple job descriptions to find patterns.

        Args:
            descriptions: List of JobDescription models

        Returns:
            AnalysisResult model with aggregated insights
        """
        min_required = config.get('analysis.min_job_descriptions', 3)
        if len(descriptions) < min_required:
            raise InsufficientDataError(
                f"At least {min_required} job descriptions required for quality analysis. Got {len(descriptions)}."
            )

        logger.info(f"Analyzing {len(descriptions)} job descriptions...")

        try:
            all_insights = [self.analyze_job_description(desc) for desc in descriptions]

            # Aggregate data
            all_skills = []
            all_responsibilities = []
            all_qualifications = []
            salary_ranges = []

            for insight in all_insights:
                all_skills.extend(insight['skills'])
                all_responsibilities.extend(insight['responsibilities'])
                all_qualifications.extend(insight['qualifications'])
                if insight.get('salary_range', {}).get('min'):
                    salary_ranges.append(insight['salary_range'])

            # Count frequencies
            skill_freq = dict(Counter(all_skills).most_common(50))
            responsibility_freq = dict(Counter(all_responsibilities).most_common(30))
            qualification_freq = dict(Counter(all_qualifications).most_common(30))

            # Salary insights
            salary_insights = self._aggregate_salary_data(salary_ranges) if salary_ranges else None

            # Market comparison
            market_comparison = self._generate_market_comparison(all_insights)

            result = AnalysisResult(
                total_analyzed=len(descriptions),
                common_skills=skill_freq,
                common_responsibilities=responsibility_freq,
                common_qualifications=qualification_freq,
                insights=[insight for insight in all_insights],
                salary_insights=salary_insights,
                market_comparison=market_comparison
            )

            logger.info(f"Analysis complete. Found {len(skill_freq)} unique skills.")
            return result

        except Exception as e:
            logger.error(f"Error in multi-description analysis: {e}")
            raise AnalysisError(f"Failed to analyze descriptions: {e}")

    def _extract_skills_nlp(self, text: str) -> List[str]:
        """Extract skills using spaCy NLP."""
        if not self.nlp:
            return self._extract_skills_rules(text.lower())

        doc = self.nlp(text)
        skills = set()

        # Extract using noun chunks
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.lower().strip()
            # Check against known skills
            for category, skill_list in self.skill_patterns.items():
                for skill in skill_list:
                    if skill in chunk_text or chunk_text in skill:
                        skills.add(skill)

        # Extract using entities
        for ent in doc.ents:
            if ent.label_ in ['PRODUCT', 'ORG', 'SKILL']:
                ent_text = ent.text.lower()
                for category, skill_list in self.skill_patterns.items():
                    for skill in skill_list:
                        if skill in ent_text:
                            skills.add(skill)

        # Also use rule-based extraction as backup
        rules_skills = self._extract_skills_rules(text.lower())
        skills.update(rules_skills)

        return list(skills)

    def _extract_skills_rules(self, text: str) -> List[str]:
        """Extract skills using rule-based pattern matching."""
        skills = set()

        for category, skill_list in self.skill_patterns.items():
            for skill in skill_list:
                # Use word boundaries for better matching
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text, re.IGNORECASE):
                    skills.add(skill)

        return list(skills)

    def _categorize_skills(self, skills: List[str]) -> Dict[str, List[str]]:
        """Categorize skills into different types."""
        categorized = {category: [] for category in self.skill_patterns.keys()}

        for skill in skills:
            for category, skill_list in self.skill_patterns.items():
                if skill in skill_list:
                    categorized[category].append(skill)
                    break

        return {k: v for k, v in categorized.items() if v}

    def _extract_sections(self, text: str, keywords: List[str]) -> List[str]:
        """Extract bullet points from specific sections."""
        items = []
        lines = text.split('\n')

        in_section = False
        for i, line in enumerate(lines):
            line = line.strip()

            # Check if we're entering a relevant section
            if any(keyword in line.lower() for keyword in keywords):
                in_section = True
                continue

            # Check if we're leaving the section
            if in_section and line and not re.match(r'^[-•*\d.]', line):
                if i < len(lines) - 1 and not re.match(r'^[-•*\d.]', lines[i + 1].strip()):
                    in_section = False

            # Extract bullet points
            if in_section and re.match(r'^[-•*]\s+', line) or re.match(r'^\d+\.\s+', line):
                clean_line = re.sub(r'^[-•*\d.]+\s+', '', line)
                if len(clean_line) > 20:
                    items.append(clean_line[:200])  # Limit length

        return items[:20]  # Limit total items

    def _extract_experience_level(self, text: str) -> str:
        """Determine experience level from text."""
        text_lower = text.lower()

        # Check for explicit mentions
        if re.search(r'\blead\b|\bprincipal\b|\bstaff\b', text_lower):
            return 'Lead/Principal'
        if re.search(r'\bsenior\b|\bsr\.?\b', text_lower):
            return 'Senior'
        if re.search(r'\bentry\b|\bjunior\b|\bassociate\b', text_lower):
            return 'Entry-Level'

        # Check years of experience
        years = self._extract_years_experience(text)
        if years:
            if years >= 10:
                return 'Lead/Principal'
            elif years >= 6:
                return 'Senior'
            elif years >= 3:
                return 'Mid-Level'
            else:
                return 'Entry-Level'

        return 'Mid-Level'

    def _extract_years_experience(self, text: str) -> Optional[int]:
        """Extract required years of experience."""
        patterns = [
            r'(\d+)\+?\s*(?:to|\-|–)\s*(\d+)?\s*years?',
            r'(\d+)\+?\s*years?'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))

        return None

    def _extract_salary_info(self, salary_range: Optional[str], text: str) -> Dict[str, Any]:
        """Extract and parse salary information."""
        if not salary_range:
            # Try to find in text
            salary_pattern = r'\$(\d{1,3}(?:,\d{3})*(?:k|K)?)\s*(?:to|\-|–)\s*\$?(\d{1,3}(?:,\d{3})*(?:k|K)?)'
            match = re.search(salary_pattern, text)
            if match:
                salary_range = f"${match.group(1)} - ${match.group(2)}"

        if not salary_range:
            return {}

        # Parse salary range
        amounts = re.findall(r'\$?(\d{1,3}(?:,\d{3})*(?:k|K)?)', salary_range)
        if len(amounts) >= 2:
            try:
                min_sal = self._parse_salary(amounts[0])
                max_sal = self._parse_salary(amounts[1])
                return {
                    'min': min_sal,
                    'max': max_sal,
                    'average': (min_sal + max_sal) // 2,
                    'range': salary_range
                }
            except:
                pass

        return {'range': salary_range}

    def _parse_salary(self, salary_str: str) -> int:
        """Parse salary string to integer."""
        salary_str = salary_str.replace(',', '').replace('$', '')
        if salary_str.endswith('k') or salary_str.endswith('K'):
            return int(salary_str[:-1]) * 1000
        return int(salary_str)

    def _extract_remote_policy(self, text: str) -> str:
        """Extract remote work policy."""
        if re.search(r'fully remote|100%\s*remote|remote[- ]first', text):
            return 'Fully Remote'
        if re.search(r'hybrid', text):
            return 'Hybrid'
        if re.search(r'on[- ]?site|in[- ]office', text):
            return 'On-Site'
        if re.search(r'remote', text):
            return 'Remote Available'
        return 'Not Specified'

    def _extract_company_info(self, text: str) -> Dict[str, Any]:
        """Extract company information."""
        info = {}

        # Company stage
        if re.search(r'startup|early[- ]stage', text):
            info['stage'] = 'Startup'
        elif re.search(r'series [a-d]', text):
            match = re.search(r'series ([a-d])', text)
            info['stage'] = f'Series {match.group(1).upper()}'
        elif re.search(r'enterprise|fortune', text):
            info['stage'] = 'Enterprise'

        # Company size
        size_match = re.search(r'(\d+)\+?\s*(?:person|people|employee)', text)
        if size_match:
            info['size'] = f"{size_match.group(1)}+ employees"

        return info

    def _extract_education(self, text: str) -> List[str]:
        """Extract education requirements."""
        education = []
        text_lower = text.lower()

        education_keywords = [
            r"bachelor'?s?\s+degree",
            r"master'?s?\s+degree",
            r"mba",
            r"ph\.?d\.?",
            r"computer science degree",
            r"technical degree",
            r"engineering degree"
        ]

        for keyword in education_keywords:
            if re.search(keyword, text_lower):
                education.append(re.search(keyword, text_lower).group(0))

        return education

    def _extract_nice_to_have(self, text: str) -> List[str]:
        """Extract nice-to-have qualifications."""
        nice_to_have = []
        text_lower = text.lower()

        # Find "nice to have" or "preferred" sections
        nice_keywords = [
            'nice to have', 'preferred', 'bonus', 'plus', 'ideal candidate'
        ]

        lines = text.split('\n')
        in_nice_section = False

        for line in lines:
            if any(keyword in line.lower() for keyword in nice_keywords):
                in_nice_section = True
                continue

            if in_nice_section and re.match(r'^[-•*]\s+', line):
                clean_line = re.sub(r'^[-•*\d.]+\s+', '', line.strip())
                if len(clean_line) > 10:
                    nice_to_have.append(clean_line[:200])

        return nice_to_have[:10]

    def _aggregate_salary_data(self, salary_ranges: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate salary data from multiple sources."""
        if not salary_ranges:
            return {}

        min_salaries = [s['min'] for s in salary_ranges if 'min' in s]
        max_salaries = [s['max'] for s in salary_ranges if 'max' in s]

        if not min_salaries:
            return {}

        return {
            'market_min': min(min_salaries),
            'market_max': max(max_salaries),
            'average_min': sum(min_salaries) // len(min_salaries),
            'average_max': sum(max_salaries) // len(max_salaries) if max_salaries else None,
            'sample_size': len(salary_ranges)
        }

    def _generate_market_comparison(self, insights: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate market comparison insights."""
        comparison = {
            'total_roles_analyzed': len(insights),
            'experience_levels': Counter([i['experience_level'] for i in insights]),
            'remote_policies': Counter([i['remote_policy'] for i in insights]),
            'common_requirements': self._find_common_patterns(insights),
        }

        return comparison

    def _find_common_patterns(self, insights: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Find common patterns across job descriptions."""
        patterns = {}

        # Most common skills across all jobs
        all_skills = []
        for insight in insights:
            all_skills.extend(insight.get('skills', []))

        patterns['top_skills'] = [skill for skill, count in Counter(all_skills).most_common(10)]

        # Common years of experience
        years = [i.get('experience_years') for i in insights if i.get('experience_years')]
        if years:
            patterns['average_years_required'] = sum(years) / len(years)

        # Education requirements frequency
        has_degree_req = sum(1 for i in insights if i.get('required_education'))
        patterns['education_requirement_frequency'] = has_degree_req / len(insights)

        return patterns
