"""
Lithium-Validation: AI Output Validation Framework
Stabilizing AI outputs through systematic validation

Author: Guillermo Espinosa
Based on "Why Language Models Hallucinate" by Kalai, Nachum, Vempala, & Zhang
"""

__version__ = "1.0.0"
__author__ = "Guillermo Espinosa"
__email__ = "hola@ged.do"

from .core.validation_interface import (
    ValidationInterface,
    quick_check,
    quick_validate,
)
from .core.validation_engine import (
    OutputValidator,
    ValidationResult,
    ConfidenceLevel,
)

__all__ = [
    "ValidationInterface",
    "OutputValidator",
    "ValidationResult",
    "ConfidenceLevel",
    "quick_check",
    "quick_validate",
]

def validate(content: str, sources: list = None, domain: str = "general") -> dict:
    """
    Quick validation of content with optional sources.
    
    Args:
        content: Text content to validate
        sources: Optional list of source texts for cross-validation
        domain: Domain context (general, consulting, technical, research)
    
    Returns:
        Dictionary with score, risk level, and recommendations
    """
    return quick_check(content, sources, domain)
