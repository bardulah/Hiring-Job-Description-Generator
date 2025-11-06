"""
Pydantic models for type safety and validation.
"""

from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


# Type aliases
ExperienceLevel = Literal["Entry-Level", "Mid-Level", "Senior", "Lead/Principal"]
Urgency = Literal["low", "medium", "high"]
EmploymentType = Literal["Full-Time", "Part-Time", "Contract", "Internship"]


class JobDescription(BaseModel):
    """Model for job description input."""
    title: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=200)
    location: Optional[str] = None
    salary_range: Optional[str] = None
    description: str = Field(..., min_length=10)

    @field_validator('description')
    @classmethod
    def validate_description(cls, v: str) -> str:
        if len(v.split()) < 50:
            raise ValueError("Description must contain at least 50 words")
        return v


class CompanyInfo(BaseModel):
    """Model for company information."""
    company_name: str = Field(..., min_length=1, max_length=200)
    department: str = "Product"
    experience_level: ExperienceLevel = "Mid-Level"
    location: str = "Remote"
    employment_type: EmploymentType = "Full-Time"
    mission: Optional[str] = None
    about: Optional[str] = None
    product_focus: Optional[str] = None
    salary_range: Optional[str] = None
    equity: Optional[str] = None
    bonus: Optional[str] = None
    benefits: List[str] = Field(default_factory=list)
    custom_responsibilities: List[str] = Field(default_factory=list)
    required_qualifications: List[str] = Field(default_factory=list)
    preferred_qualifications: List[str] = Field(default_factory=list)
    required_skills: List[str] = Field(default_factory=list)
    differentiators: List[str] = Field(default_factory=list)
    application_instructions: Optional[str] = None


class HiringGoals(BaseModel):
    """Model for hiring goals and constraints."""
    target_headcount: int = Field(default=1, ge=1, le=100)
    urgency: Urgency = "medium"
    hiring_manager: str = "VP of Product"
    start_date: Optional[str] = None
    budget_max: Optional[int] = None
    differentiators: List[str] = Field(default_factory=list)

    @field_validator('start_date')
    @classmethod
    def validate_start_date(cls, v: Optional[str]) -> Optional[str]:
        if v:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError("start_date must be in YYYY-MM-DD format")
        return v


class HiringConfig(BaseModel):
    """Model for hiring process configuration."""
    include_technical: bool = True
    include_leadership: bool = True
    custom_stages: List[str] = Field(default_factory=list)
    min_interview_stages: int = Field(default=5, ge=3, le=10)


class GenerationRequest(BaseModel):
    """Model for complete generation request."""
    external_job_descriptions: List[JobDescription]
    company_info: CompanyInfo
    hiring_goals: Optional[HiringGoals] = None
    hiring_config: Optional[HiringConfig] = None
    output_formats: List[str] = Field(default=["json", "text"])

    @field_validator('external_job_descriptions')
    @classmethod
    def validate_job_descriptions(cls, v: List[JobDescription]) -> List[JobDescription]:
        if len(v) < 3:
            raise ValueError("At least 3 external job descriptions required for quality analysis")
        return v


class AnalysisResult(BaseModel):
    """Model for analysis results."""
    total_analyzed: int
    common_skills: Dict[str, int]
    common_responsibilities: Dict[str, int]
    common_qualifications: Dict[str, int]
    insights: List[Dict[str, Any]]
    salary_insights: Optional[Dict[str, Any]] = None
    market_comparison: Optional[Dict[str, Any]] = None


class GeneratedJobDescription(BaseModel):
    """Model for generated job description."""
    metadata: Dict[str, Any]
    header: Dict[str, str]
    overview: str
    responsibilities: List[str]
    qualifications: Dict[str, List[str]]
    skills: Dict[str, List[str]]
    compensation: Dict[str, Any]
    benefits: List[str]
    application_process: Dict[str, Any]


class GenerationResponse(BaseModel):
    """Model for complete generation response."""
    request_id: str
    generated_at: datetime
    status: str
    analysis: Optional[AnalysisResult] = None
    job_description: Optional[GeneratedJobDescription] = None
    hiring_plan: Optional[Dict[str, Any]] = None
    interview_rubric: Optional[Dict[str, Any]] = None
    timeline: Optional[Dict[str, Any]] = None
    output_files: Dict[str, str] = Field(default_factory=dict)
    processing_time: Optional[float] = None


class FeedbackRecord(BaseModel):
    """Model for tracking hiring outcomes."""
    candidate_id: str
    role: str
    hired: bool
    time_to_hire: Optional[int] = None  # days
    performance_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    retention_months: Optional[int] = None
    feedback_notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)


class UsageMetrics(BaseModel):
    """Model for usage analytics."""
    request_id: str
    role_type: str
    experience_level: ExperienceLevel
    processing_time: float
    success: bool
    error_message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
