#!/usr/bin/env python3
"""
Validation Interface - Easy-to-use wrapper for the validation engine
Provides quick validation checks and report generation
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from validation_engine import OutputValidator, ValidationResult, ConfidenceLevel

class ValidationInterface:
    """
    User-friendly interface for output validation
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize with optional configuration"""
        self.validator = OutputValidator()
        self.history = []
        self.config = self._load_config(config_path) if config_path else {}
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load config from {config_path}: {e}")
            return {}
    
    def quick_validate(self, content: str, sources: List[str] = None) -> Dict:
        """
        Quick validation with simple output
        
        Args:
            content: Text to validate
            sources: Optional list of source texts
            
        Returns:
            Simplified validation results
        """
        metadata = {'sources': sources or []}
        result = self.validator.validate_output(content, metadata)
        
        # Store in history
        self.history.append(result)
        
        # Create simplified output
        return {
            'passed': result.passed,
            'score': round(result.overall_score * 100, 1),
            'risk': result.hallucination_risk,
            'key_issues': result.validation_flags[:3],  # Top 3 issues
            'top_recommendation': result.recommendations[0] if result.recommendations else None
        }
    
    def full_validate(self, content: str, 
                     sources: List[str] = None,
                     scope: str = None,
                     domain: str = None) -> ValidationResult:
        """
        Full validation with comprehensive metadata
        
        Args:
            content: Text to validate
            sources: Optional list of source texts
            scope: Scope definition
            domain: Domain/field of the content
            
        Returns:
            Complete ValidationResult
        """
        metadata = {
            'sources': sources or [],
            'scope': scope,
            'domain': domain,
            'timestamp': datetime.now().isoformat()
        }
        
        result = self.validator.validate_output(content, metadata)
        self.history.append(result)
        
        return result
    
    def generate_report(self, result: ValidationResult, 
                       format: str = 'markdown') -> str:
        """
        Generate a validation report
        
        Args:
            result: ValidationResult to report on
            format: Output format ('markdown', 'json', 'text')
            
        Returns:
            Formatted report string
        """
        if format == 'json':
            return json.dumps(result.to_dict(), indent=2)
        elif format == 'markdown':
            return self._generate_markdown_report(result)
        else:
            return self._generate_text_report(result)
    
    def _generate_markdown_report(self, result: ValidationResult) -> str:
        """Generate markdown format report"""
        report = f"""# Validation Report

**Generated:** {result.timestamp}  
**Overall Score:** {result.overall_score*100:.1f}%  
**Status:** {'✅ PASSED' if result.passed else '❌ FAILED'}  
**Hallucination Risk:** {result.hallucination_risk}

## Confidence Distribution

"""
        for level, count in result.confidence_distribution.items():
            report += f"- **{level}:** {count} claims\n"
        
        report += f"""

## Key Metrics

- **Singleton Rate:** {result.singleton_rate*100:.1f}%
- **Validation Flags:** {len(result.validation_flags)}

## Issues Found

"""
        for flag in result.validation_flags:
            report += f"- {flag.replace('_', ' ').title()}\n"
        
        report += "\n## Recommendations\n\n"
        for i, rec in enumerate(result.recommendations, 1):
            report += f"{i}. {rec}\n"
        
        return report
    
    def _generate_text_report(self, result: ValidationResult) -> str:
        """Generate plain text report"""
        report = f"""
VALIDATION REPORT
================
Generated: {result.timestamp}
Overall Score: {result.overall_score*100:.1f}%
Status: {'PASSED' if result.passed else 'FAILED'}
Hallucination Risk: {result.hallucination_risk}

