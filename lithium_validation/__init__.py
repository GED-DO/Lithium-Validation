"""
Lithium-Validation: AI Output Validation Framework
Automatic validation with zero configuration required

Author: Guillermo Espinosa
Based on "Why Language Models Hallucinate" by Kalai, Nachum, Vempala, & Zhang
"""

__version__ = "2.0.0"  # Updated for auto-validation
__author__ = "Guillermo Espinosa"
__email__ = "hola@ged.do"

# Core validation components
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

# Auto-validation components (NEW)
try:
    from .mcp.auto_validator import (
        AutoValidator,
        ContentType,
        ValidationMode,
    )
    auto_available = True
except ImportError:
    auto_available = False
    AutoValidator = None

__all__ = [
    # Core components
    "ValidationInterface",
    "OutputValidator",
    "ValidationResult",
    "ConfidenceLevel",
    "quick_check",
    "quick_validate",
    # Auto components
    "AutoValidator",
    "ContentType", 
    "ValidationMode",
    # Convenience functions
    "validate",
    "auto_validate",
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

def auto_validate(content: str, enabled: bool = True) -> dict:
    """
    Automatic validation with zero configuration.
    Detects content type and applies appropriate validation.
    
    Args:
        content: Text content to validate
        enabled: Toggle validation on/off
    
    Returns:
        Dictionary with auto-detected validation results
        
    Example:
        >>> result = auto_validate("ROI will be 200%")
        >>> print(result['auto_decision']['message'])
        '⚠️ High-risk claim needs evidence'
    """
    if not auto_available or not enabled:
        return {'enabled': False, 'message': 'Auto-validation not available or disabled'}
    
    validator = AutoValidator()
    validator.enabled = enabled
    
    if not validator.should_validate(content):
        return {'skipped': True, 'reason': 'Content too short or not suitable for validation'}
    
    # Get automatic parameters
    auto_params = validator.get_auto_validation_params(content)
    
    # Perform validation with auto-detected parameters
    interface = ValidationInterface()
    result = interface.full_validate(
        content=content,
        sources=auto_params['sources'],
        domain=auto_params['params']['domain']
    )
    
    # Add auto-detection metadata
    return {
        'score': round(result.overall_score * 100, 1),
        'passed': result.passed,
        'risk': result.hallucination_risk,
        'auto_detected': {
            'content_type': auto_params['content_type'],
            'risk_level': auto_params['risk_level'],
            'validation_mode': auto_params['validation_mode'],
            'confidence': auto_params['type_confidence']
        },
        'auto_decision': validator.make_auto_decision(
            result.overall_score * 100,
            auto_params['risk_level']
        ),
        'issues': result.validation_flags[:3],
        'recommendations': result.recommendations[:2]
    }

# Set a global flag for auto-validation
AUTO_VALIDATION_ENABLED = True

def set_auto_validation(enabled: bool):
    """
    Enable or disable automatic validation globally.
    
    Args:
        enabled: True to enable, False to disable
    """
    global AUTO_VALIDATION_ENABLED
    AUTO_VALIDATION_ENABLED = enabled
    return f"Auto-validation {'enabled' if enabled else 'disabled'}"
