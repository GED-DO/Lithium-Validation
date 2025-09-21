#!/usr/bin/env python3
"""
MCP Server for Output Validation System
Based on "Why Language Models Hallucinate" paper insights

This server exposes validation tools that can be called directly from Claude
or other MCP-compatible clients.
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('validation-mcp')

class ValidationMCPServer:
    """MCP Server wrapper for the validation system"""
    
    def __init__(self):
        self.server = Server("validation-system")
        self.validator = ValidationInterface()
        self.cache = {}  # Simple cache for repeated validations
        self.config = self._load_config()
        
        # Setup handlers
        self._setup_handlers()
        
        logger.info("Validation MCP Server initialized")
    
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
            """Return list of available validation tools"""
            return [
                types.Tool(
                    name="validate_output",
                    description="Validate text for hallucination risk and quality issues. Returns score, risk level, and recommendations.",
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
                    name="validate_with_context",
                    description="Validate with specific domain context and configuration. Best for specialized content (consulting, technical, research).",
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
                    name="check_hallucination_risk",
                    description="Quick check specifically for hallucination risk. Returns risk level and singleton rate.",
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
                    name="validate_claims",
                    description="Extract and validate individual claims. Returns claim-by-claim analysis.",
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
                    name="get_validation_report",
                    description="Generate a formatted validation report (markdown or JSON).",
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
                    name="batch_validate",
                    description="Validate multiple outputs at once. Useful for comparing alternatives.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "contents": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of texts to validate"
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
                    name="improve_output",
                    description="Validate and provide specific improvement suggestions with examples.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "Text to improve"
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
                                "description": "Target validation score to achieve"
                            },
                            "max_iterations": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 5,
                                "default": 3,
                                "description": "Maximum improvement iterations"
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
            """Handle tool calls"""
            
            try:
                if name == "validate_output":
                    result = await self._validate_output(arguments)
                
                elif name == "validate_with_context":
                    result = await self._validate_with_context(arguments)
                
                elif name == "check_hallucination_risk":
                    result = await self._check_hallucination_risk(arguments)
                
                elif name == "validate_claims":
                    result = await self._validate_claims(arguments)
                
                elif name == "get_validation_report":
                    result = await self._get_validation_report(arguments)
                
                elif name == "batch_validate":
                    result = await self._batch_validate(arguments)
                
                elif name == "improve_output":
                    result = await self._improve_output(arguments)
                
                else:
                    result = f"Unknown tool: {name}"
                
                return [types.TextContent(
                    type="text",
                    text=result if isinstance(result, str) else json.dumps(result, indent=2)
                )]
                
            except Exception as e:
                logger.error(f"Error in {name}: {str(e)}")
                return [types.TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]
    
    async def _validate_output(self, args: dict) -> dict:
        """Handle validate_output tool"""
        content = args['content']
        sources = args.get('sources', [])
        mode = args.get('mode', 'quick')
        
        # Check cache
        cache_key = f"{hash(content)}_{hash(tuple(sources))}_{mode}"
        if cache_key in self.cache:
            logger.info("Returning cached result")
            return self.cache[cache_key]
        
        # Perform validation
        if mode == 'quick':
            result = self.validator.quick_validate(content, sources)
        else:
            val_result = self.validator.full_validate(content, sources)
            
            if mode == 'detailed':
                # Include detailed breakdown
                result = {
                    'score': round(val_result.overall_score * 100, 1),
                    'passed': val_result.passed,
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
                    'score': round(val_result.overall_score * 100, 1),
                    'passed': val_result.passed,
                    'risk': val_result.hallucination_risk,
                    'singleton_rate': round(val_result.singleton_rate * 100, 1),
                    'key_issues': val_result.validation_flags[:5],
                    'recommendations': val_result.recommendations[:3]
                }
        
        # Cache result
        self.cache[cache_key] = result
        
        return result
    
    async def _validate_with_context(self, args: dict) -> dict:
        """Handle validate_with_context tool"""
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
            'score': round(result.overall_score * 100, 1),
            'passed': result.passed and passed_threshold,
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
            'hallucination_risk': result.hallucination_risk,
            'risk_score': self._calculate_risk_score(result),
            'singleton_rate': round(result.singleton_rate * 100, 1),
            'unsupported_claims': unsupported,
            'total_claims': len(claims),
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
            'claims': analyzed_claims,
            'summary': {
                'total_claims': total,
                'supported_claims': supported,
                'unsupported_claims': total - supported,
                'support_ratio': round(supported / total * 100, 1) if total > 0 else 0
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
            return json.dumps(result.to_dict(), indent=2)
        
        elif format == 'markdown':
            report = self.validator.generate_report(result, 'markdown')
            if not include_recs:
                # Remove recommendations section
                lines = report.split('\n')
                filtered = []
                skip = False
                for line in lines:
                    if '## Recommendations' in line:
                        skip = True
                    elif skip and line.startswith('##'):
                        skip = False
                    if not skip:
                        filtered.append(line)
                report = '\n'.join(filtered)
            return report
        
        else:  # summary format
            summary = f"""**Validation Summary**

