#!/usr/bin/env python3
"""
Lithium Auto-Validator Module
Intelligent content detection and automatic validation selection
"""

import re
from typing import Dict, List, Optional, Tuple
from enum import Enum

class ContentType(Enum):
    """Auto-detected content types"""
    CONSULTING = "consulting"
    TECHNICAL = "technical"
    RESEARCH = "research"
    CREATIVE = "creative"
    FACTUAL = "factual"
    ANALYSIS = "analysis"
    RECOMMENDATION = "recommendation"
    GENERAL = "general"

class ValidationMode(Enum):
    """Validation modes based on risk level"""
    STRICT = "strict"      # High-stakes content
    BALANCED = "balanced"  # Normal content
    PERMISSIVE = "permissive"  # Creative/exploratory content

class AutoValidator:
    """Intelligent content analyzer and validator"""
    
    def __init__(self):
        self.enabled = True  # Master on/off switch
        
        # Detection patterns for content type
        self.content_patterns = {
            ContentType.CONSULTING: [
                r'\b(ROI|market analysis|strategy|recommendation|MECE|framework|hypothesis)\b',
                r'\b(stakeholder|implementation|phased approach|risk assessment)\b',
                r'\b(executive summary|key findings|action items)\b'
            ],
            ContentType.TECHNICAL: [
                r'\b(algorithm|code|API|database|system|architecture|performance)\b',
                r'\b(bug|error|debug|compile|runtime|optimization)\b',
                r'\b(function|method|class|variable|parameter)\b'
            ],
            ContentType.RESEARCH: [
                r'\b(study|research|findings|methodology|hypothesis|conclusion)\b',
                r'\b(data shows|evidence|statistical|correlation|causation)\b',
                r'\b(peer-reviewed|citation|reference|literature)\b'
            ],
            ContentType.CREATIVE: [
                r'\b(story|narrative|character|plot|theme|metaphor)\b',
                r'\b(imagine|create|design|artistic|aesthetic)\b',
                r'\b(poem|prose|fiction|creative writing)\b'
            ],
            ContentType.FACTUAL: [
                r'\b(fact|date|number|percentage|statistic|measurement)\b',
                r'\b(historically|currently|according to|source states)\b',
                r'\b(definition|explanation|describes?|means?)\b'
            ],
            ContentType.ANALYSIS: [
                r'\b(analyze|analysis|evaluate|assessment|examination)\b',
                r'\b(compare|contrast|relationship|pattern|trend)\b',
                r'\b(insight|observation|interpretation|implication)\b'
            ],
            ContentType.RECOMMENDATION: [
                r'\b(recommend|suggest|should|must|need to|ought to)\b',
                r'\b(best practice|optimal|ideal|preferred approach)\b',
                r'\b(action plan|next steps|implementation|roadmap)\b'
            ]
        }
        
        # Risk indicators for automatic strictness
        self.risk_patterns = {
            'high_risk': [
                r'\b(guarantee|definitely|certainly|always|never|100%|impossible)\b',
                r'\b(will succeed|will fail|must happen|cannot fail)\b',
                r'\b(proven fact|undeniable|absolute truth)\b'
            ],
            'medium_risk': [
                r'\b(likely|probably|typically|usually|generally|mostly)\b',
                r'\b(should work|expect|anticipate|project)\b',
                r'\b(evidence suggests|data indicates|trends show)\b'
            ],
            'low_risk': [
                r'\b(might|could|possibly|perhaps|maybe|uncertain)\b',
                r'\b(preliminary|subject to change|approximate|estimated)\b',
                r'\b(further research|more data needed|limitations)\b'
            ]
        }
    
    def detect_content_type(self, content: str) -> Tuple[ContentType, float]:
        """Automatically detect the type of content"""
        content_lower = content.lower()
        scores = {}
        
        # Score each content type
        for content_type, patterns in self.content_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, content_lower, re.IGNORECASE))
                score += matches
            scores[content_type] = score
        
        # Get the highest scoring type
        if scores:
            best_type = max(scores, key=scores.get)
            confidence = scores[best_type] / (sum(scores.values()) + 1)
            
            # If confidence is too low, default to general
            if confidence < 0.3:
                return ContentType.GENERAL, confidence
            return best_type, confidence
        
        return ContentType.GENERAL, 0.0
    
    def detect_risk_level(self, content: str) -> str:
        """Detect the risk level of claims in the content"""
        content_lower = content.lower()
        
        # Count risk indicators
        high_risk_count = sum(
            len(re.findall(pattern, content_lower, re.IGNORECASE))
            for pattern in self.risk_patterns['high_risk']
        )
        medium_risk_count = sum(
            len(re.findall(pattern, content_lower, re.IGNORECASE))
            for pattern in self.risk_patterns['medium_risk']
        )
        low_risk_count = sum(
            len(re.findall(pattern, content_lower, re.IGNORECASE))
            for pattern in self.risk_patterns['low_risk']
        )
        
        # Determine overall risk
        if high_risk_count > 2:
            return "HIGH"
        elif high_risk_count > 0 or medium_risk_count > 3:
            return "MEDIUM"
        else:
            return "LOW"
    
    def detect_validation_mode(self, content: str, content_type: ContentType) -> ValidationMode:
        """Determine how strict validation should be"""
        risk_level = self.detect_risk_level(content)
        
        # Creative content gets more permissive validation
        if content_type == ContentType.CREATIVE:
            return ValidationMode.PERMISSIVE
        
        # High-risk content gets strict validation
        if risk_level == "HIGH":
            return ValidationMode.STRICT
        
        # Consulting and recommendations need balanced validation
        if content_type in [ContentType.CONSULTING, ContentType.RECOMMENDATION]:
            return ValidationMode.BALANCED if risk_level == "MEDIUM" else ValidationMode.STRICT
        
        # Technical and research content needs strict validation
        if content_type in [ContentType.TECHNICAL, ContentType.RESEARCH]:
            return ValidationMode.STRICT if risk_level in ["HIGH", "MEDIUM"] else ValidationMode.BALANCED
        
        # Default to balanced
        return ValidationMode.BALANCED
    
    def extract_sources_from_content(self, content: str) -> List[str]:
        """Automatically extract potential sources from content"""
        sources = []
        
        # Look for quoted text that might be sources
        quotes = re.findall(r'"([^"]+)"', content)
        sources.extend([q for q in quotes if len(q) > 50])
        
        # Look for references to data or studies
        data_refs = re.findall(r'(?:data shows?|study finds?|research indicates?|according to)[^.]+\.', 
                               content, re.IGNORECASE)
        sources.extend(data_refs)
        
        return sources[:5]  # Limit to 5 sources
    
    def get_auto_validation_params(self, content: str) -> Dict:
        """
        Get automatic validation parameters based on content analysis
        Returns everything needed for validation without user input
        """
        # Detect content characteristics
        content_type, type_confidence = self.detect_content_type(content)
        risk_level = self.detect_risk_level(content)
        validation_mode = self.detect_validation_mode(content, content_type)
        sources = self.extract_sources_from_content(content)
        
        # Set parameters based on detected mode
        if validation_mode == ValidationMode.STRICT:
            params = {
                'threshold': 0.8,
                'min_sources': 3,
                'domain': content_type.value,
                'mode': 'full'
            }
        elif validation_mode == ValidationMode.BALANCED:
            params = {
                'threshold': 0.7,
                'min_sources': 2,
                'domain': content_type.value,
                'mode': 'balanced'
            }
        else:  # PERMISSIVE
            params = {
                'threshold': 0.6,
                'min_sources': 1,
                'domain': 'general',
                'mode': 'quick'
            }
        
        return {
            'content_type': content_type.value,
            'risk_level': risk_level,
            'validation_mode': validation_mode.value,
            'type_confidence': round(type_confidence, 2),
            'sources': sources,
            'params': params,
            'auto_detected': True
        }
    
    def should_validate(self, content: str) -> bool:
        """Determine if content should be validated"""
        if not self.enabled:
            return False
        
        # Skip very short content
        if len(content) < 100:
            return False
        
        # Skip pure code blocks
        if content.strip().startswith('```') and content.strip().endswith('```'):
            return False
        
        # Skip content that's mostly numbers/data
        alphanum_ratio = len(re.findall(r'[a-zA-Z]', content)) / (len(content) + 1)
        if alphanum_ratio < 0.3:
            return False
        
        return True
    
    def make_auto_decision(self, score: float, risk_level: str) -> Dict:
        """Make an automatic decision about the content"""
        if score >= 80:
            return {
                'action': 'APPROVE',
                'confidence': 'HIGH',
                'message': '✅ Content is well-validated and ready to use',
                'color': 'green'
            }
        elif score >= 70 and risk_level == "LOW":
            return {
                'action': 'APPROVE_WITH_NOTES',
                'confidence': 'MEDIUM',
                'message': '⚠️ Content is acceptable with minor considerations',
                'color': 'yellow'
            }
        elif score >= 60 and risk_level != "HIGH":
            return {
                'action': 'REVIEW',
                'confidence': 'LOW',
                'message': '🔍 Content needs review before use',
                'color': 'orange'
            }
        else:
            return {
                'action': 'REVISE',
                'confidence': 'LOW',
                'message': '❌ Content requires significant revision',
                'color': 'red'
            }
