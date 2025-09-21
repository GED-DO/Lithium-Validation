#!/usr/bin/env python3
"""
Validation Engine for Output Quality Assurance
Based on "Why Language Models Hallucinate" (Kalai et al., 2025)

This system implements a three-stage validation process:
1. Pre-Validation Check
2. Output Generation Assessment  
3. Quality Assurance Verification
"""

import json
import re
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

class ConfidenceLevel(Enum):
    """Confidence levels based on paper's threshold recommendations"""
    HIGH = 0.9  # t=0.9, penalty 9 for errors
    MEDIUM = 0.75  # t=0.75, penalty 2 for errors  
    LOW = 0.5  # t=0.5, penalty 1 for errors
    UNCERTAIN = 0.0  # Below threshold - should abstain

class ClaimType(Enum):
    """Types of claims based on epistemological foundations"""
    EMPIRICAL = "empirical"  # Based on verifiable data
    INFERENTIAL = "inferential"  # Logical deduction from data
    HYPOTHETICAL = "hypothetical"  # Speculation or projection
    ARBITRARY = "arbitrary"  # No pattern in data (singleton)
    COMPUTATIONAL = "computational"  # Requires complex calculation

@dataclass
class ValidationResult:
    """Comprehensive validation results"""
    timestamp: str
    overall_score: float
    confidence_distribution: Dict[str, float]
    singleton_rate: float
    validation_flags: List[str]
    recommendations: List[str]
    passed: bool
    hallucination_risk: str
    
    def to_dict(self):
        return asdict(self)

