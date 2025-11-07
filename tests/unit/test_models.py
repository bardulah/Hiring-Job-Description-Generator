"""
Unit tests for Pydantic models.
"""

import pytest
from pydantic import ValidationError
from src.core.models import JobDescription, CompanyInfo, HiringGoals


class TestJobDescription:
    """Tests for JobDescription model."""

    def test_valid_job_description(self):
        """Test creating a valid job description."""
        jd = JobDescription(
            title="Senior Product Manager",
            company="TestCorp",
            description=" ".join(["word"] * 100)  # 100 words minimum
        )
        assert jd.title == "Senior Product Manager"
        assert jd.company == "TestCorp"

    def test_invalid_description_too_short(self):
        """Test that short descriptions are rejected."""
        with pytest.raises(ValidationError):
            JobDescription(
                title="PM",
                company="TestCorp",
                description="Too short"
            )


class TestCompanyInfo:
    """Tests for CompanyInfo model."""

    def test_valid_company_info(self):
        """Test creating valid company info."""
        info = CompanyInfo(
            company_name="TestCorp",
            experience_level="Senior"
        )
        assert info.company_name == "TestCorp"
        assert info.experience_level == "Senior"

    def test_default_values(self):
        """Test default values are set correctly."""
        info = CompanyInfo(company_name="TestCorp")
        assert info.department == "Product"
        assert info.location == "Remote"
        assert info.experience_level == "Mid-Level"


class TestHiringGoals:
    """Tests for HiringGoals model."""

    def test_valid_hiring_goals(self):
        """Test creating valid hiring goals."""
        goals = HiringGoals(
            target_headcount=5,
            urgency="high"
        )
        assert goals.target_headcount == 5
        assert goals.urgency == "high"

    def test_invalid_headcount(self):
        """Test that invalid headcount is rejected."""
        with pytest.raises(ValidationError):
            HiringGoals(target_headcount=0)

    def test_invalid_date_format(self):
        """Test that invalid date format is rejected."""
        with pytest.raises(ValidationError):
            HiringGoals(start_date="2024/01/01")  # Wrong format