Score: {result.overall_score*100:.1f}%
Status: {'✅ PASSED' if result.passed else '❌ FAILED'}
Risk: {result.hallucination_risk}
Singleton Rate: {result.singleton_rate*100:.1f}%

**Key Issues:** {', '.join(result.validation_flags[:3]) if result.validation_flags else 'None'}
"""
            if include_recs and result.recommendations:
                summary += f"\n**Top Recommendation:** {result.recommendations[0]}"
            
            return summary
    
    async def _batch_validate(self, args: dict) -> dict:
        """Validate multiple outputs"""
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
                'passed': val_result['passed'],
                'risk': val_result['risk']
            })
        
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        
        output = {
            'results': results,
            'best_index': results[0]['index'] if results else None,
            'worst_index': results[-1]['index'] if results else None
        }
        
        if compare and len(results) > 1:
            # Add comparative analysis
            scores = [r['score'] for r in results]
            output['comparison'] = {
                'average_score': round(sum(scores) / len(scores), 1),
                'score_range': max(scores) - min(scores),
                'all_passed': all(r['passed'] for r in results),
                'risk_distribution': {
                    'LOW': sum(1 for r in results if r['risk'] == 'LOW'),
                    'MEDIUM': sum(1 for r in results if r['risk'] == 'MEDIUM'),
                    'HIGH': sum(1 for r in results if r['risk'] == 'HIGH')
                }
            }
        
        return output
    
    async def _improve_output(self, args: dict) -> dict:
        """Provide improvement suggestions"""
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
                'suggestions': suggestions
            })
            
            # Apply top suggestion (simulated)
            if suggestions:
                current_content = self._apply_suggestion(current_content, suggestions[0])
        
        # Final validation
        final_result = self.validator.full_validate(current_content, sources)
        
        return {
            'original_score': round(improvements[0]['score'], 1) if improvements else 100,
            'final_score': round(final_result.overall_score * 100, 1),
            'target_achieved': final_result.overall_score >= target_score,
            'iterations_used': len(improvements),
            'improvements': improvements,
            'final_recommendations': final_result.recommendations[:3]
        }
    
    # Helper methods
    def _calculate_validation_ratio(self, result: ValidationResult) -> float:
        """Calculate validation ratio from result"""
        # This would need access to internal metrics
        # Simplified calculation
        if result.singleton_rate > 0:
            return (1 - result.singleton_rate) / result.singleton_rate
        return 10.0  # High ratio if no singletons
    
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
        # Based on paper's formula
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
            return "Critical: Add source validation and explicit uncertainty acknowledgments"
        elif result.hallucination_risk == "MEDIUM":
            return "Moderate: Strengthen claim support and qualify uncertain statements"
        else:
            return "Low risk: Maintain current validation practices"
    
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
        # This is a simplified simulation
        # In practice, you'd want more sophisticated text modification
        
        if suggestion['type'] == 'add_uncertainty':
            # Add uncertainty phrase to first definitive claim
            import re
            content = re.sub(
                r'(\b(?:is|are|will|must)\b)',
                r'likely \1',
                content,
                count=1
            )
        
        elif suggestion['type'] == 'reduce_singletons':
            # Add validation phrase
            content = "Based on multiple sources, " + content
        
        return content
    
    async def run(self):
        """Run the MCP server"""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="validation-system",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )


async def main():
    """Main entry point"""
    server = ValidationMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
