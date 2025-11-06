"""
Custom exceptions for the Hiring System Generator.
"""


class HiringSystemError(Exception):
    """Base exception for all hiring system errors."""
    pass


class ValidationError(HiringSystemError):
    """Raised when input validation fails."""
    pass


class InvalidJobDescriptionError(ValidationError):
    """Raised when job description format is invalid."""
    pass


class InvalidCompanyInfoError(ValidationError):
    """Raised when company info is invalid."""
    pass


class InsufficientDataError(HiringSystemError):
    """Raised when not enough data to generate results."""
    pass


class AnalysisError(HiringSystemError):
    """Raised when analysis fails."""
    pass


class GenerationError(HiringSystemError):
    """Raised when generation fails."""
    pass


class TemplateNotFoundError(HiringSystemError):
    """Raised when required template is not found."""
    pass


class ConfigurationError(HiringSystemError):
    """Raised when configuration is invalid."""
    pass


class ExportError(HiringSystemError):
    """Raised when export fails."""
    pass


class CacheError(HiringSystemError):
    """Raised when cache operations fail."""
    pass


class PluginError(HiringSystemError):
    """Raised when plugin fails to load or execute."""
    pass
