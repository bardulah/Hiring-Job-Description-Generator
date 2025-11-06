"""
Unit tests for NLP analyzer.
"""

import pytest
from src.analyzers.nlp_analyzer import NLPAnalyzer
from src.core.models import JobDescription
from src.core.exceptions import InsufficientDataError


class TestNLPAnalyzer:
    """Tests for NLPAnalyzer class."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance."""
        return NLPAnalyzer()

    @pytest.fixture
    def sample_job_description(self):
        """Create sample job description."""
        return JobDescription(
            title="Senior Product Manager",
            company="TechCorp",
            location="San Francisco",
            salary_range="$150k - $180k",
            description="""
            We are seeking a Senior Product Manager with 6+ years of experience.
            Responsibilities include:
            - Lead product strategy and roadmap
            - Work with engineering teams
            - Conduct user research
            - Define metrics and KPIs

            Requirements:
            - 6+ years in product management
            - Strong analytical skills
            - Experience with SQL and data analysis
            - Excellent communication skills
            - Bachelor's degree required
            """
        )

    def test_analyze_single_job_description(self, analyzer, sample_job_description):
        """Test analyzing a single job description."""
        result = analyzer.analyze_job_description(sample_job_description)

        assert result['title'] == "Senior Product Manager"
        assert result['company'] == "TechCorp"
        assert result['experience_level'] in ["Entry-Level", "Mid-Level", "Senior", "Lead/Principal"]
        assert isinstance(result['skills'], list)
        assert len(result['skills']) > 0

    def test_extract_experience_level(self, analyzer):
        """Test experience level extraction."""
        text_senior = "We need a senior product manager with 7+ years"
        level = analyzer._extract_experience_level(text_senior)
        assert level == "Senior"

        text_entry = "Looking for an entry-level associate product manager"
        level = analyzer._extract_experience_level(text_entry)
        assert level == "Entry-Level"

    def test_insufficient_data_error(self, analyzer):
        """Test that insufficient data raises error."""
        jds = [
            JobDescription(
                title="PM",
                company="Corp",
                description=" ".join(["word"] * 100)
            )
        ]

        with pytest.raises(InsufficientDataError):
            analyzer.analyze_multiple_descriptions(jds)

    def test_skill_extraction(self, analyzer, sample_job_description):
        """Test skill extraction from job description."""
        result = analyzer.analyze_job_description(sample_job_description)

        # Should extract some common PM skills
        skills_text = ' '.join(result['skills']).lower()
        assert 'sql' in skills_text or 'data analysis' in skills_text
