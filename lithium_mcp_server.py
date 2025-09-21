#!/usr/bin/env python3
"""
Lithium - Validation Framework MCP Server
Based on "Why Language Models Hallucinate" paper insights

A lightweight, powerful validation framework for detecting and preventing
hallucinations in AI-generated content.

Lithium: Stabilizing your outputs, reducing manic confidence swings.
"""

import asyncio
import json
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Add validation system to path
sys.path.append(str(Path(__file__).parent))

# MCP imports
import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# Import our validation system
from validation_engine import OutputValidator, ValidationResult, ConfidenceLevel
from validation_interface import ValidationInterface

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - Lithium - %(levelname)s - %(message)s'
)
logger = logging.getLogger('lithium')

class LithiumMCPServer:
    """
    Lithium Validation Framework MCP Server
    Stabilizing outputs through systematic validation
    """
    
    def __init__(self):
        self.server = Server("lithium")
        self.validator = ValidationInterface()
        self.cache = {}  # Simple cache for repeated validations
        self.config = self._load_config()
        
        # Setup handlers
        self._setup_handlers()
        
        logger.info("Lithium Validation Framework initialized")
    
    def _load_config(self) -> Dict:
        """Load configuration from config.json"""
        config_path = Path(__file__).parent / "config.json"
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load config: {e}")
            return {}
    
    def _setup_handlers(self):
        """Setup all MCP handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            """Return list of available Lithium validation tools"""
            return [
                types.Tool(
                    name="lithium_validate",
                    description="[Lithium] Validate text for hallucination risk and quality issues. Returns score, risk level, and recommendations.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "The text content to validate"
                            },
                            "sources": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional source texts for cross-validation"
                            },
                            "mode": {
                                "type": "string",
                                "enum": ["quick", "full", "detailed"],
                                "default": "quick",
                                "description": "Validation mode: quick (fast), full (comprehensive), detailed (with examples)"
                            }
                        },
                        "required": ["content"]
                    }
                ),
                
                types.Tool(
                    name="lithium_validate_context",
                    description="[Lithium] Validate with specific domain context. Best for specialized content (consulting, technical, research).",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "The text content to validate"
                            },
                            "sources": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Source texts for validation"
                            },
                            "domain": {
                                "type": "string",
                                "enum": ["consulting", "technical", "research", "general"],
                                "default": "general",
                                "description": "Domain-specific rules to apply"
                            },
                            "scope": {
                                "type": "string",
                                "description": "Scope definition for the content"
                            },
                            "confidence_threshold": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": 1,
                                "default": 0.7,
                                "description": "Minimum confidence threshold (0-1)"
                            }
                        },
                        "required": ["content"]
                    }
                ),
                
                types.Tool(
                    name="lithium_risk_check",
                    description="[Lithium] Quick hallucination risk assessment. Returns risk level and singleton rate.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "Text to check for hallucination risk"
                            },
                            "sources": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Sources for fact-checking"
                            }
                        },
                        "required": ["content"]
                    }
                ),
                
                types.Tool(
                    name="lithium_analyze_claims",
                    description="[Lithium] Extract and validate individual claims. Returns claim-by-claim analysis.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "Text containing claims to validate"
                            },
                            "sources": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Sources to validate claims against"
                            },
                            "return_unsupported_only": {
                                "type": "boolean",
                                "default": False,
                                "description": "Only return unsupported claims"
                            }
                        },
                        "required": ["content"]
                    }
                ),
                
                types.Tool(
                    name="lithium_report",
                    description="[Lithium] Generate a formatted validation report (markdown or JSON).",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "Text to validate and report on"
                            },
                            "sources": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Sources for validation"
                            },
                            "format": {
                                "type": "string",
                                "enum": ["markdown", "json", "summary"],
                                "default": "summary",
                                "description": "Report format"
                            },
                            "include_recommendations": {
                                "type": "boolean",
                                "default": True,
                                "description": "Include improvement recommendations"
                            }
                        },
                        "required": ["content"]
                    }
                ),
                
                types.Tool(
                    name="lithium_compare",
                    description="[Lithium] Compare multiple text versions. Useful for A/B testing content.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "contents": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of texts to compare"
                            },
                            "sources": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Shared sources for all validations"
                            },
                            "compare": {
                                "type": "boolean",
                                "default": True,
                                "description": "Include comparative analysis"
                            }
                        },
                        "required": ["contents"]
                    }
                ),
                
                types.Tool(
                    name="lithium_stabilize",
                    description="[Lithium] Stabilize output by providing specific improvement suggestions.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "Text to stabilize"
                            },
                            "sources": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Sources for validation"
                            },
                            "target_score": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": 1,
                                "default": 0.8,
                                "description": "Target stability score to achieve"
                            },
                            "max_iterations": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 5,
                                "default": 3,
                                "description": "Maximum stabilization iterations"
                            }
                        },
                        "required": ["content"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str, 
            arguments: dict
        ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
            """Handle Lithium tool calls"""
            
            try:
                if name == "lithium_validate":
                    result = await self._validate_output(arguments)
                
                elif name == "lithium_validate_context":
                    result = await self._validate_with_context(arguments)
                
                elif name == "lithium_risk_check":
                    result = await self._check_hallucination_risk(arguments)
                
                elif name == "lithium_analyze_claims":
                    result = await self._validate_claims(arguments)
                
                elif name == "lithium_report":
                    result = await self._get_validation_report(arguments)
                
                elif name == "lithium_compare":
                    result = await self._batch_validate(arguments)
                
                elif name == "lithium_stabilize":
                    result = await self._improve_output(arguments)
                
                else:
                    result = f"Unknown Lithium tool: {name}"
                
                return [types.TextContent(
                    type="text",
                    text=result if isinstance(result, str) else json.dumps(result, indent=2)
                )]
                
            except Exception as e:
                logger.error(f"Error in {name}: {str(e)}")
                return [types.TextContent(
                    type="text",
                    text=f"Lithium Error: {str(e)}"
                )]
    
    async def _validate_output(self, args: dict) -> dict:
        """Handle lithium_validate tool"""
        content = args['content']
        sources = args.get('sources', [])
        mode = args.get('mode', 'quick')
        
        # Check cache
        cache_key = f"{hash(content)}_{hash(tuple(sources))}_{mode}"
        if cache_key in self.cache:
            logger.info("Returning cached Lithium result")
            result = self.cache[cache_key]
            result['cached'] = True
            return result
        
        # Perform validation
        if mode == 'quick':
            result = self.validator.quick_validate(content, sources)
            result['framework'] = 'Lithium'
        else:
            val_result = self.validator.full_validate(content, sources)
            
            if mode == 'detailed':
                # Include detailed breakdown
                result = {
                    'framework': 'Lithium - Detailed Analysis',
                    'score': round(val_result.overall_score * 100, 1),
                    'stability': 'STABLE' if val_result.passed else 'UNSTABLE',
                    'risk': val_result.hallucination_risk,
                    'singleton_rate': round(val_result.singleton_rate * 100, 1),
                    'confidence_distribution': val_result.confidence_distribution,
                    'issues': val_result.validation_flags,
                    'recommendations': val_result.recommendations,
                    'metrics': {
                        'total_claims': len(val_result.confidence_distribution),
                        'validation_ratio': self._calculate_validation_ratio(val_result)
                    }
                }
            else:
                # Standard full result
                result = {
                    'framework': 'Lithium',
                    'score': round(val_result.overall_score * 100, 1),
                    'stability': 'STABLE' if val_result.passed else 'UNSTABLE',
                    'risk': val_result.hallucination_risk,
                    'singleton_rate': round(val_result.singleton_rate * 100, 1),
                    'key_issues': val_result.validation_flags[:5],
                    'recommendations': val_result.recommendations[:3]
                }
        
        # Cache result
        self.cache[cache_key] = result
        
        return result
    
    async def _validate_with_context(self, args: dict) -> dict:
        """Handle lithium_validate_context tool"""
        content = args['content']
        sources = args.get('sources', [])
        domain = args.get('domain', 'general')
        scope = args.get('scope', '')
        threshold = args.get('confidence_threshold', 0.7)
        
        # Apply domain-specific configuration
        if domain in self.config.get('domain_specific_rules', {}):
            domain_rules = self.config['domain_specific_rules'][domain]
            # Adjust validator settings based on domain
            self.validator.validator.singleton_threshold = domain_rules.get(
                'singleton_threshold', 0.2
            )
            self.validator.validator.minimum_sources = domain_rules.get(
                'minimum_sources', 2
            )
        
        # Perform validation
        result = self.validator.full_validate(content, sources, scope, domain)
        
        # Apply threshold check
        passed_threshold = result.overall_score >= threshold
        
        return {
            'framework': 'Lithium Context-Aware',
            'score': round(result.overall_score * 100, 1),
            'stability': 'STABLE' if (result.passed and passed_threshold) else 'UNSTABLE',
            'domain': domain,
            'scope': scope,
            'risk': result.hallucination_risk,
            'singleton_rate': round(result.singleton_rate * 100, 1),
            'meets_threshold': passed_threshold,
            'threshold': threshold * 100,
            'domain_specific_flags': self._get_domain_flags(result, domain),
            'recommendations': result.recommendations
        }
    
    async def _check_hallucination_risk(self, args: dict) -> dict:
        """Quick hallucination risk check"""
        content = args['content']
        sources = args.get('sources', [])
        
        # Quick validation
        result = self.validator.full_validate(content, sources)
        
        # Calculate specific hallucination metrics
        claims = self._extract_claims(content)
        unsupported = self._count_unsupported_claims(claims, sources)
        
        return {
            'framework': 'Lithium Risk Assessment',
            'hallucination_risk': result.hallucination_risk,
            'risk_score': self._calculate_risk_score(result),
            'singleton_rate': round(result.singleton_rate * 100, 1),
            'unsupported_claims': unsupported,
            'total_claims': len(claims),
            'stability_level': self._get_stability_level(result),
            'confidence_breakdown': {
                'high': result.confidence_distribution.get('HIGH', 0),
                'medium': result.confidence_distribution.get('MEDIUM', 0),
                'low': result.confidence_distribution.get('LOW', 0),
                'uncertain': result.confidence_distribution.get('UNCERTAIN', 0)
            },
            'recommendation': self._get_risk_recommendation(result)
        }
    
    async def _validate_claims(self, args: dict) -> dict:
        """Validate individual claims"""
        content = args['content']
        sources = args.get('sources', [])
        unsupported_only = args.get('return_unsupported_only', False)
        
        # Extract and analyze claims
        claims = self._extract_claims(content)
        analyzed_claims = []
        
        for claim in claims:
            support_count = self._count_support(claim, sources)
            confidence = self._assess_confidence(claim, support_count)
            
            claim_analysis = {
                'claim': claim,
                'supported': support_count > 0,
                'support_count': support_count,
                'confidence': confidence,
                'type': self._classify_claim(claim)
            }
            
            if not unsupported_only or not claim_analysis['supported']:
                analyzed_claims.append(claim_analysis)
        
        # Summary statistics
        total = len(claims)
        supported = sum(1 for c in analyzed_claims if c['supported'])
        
        return {
            'framework': 'Lithium Claim Analysis',
            'claims': analyzed_claims,
            'summary': {
                'total_claims': total,
                'supported_claims': supported,
                'unsupported_claims': total - supported,
                'support_ratio': round(supported / total * 100, 1) if total > 0 else 0,
                'stability': 'STABLE' if supported / total >= 0.67 else 'UNSTABLE'
            }
        }
    
    async def _get_validation_report(self, args: dict) -> str:
        """Generate formatted validation report"""
        content = args['content']
        sources = args.get('sources', [])
        format = args.get('format', 'summary')
        include_recs = args.get('include_recommendations', True)
        
        # Perform full validation
        result = self.validator.full_validate(content, sources)
        
        if format == 'json':
            report_dict = result.to_dict()
            report_dict['framework'] = 'Lithium Validation Framework'
            return json.dumps(report_dict, indent=2)
        
        elif format == 'markdown':
            report = f"""# Lithium Validation Report