class OutputValidator:
    """
    Main validation engine implementing the three-stage process
    from the hallucination paper
    """
    
    def __init__(self):
        self.singleton_threshold = 0.2  # 20% singleton rate threshold
        self.minimum_sources = 2  # Minimum sources for validation
        self.confidence_weights = {
            ConfidenceLevel.HIGH: 1.0,
            ConfidenceLevel.MEDIUM: 0.75,
            ConfidenceLevel.LOW: 0.5,
            ConfidenceLevel.UNCERTAIN: 0.0
        }
        
    def validate_output(self, 
                       content: str,
                       metadata: Optional[Dict] = None) -> ValidationResult:
        """
        Main validation function implementing the three-stage process
        
        Args:
            content: The output text to validate
            metadata: Optional metadata about sources, confidence, etc.
            
        Returns:
            ValidationResult with comprehensive analysis
        """
        metadata = metadata or {}
        
        # Stage 1: Pre-Validation
        pre_validation = self._pre_validation_check(content, metadata)
        
        # Stage 2: Output Generation Assessment
        generation_assessment = self._assess_output_generation(content, metadata)
        
        # Stage 3: Quality Assurance
        quality_scores = self._quality_assurance_check(
            content, metadata, pre_validation, generation_assessment
        )
        
        # Compile final results
        return self._compile_results(
            pre_validation, generation_assessment, quality_scores, metadata
        )
    
    def _pre_validation_check(self, content: str, metadata: Dict) -> Dict:
        """
        Stage 1: Pre-Validation Check
        Implements the paper's query classification and context enrichment
        """
        results = {
            'claim_types': self._classify_claims(content),
            'ambiguity_score': self._check_ambiguity(content),
            'scope_defined': self._verify_scope(content, metadata),
            'temporal_context': self._check_temporal_context(content),
            'source_count': len(metadata.get('sources', [])),
            'has_abstentions': self._check_for_abstentions(content)
        }
        
        # Check for singleton patterns (arbitrary facts)
        results['singleton_claims'] = self._identify_singletons(content, metadata)
        
        return results
    
    def _assess_output_generation(self, content: str, metadata: Dict) -> Dict:
        """
        Stage 2: Output Generation Assessment
        Evaluates confidence distribution and claim support
        """
        claims = self._extract_claims(content)
        
        assessment = {
            'total_claims': len(claims),
            'confidence_distribution': {},
            'unsupported_claims': [],
            'cross_validated': [],
            'computational_hardness': []
        }
        
        for claim in claims:
            confidence = self._assess_claim_confidence(claim, metadata)
            claim_type = self._get_claim_type(claim)
            
            # Track confidence distribution
            if confidence.name not in assessment['confidence_distribution']:
                assessment['confidence_distribution'][confidence.name] = 0
            assessment['confidence_distribution'][confidence.name] += 1
            
            # Check support
            if not self._is_claim_supported(claim, metadata):
                assessment['unsupported_claims'].append(claim)
            
            # Check for computational intractability
            if self._is_computationally_hard(claim):
                assessment['computational_hardness'].append(claim)
                
        return assessment
    
    def _quality_assurance_check(self, content: str, metadata: Dict,
                                pre_validation: Dict, 
                                generation_assessment: Dict) -> Dict:
        """
        Stage 3: Quality Assurance Verification
        Implements the paper's error rate calculations
        """
        quality_scores = {}
        
        # Calculate singleton rate (sr from the paper)
        total_claims = generation_assessment['total_claims']
        singleton_count = len(pre_validation.get('singleton_claims', []))
        quality_scores['singleton_rate'] = (
            singleton_count / total_claims if total_claims > 0 else 0
        )
        
        # Apply the 2:1 rule from the paper
        validated = total_claims - len(generation_assessment['unsupported_claims'])
        unvalidated = len(generation_assessment['unsupported_claims'])
        quality_scores['validation_ratio'] = (
            validated / (unvalidated + 1)  # +1 to avoid division by zero
        )
        
        # Calculate confidence-weighted score
        conf_dist = generation_assessment['confidence_distribution']
        weighted_score = 0
        total_weight = 0
        
        for level_name, count in conf_dist.items():
            level = ConfidenceLevel[level_name]
            weight = self.confidence_weights[level]
            weighted_score += weight * count
            total_weight += count
            
        quality_scores['confidence_weighted_score'] = (
            weighted_score / total_weight if total_weight > 0 else 0
        )
        
        # Bias detection
        quality_scores['bias_checks'] = self._check_biases(content)
        
        # Calculate hallucination risk based on paper's formulas
        quality_scores['hallucination_risk'] = self._calculate_hallucination_risk(
            quality_scores, generation_assessment
        )
        
        return quality_scores
    
    def _compile_results(self, pre_validation: Dict, 
                         generation_assessment: Dict,
                         quality_scores: Dict,
                         metadata: Dict) -> ValidationResult:
        """
        Compile all validation stages into final result
        """
        # Overall score calculation
        overall_score = self._calculate_overall_score(
            pre_validation, generation_assessment, quality_scores
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            pre_validation, generation_assessment, quality_scores
        )
        
        # Validation flags
        flags = self._generate_flags(
            pre_validation, generation_assessment, quality_scores
        )
        
        # Determine if output passes validation
        passed = (
            overall_score >= 0.7 and
            quality_scores['singleton_rate'] < self.singleton_threshold and
            quality_scores['validation_ratio'] >= 2.0
        )
        
        # Determine hallucination risk level
        risk_score = quality_scores['hallucination_risk']
        if risk_score < 0.2:
            risk_level = "LOW"
        elif risk_score < 0.5:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"
        
        return ValidationResult(
            timestamp=datetime.now().isoformat(),
            overall_score=overall_score,
            confidence_distribution=generation_assessment['confidence_distribution'],
            singleton_rate=quality_scores['singleton_rate'],
            validation_flags=flags,
            recommendations=recommendations,
            passed=passed,
            hallucination_risk=risk_level
        )
    
    # Helper methods
    def _classify_claims(self, content: str) -> Dict[str, int]:
        """Classify claims by type"""
        claims = self._extract_claims(content)
        classification = {
            ClaimType.EMPIRICAL.value: 0,
            ClaimType.INFERENTIAL.value: 0,
            ClaimType.HYPOTHETICAL.value: 0,
            ClaimType.ARBITRARY.value: 0,
            ClaimType.COMPUTATIONAL.value: 0
        }
        
        for claim in claims:
            claim_type = self._get_claim_type(claim)
            classification[claim_type.value] += 1
            
        return classification
    
    def _extract_claims(self, content: str) -> List[str]:
        """Extract individual claims from content"""
        # Simple sentence splitting for now
        # In production, use NLP for better extraction
        sentences = re.split(r'[.!?]+', content)
        claims = [s.strip() for s in sentences if s.strip()]
        return claims
    
    def _get_claim_type(self, claim: str) -> ClaimType:
        """Determine the type of a claim"""
        claim_lower = claim.lower()
        
        # Heuristic classification
        if any(word in claim_lower for word in ['data shows', 'evidence', 'study', 'research']):
            return ClaimType.EMPIRICAL
        elif any(word in claim_lower for word in ['therefore', 'thus', 'implies', 'suggests']):
            return ClaimType.INFERENTIAL
        elif any(word in claim_lower for word in ['might', 'could', 'possibly', 'hypothesis']):
            return ClaimType.HYPOTHETICAL
        elif any(word in claim_lower for word in ['calculate', 'compute', 'algorithm']):
            return ClaimType.COMPUTATIONAL
        else:
            return ClaimType.ARBITRARY
    
    def _check_ambiguity(self, content: str) -> float:
        """Check for ambiguous language"""
        ambiguous_terms = ['maybe', 'perhaps', 'might', 'could', 'possibly', 
                          'somewhat', 'relatively', 'fairly', 'quite']
        
        words = content.lower().split()
        ambiguous_count = sum(1 for word in words if word in ambiguous_terms)
        
        return ambiguous_count / len(words) if words else 0
    
    def _verify_scope(self, content: str, metadata: Dict) -> bool:
        """Check if scope is properly defined"""
        scope_indicators = ['specifically', 'limited to', 'within', 'scope', 
                           'boundaries', 'constraints']
        
        has_scope_language = any(ind in content.lower() for ind in scope_indicators)
        has_scope_metadata = 'scope' in metadata
        
        return has_scope_language or has_scope_metadata
    
    def _check_temporal_context(self, content: str) -> Dict[str, bool]:
        """Check temporal context markers"""
        return {
            'has_dates': bool(re.search(r'\b\d{4}\b', content)),
            'has_time_markers': any(word in content.lower() for word in 
                                   ['currently', 'recently', 'historically', 
                                    'previously', 'future']),
            'has_version_info': bool(re.search(r'v\d+|\d+\.\d+', content))
        }
    
    def _check_for_abstentions(self, content: str) -> bool:
        """Check if output appropriately abstains when uncertain"""
        abstention_phrases = [
            "don't know", "uncertain", "cannot determine", "insufficient data",
            "requires further", "unable to", "beyond scope", "cannot verify"
        ]
        
        return any(phrase in content.lower() for phrase in abstention_phrases)
    
    def _identify_singletons(self, content: str, metadata: Dict) -> List[str]:
        """Identify singleton claims (appearing only once in sources)"""
        singletons = []
        claims = self._extract_claims(content)
        sources = metadata.get('sources', [])
        
        for claim in claims:
            # Check if claim appears in only one source
            appearances = sum(1 for source in sources 
                            if self._claim_in_source(claim, source))
            if appearances <= 1:
                singletons.append(claim)
                
        return singletons
    
    def _claim_in_source(self, claim: str, source: str) -> bool:
        """Check if a claim appears in a source"""
        # Simplified check - in production use semantic similarity
        key_words = [w for w in claim.lower().split() 
                    if len(w) > 4 and w not in ['that', 'this', 'with', 'from']]
        
        if len(key_words) < 2:
            return False
            
        matches = sum(1 for word in key_words if word in source.lower())
        return matches >= len(key_words) * 0.5
    
    def _assess_claim_confidence(self, claim: str, metadata: Dict) -> ConfidenceLevel:
        """Assess confidence level for a specific claim"""
        # Check claim support in metadata
        sources = metadata.get('sources', [])
        support_count = sum(1 for source in sources 
                          if self._claim_in_source(claim, source))
        
        # Check claim type
        claim_type = self._get_claim_type(claim)
        
        # Determine confidence based on support and type
        if support_count >= 3 and claim_type == ClaimType.EMPIRICAL:
            return ConfidenceLevel.HIGH
        elif support_count >= 2:
            return ConfidenceLevel.MEDIUM
        elif support_count >= 1:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.UNCERTAIN
    
    def _is_claim_supported(self, claim: str, metadata: Dict) -> bool:
        """Check if a claim has adequate support"""
        sources = metadata.get('sources', [])
        support_count = sum(1 for source in sources 
                          if self._claim_in_source(claim, source))
        
        return support_count >= self.minimum_sources
    
    def _is_computationally_hard(self, claim: str) -> bool:
        """Check if claim involves computationally intractable problems"""
        hard_indicators = [
            'optimize', 'solve np-hard', 'factor large', 'decrypt',
            'break encryption', 'predict perfectly', 'guarantee optimal'
        ]
        
        claim_lower = claim.lower()
        return any(indicator in claim_lower for indicator in hard_indicators)
    
    def _check_biases(self, content: str) -> Dict[str, bool]:
        """Check for various biases mentioned in the paper"""
        return {
            'confirmation_bias': self._check_confirmation_bias(content),
            'recency_bias': self._check_recency_bias(content),
            'geographic_bias': self._check_geographic_bias(content)
        }
    
    def _check_confirmation_bias(self, content: str) -> bool:
        """Check for confirmation bias indicators"""
        one_sided_terms = ['always', 'never', 'all', 'none', 'every', 'no one']
        return any(term in content.lower() for term in one_sided_terms)
    
    def _check_recency_bias(self, content: str) -> bool:
        """Check for recency bias"""
        recency_terms = ['latest', 'newest', 'most recent', 'cutting-edge', 'state-of-the-art']
        return any(term in content.lower() for term in recency_terms)
    
    def _check_geographic_bias(self, content: str) -> bool:
        """Check for geographic bias"""
        # Simple check - in production use more sophisticated location detection
        locations = ['america', 'europe', 'asia', 'western', 'eastern']
        return sum(1 for loc in locations if loc in content.lower()) >= 2
    
    def _calculate_hallucination_risk(self, quality_scores: Dict,
                                     generation_assessment: Dict) -> float:
        """
        Calculate hallucination risk based on paper's formula:
        err ≥ 2 · erriiv - |Vc|/|Ec| - δ
        """
        singleton_rate = quality_scores['singleton_rate']
        unsupported_ratio = (len(generation_assessment['unsupported_claims']) / 
                            (generation_assessment['total_claims'] + 1))
        
        # Simplified risk calculation based on paper's insights
        risk = (singleton_rate * 0.4 + 
                unsupported_ratio * 0.4 + 
                (1 - quality_scores['confidence_weighted_score']) * 0.2)
        
        return min(1.0, risk)
    
    def _calculate_overall_score(self, pre_validation: Dict,
                                generation_assessment: Dict,
                                quality_scores: Dict) -> float:
        """Calculate overall validation score"""
        # Weighted scoring based on paper's emphasis
        pre_val_score = (
            (1.0 if pre_validation['scope_defined'] else 0.5) *
            (1.0 if pre_validation['has_abstentions'] else 0.7) *
            (1.0 - pre_validation['ambiguity_score'])
        )
        
        gen_score = quality_scores['confidence_weighted_score']
        
        qa_score = (
            (1.0 - quality_scores['singleton_rate']) * 0.5 +
            min(1.0, quality_scores['validation_ratio'] / 4.0) * 0.5
        )
        
        # Weighted average
        overall = (pre_val_score * 0.3 + gen_score * 0.4 + qa_score * 0.3)
        
        return overall
    
    def _generate_recommendations(self, pre_validation: Dict,
                                 generation_assessment: Dict,
                                 quality_scores: Dict) -> List[str]:
        """Generate specific recommendations based on validation"""
        recommendations = []
        
        # Check singleton rate
        if quality_scores['singleton_rate'] > self.singleton_threshold:
            recommendations.append(
                f"High singleton rate ({quality_scores['singleton_rate']:.2%}). "
                "Add cross-validation from additional sources."
            )
        
        # Check validation ratio
        if quality_scores['validation_ratio'] < 2.0:
            recommendations.append(
                "Validation ratio below 2:1. Increase supported claims or "
                "remove unsupported assertions."
            )
        
        # Check confidence distribution
        conf_dist = generation_assessment['confidence_distribution']
        if conf_dist.get('UNCERTAIN', 0) > conf_dist.get('HIGH', 0):
            recommendations.append(
                "More uncertain claims than high-confidence claims. "
                "Consider abstaining on uncertain topics."
            )
        
        # Check computational hardness
        if generation_assessment['computational_hardness']:
            recommendations.append(
                "Contains computationally hard claims. "
                "Acknowledge computational limitations explicitly."
            )
        
        # Check biases
        biases = quality_scores['bias_checks']
        if any(biases.values()):
            bias_types = [k.replace('_', ' ') for k, v in biases.items() if v]
            recommendations.append(
                f"Detected potential biases: {', '.join(bias_types)}. "
                "Review for balanced perspective."
            )
        
        # Check abstentions
        if not pre_validation['has_abstentions'] and quality_scores['singleton_rate'] > 0.1:
            recommendations.append(
                "Consider adding explicit uncertainty acknowledgments "
                "for low-confidence claims."
            )
        
        return recommendations
    
    def _generate_flags(self, pre_validation: Dict,
                       generation_assessment: Dict,
                       quality_scores: Dict) -> List[str]:
        """Generate validation flags for issues found"""
        flags = []
        
        if quality_scores['singleton_rate'] > 0.3:
            flags.append("HIGH_SINGLETON_RATE")
        
        if quality_scores['validation_ratio'] < 1.0:
            flags.append("POOR_VALIDATION_RATIO")
        
        if generation_assessment['unsupported_claims']:
            flags.append("UNSUPPORTED_CLAIMS")
        
        if generation_assessment['computational_hardness']:
            flags.append("COMPUTATIONAL_INTRACTABILITY")
        
        if not pre_validation['scope_defined']:
            flags.append("UNDEFINED_SCOPE")
        
        if pre_validation['ambiguity_score'] > 0.1:
            flags.append("HIGH_AMBIGUITY")
        
        if not pre_validation['has_abstentions'] and quality_scores['singleton_rate'] > 0.1:
            flags.append("MISSING_UNCERTAINTY_ACKNOWLEDGMENT")
        
        biases = quality_scores['bias_checks']
        if biases['confirmation_bias']:
            flags.append("CONFIRMATION_BIAS")
        if biases['recency_bias']:
            flags.append("RECENCY_BIAS")
        if biases['geographic_bias']:
            flags.append("GEOGRAPHIC_BIAS")
        
        return flags


def validate_output(content: str, metadata: Optional[Dict] = None) -> ValidationResult:
    """
    Convenience function to validate output
    
    Args:
        content: The output text to validate
        metadata: Optional metadata about sources, confidence, etc.
        
    Returns:
        ValidationResult with comprehensive analysis
    """
    validator = OutputValidator()
    return validator.validate_output(content, metadata)