ISSUES:
"""
        for flag in result.validation_flags:
            report += f"  - {flag.replace('_', ' ')}\n"
        
        report += "\nRECOMMENDATIONS:\n"
        for i, rec in enumerate(result.recommendations, 1):
            report += f"  {i}. {rec}\n"
        
        return report
    
    def validate_file(self, file_path: str, 
                     source_files: List[str] = None) -> ValidationResult:
        """
        Validate content from a file
        
        Args:
            file_path: Path to file containing content to validate
            source_files: Optional paths to source files
            
        Returns:
            ValidationResult
        """
        # Read content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Read sources if provided
        sources = []
        if source_files:
            for source_path in source_files:
                try:
                    with open(source_path, 'r') as f:
                        sources.append(f.read())
                except Exception as e:
                    print(f"Warning: Could not read source {source_path}: {e}")
        
        return self.full_validate(content, sources)
    
    def batch_validate(self, contents: List[str]) -> List[Dict]:
        """
        Validate multiple outputs
        
        Args:
            contents: List of content strings to validate
            
        Returns:
            List of simplified validation results
        """
        results = []
        for content in contents:
            results.append(self.quick_validate(content))
        
        return results
    
    def get_statistics(self) -> Dict:
        """
        Get statistics from validation history
        
        Returns:
            Statistics dictionary
        """
        if not self.history:
            return {'message': 'No validation history available'}
        
        passed_count = sum(1 for r in self.history if r.passed)
        total_count = len(self.history)
        
        avg_score = sum(r.overall_score for r in self.history) / total_count
        avg_singleton = sum(r.singleton_rate for r in self.history) / total_count
        
        risk_distribution = {
            'LOW': sum(1 for r in self.history if r.hallucination_risk == 'LOW'),
            'MEDIUM': sum(1 for r in self.history if r.hallucination_risk == 'MEDIUM'),
            'HIGH': sum(1 for r in self.history if r.hallucination_risk == 'HIGH')
        }
        
        common_flags = {}
        for result in self.history:
            for flag in result.validation_flags:
                common_flags[flag] = common_flags.get(flag, 0) + 1
        
        return {
            'total_validations': total_count,
            'passed': passed_count,
            'failed': total_count - passed_count,
            'pass_rate': passed_count / total_count,
            'average_score': avg_score,
            'average_singleton_rate': avg_singleton,
            'risk_distribution': risk_distribution,
            'common_issues': sorted(common_flags.items(), 
                                   key=lambda x: x[1], reverse=True)[:5]
        }


# Convenience functions for direct use

def quick_check(content: str) -> Dict:
    """Quick validation check with minimal setup"""
    interface = ValidationInterface()
    return interface.quick_validate(content)

def validate_with_sources(content: str, sources: List[str]) -> Dict:
    """Validate content against provided sources"""
    interface = ValidationInterface()
    return interface.quick_validate(content, sources)

def validate_file(file_path: str) -> ValidationResult:
    """Validate content from a file"""
    interface = ValidationInterface()
    return interface.validate_file(file_path)

def generate_report(content: str, sources: List[str] = None) -> str:
    """Generate a full validation report"""
    interface = ValidationInterface()
    result = interface.full_validate(content, sources)
    return interface.generate_report(result, 'markdown')


# Example usage
if __name__ == "__main__":
    # Example content to validate
    example_content = """
    Based on extensive market research, the global AI market will reach $1.5 trillion 
    by 2030. Studies consistently show that 90% of enterprises are adopting AI 
    technologies. However, some aspects of implementation remain uncertain and 
    require further investigation. The computational complexity of certain AI tasks 
    makes perfect optimization impossible in polynomial time.
    """
    
    # Example sources
    example_sources = [
        "Market research indicates AI market growth projections vary between $500B and $2T by 2030.",
        "Enterprise AI adoption rates range from 50% to 90% depending on industry and region.",
        "NP-hard problems cannot be solved optimally in polynomial time unless P=NP."
    ]
    
    # Quick validation
    print("Quick Validation:")
    quick_result = quick_check(example_content)
    print(json.dumps(quick_result, indent=2))
    
    print("\n" + "="*50 + "\n")
    
    # Full validation with sources
    print("Full Validation Report:")
    report = generate_report(example_content, example_sources)
    print(report)