**Framework:** Lithium - Validation Framework  
**Generated:** {result.timestamp}  
**Score:** {result.overall_score*100:.1f}%  
**Stability:** {'🟢 STABLE' if result.passed else '🔴 UNSTABLE'}  
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
            
            if include_recs and result.recommendations:
                report += "\n## Stabilization Recommendations\n\n"
                for i, rec in enumerate(result.recommendations, 1):
                    report += f"{i}. {rec}\n"
            
            return report
        
        else:  # summary format
            summary = f"""**Lithium Validation Summary**

Framework: Lithium
Score: {result.overall_score*100:.1f}%
Stability: {'STABLE ✓' if result.passed else 'UNSTABLE ⚠️'}
Risk: {result.hallucination_risk}
Singleton Rate: {result.singleton_rate*100:.1f}%

**Key Issues:** {', '.join(result.validation_flags[:3]) if result.validation_flags else 'None detected'}
"""
            if include_recs and result.recommendations:
                summary += f"\n**Primary Recommendation:** {result.recommendations[0]}"
            
            return summary
    
    async def _batch_validate(self, args: dict) -> dict:
        """Validate multiple outputs (lithium_compare)"""
        contents = args['contents']
        sources = args.get('sources', [])
        compare = args.get('compare', True)
        
        # Validate each content
        results = []
        for i, content in enumerate(contents):
            val_result = self.validator.quick_validate(content, sources)
            results.append({
                'index': i,
                'content_preview': content[:100] + '...' if len(content) > 100 else content,
                'score': val_result['score'],
                'stability': 'STABLE' if val_result['passed'] else 'UNSTABLE',
                'risk': val_result['risk']
            })
        
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        
        output = {
            'framework': 'Lithium Comparison',
            'results': results,
            'most_stable_index': results[0]['index'] if results else None,
            'least_stable_index': results[-1]['index'] if results else None
        }
        
        if compare and len(results) > 1:
            # Add comparative analysis
            scores = [r['score'] for r in results]
            output['comparison'] = {
                'average_score': round(sum(scores) / len(scores), 1),
                'score_range': max(scores) - min(scores),
                'all_stable': all(r['stability'] == 'STABLE' for r in results),
                'risk_distribution': {
                    'LOW': sum(1 for r in results if r['risk'] == 'LOW'),
                    'MEDIUM': sum(1 for r in results if r['risk'] == 'MEDIUM'),
                    'HIGH': sum(1 for r in results if r['risk'] == 'HIGH')
                }
            }
        
        return output
    
    async def _improve_output(self, args: dict) -> dict:
        """Stabilize output (lithium_stabilize)"""
        content = args['content']
        sources = args.get('sources', [])
        target_score = args.get('target_score', 0.8)
        max_iterations = args.get('max_iterations', 3)
        
        improvements = []
        current_content = content
        
        for iteration in range(max_iterations):
            # Validate current version
            result = self.validator.full_validate(current_content, sources)
            
            if result.overall_score >= target_score:
                break
            
            # Generate improvement suggestions
            suggestions = self._generate_improvements(result, current_content)
            improvements.append({
                'iteration': iteration + 1,
                'score': round(result.overall_score * 100, 1),
                'stability': 'STABLE' if result.passed else 'UNSTABLE',
                'suggestions': suggestions
            })
            
            # Apply top suggestion (simulated)
            if suggestions:
                current_content = self._apply_suggestion(current_content, suggestions[0])
        
        # Final validation
        final_result = self.validator.full_validate(current_content, sources)
        
        return {
            'framework': 'Lithium Stabilization',
            'original_score': round(improvements[0]['score'], 1) if improvements else 100,
            'final_score': round(final_result.overall_score * 100, 1),
            'stability_achieved': final_result.overall_score >= target_score,
            'final_stability': 'STABLE' if final_result.passed else 'UNSTABLE',
            'iterations_used': len(improvements),
            'stabilization_path': improvements,
            'final_recommendations': final_result.recommendations[:3]
        }
    
    # Helper methods
    def _calculate_validation_ratio(self, result: ValidationResult) -> float:
        """Calculate validation ratio from result"""
        if result.singleton_rate > 0:
            return (1 - result.singleton_rate) / result.singleton_rate
        return 10.0  # High ratio if no singletons
    
    def _get_stability_level(self, result: ValidationResult) -> str:
        """Determine stability level"""
        if result.overall_score >= 0.8 and result.hallucination_risk == "LOW":
            return "HIGHLY STABLE"
        elif result.overall_score >= 0.6 and result.hallucination_risk != "HIGH":
            return "MODERATELY STABLE"
        else:
            return "UNSTABLE"
    
    def _get_domain_flags(self, result: ValidationResult, domain: str) -> List[str]:
        """Get domain-specific validation flags"""
        flags = []
        
        if domain == 'consulting':
            if 'MISSING_UNCERTAINTY_ACKNOWLEDGMENT' in result.validation_flags:
                flags.append('LACKS_EXECUTIVE_CONFIDENCE_FRAMING')
            if 'HIGH_SINGLETON_RATE' in result.validation_flags:
                flags.append('INSUFFICIENT_MARKET_VALIDATION')
        
        elif domain == 'technical':
            if 'COMPUTATIONAL_INTRACTABILITY' in result.validation_flags:
                flags.append('UNREALISTIC_PERFORMANCE_CLAIMS')
            if 'UNSUPPORTED_CLAIMS' in result.validation_flags:
                flags.append('MISSING_TECHNICAL_CITATIONS')
        
        elif domain == 'research':
            if 'HIGH_SINGLETON_RATE' in result.validation_flags:
                flags.append('NEEDS_PEER_REVIEW')
            if 'CONFIRMATION_BIAS' in result.validation_flags:
                flags.append('LACKS_ALTERNATIVE_HYPOTHESES')
        
        return flags
    
    def _extract_claims(self, content: str) -> List[str]:
        """Extract individual claims from content"""
        import re
        sentences = re.split(r'[.!?]+', content)
        return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
    
    def _count_unsupported_claims(self, claims: List[str], sources: List[str]) -> int:
        """Count claims without support"""
        unsupported = 0
        for claim in claims:
            if not any(self._claim_in_source(claim, source) for source in sources):
                unsupported += 1
        return unsupported
    
    def _claim_in_source(self, claim: str, source: str) -> bool:
        """Check if claim appears in source"""
        key_words = [w for w in claim.lower().split() 
                    if len(w) > 4 and w not in ['that', 'this', 'with', 'from', 'have', 'been']]
        
        if len(key_words) < 2:
            return False
        
        matches = sum(1 for word in key_words if word in source.lower())
        return matches >= len(key_words) * 0.5
    
    def _count_support(self, claim: str, sources: List[str]) -> int:
        """Count how many sources support a claim"""
        return sum(1 for source in sources if self._claim_in_source(claim, source))
    
    def _assess_confidence(self, claim: str, support_count: int) -> str:
        """Assess confidence level for a claim"""
        if support_count >= 3:
            return "HIGH"
        elif support_count >= 2:
            return "MEDIUM"
        elif support_count >= 1:
            return "LOW"
        else:
            return "UNCERTAIN"
    
    def _classify_claim(self, claim: str) -> str:
        """Classify the type of claim"""
        claim_lower = claim.lower()
        
        if any(word in claim_lower for word in ['data shows', 'evidence', 'study']):
            return "empirical"
        elif any(word in claim_lower for word in ['therefore', 'thus', 'implies']):
            return "inferential"
        elif any(word in claim_lower for word in ['might', 'could', 'possibly']):
            return "hypothetical"
        else:
            return "arbitrary"
    
    def _calculate_risk_score(self, result: ValidationResult) -> float:
        """Calculate numerical risk score"""
        risk = (
            result.singleton_rate * 0.4 +
            (1 - result.overall_score) * 0.3 +
            (0.3 if result.hallucination_risk == "HIGH" else 
             0.15 if result.hallucination_risk == "MEDIUM" else 0)
        )
        return round(min(1.0, risk) * 100, 1)
    
    def _get_risk_recommendation(self, result: ValidationResult) -> str:
        """Get risk-specific recommendation"""
        if result.hallucination_risk == "HIGH":
            return "Critical: Immediate stabilization needed - add sources and uncertainty acknowledgments"
        elif result.hallucination_risk == "MEDIUM":
            return "Moderate: Strengthen claim support and qualify uncertain statements"
        else:
            return "Low risk: Output is stable - maintain current validation practices"
    
    def _generate_improvements(self, result: ValidationResult, content: str) -> List[Dict]:
        """Generate specific improvement suggestions"""
        suggestions = []
        
        if result.singleton_rate > 0.2:
            suggestions.append({
                'type': 'reduce_singletons',
                'priority': 'high',
                'suggestion': 'Add cross-validation: Include "multiple sources confirm" or "consistently observed"',
                'example': 'Replace "X is true" with "Multiple studies confirm X"'
            })
        
        if 'MISSING_UNCERTAINTY_ACKNOWLEDGMENT' in result.validation_flags:
            suggestions.append({
                'type': 'add_uncertainty',
                'priority': 'high',
                'suggestion': 'Add uncertainty qualifiers where confidence is low',
                'example': 'Add "preliminary data suggests" or "further research needed"'
            })
        
        if 'CONFIRMATION_BIAS' in result.validation_flags:
            suggestions.append({
                'type': 'balance_perspective',
                'priority': 'medium',
                'suggestion': 'Include alternative viewpoints or caveats',
                'example': 'Add "while X is common, exceptions include Y"'
            })
        
        return suggestions
    
    def _apply_suggestion(self, content: str, suggestion: Dict) -> str:
        """Apply improvement suggestion to content (simulated)"""
        import re
        
        if suggestion['type'] == 'add_uncertainty':
            content = re.sub(
                r'(\b(?:is|are|will|must)\b)',
                r'likely \1',
                content,
                count=1
            )
        
        elif suggestion['type'] == 'reduce_singletons':
            content = "Based on multiple sources, " + content
        
        return content
    
    async def run(self):
        """Run the Lithium MCP server"""
        logger.info("Starting Lithium Validation Framework MCP Server...")
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="Lithium Validation Framework",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )


async def main():
    """Main entry point for Lithium"""
    print("""
    ╔══════════════════════════════════════╗
    ║   Lithium - Validation Framework     ║
    ║   Stabilizing AI-generated content   ║
    ╚══════════════════════════════════════╝
    
    Starting server...
    """)
    server = LithiumMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
