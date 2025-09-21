# Validation System MCP Integration

Complete Model Context Protocol (MCP) server for the output validation system, enabling direct validation within Claude and other MCP-compatible environments.

## Features

### 7 Validation Tools Available:

1. **`validate_output`** - General validation with quick/full/detailed modes
2. **`validate_with_context`** - Domain-specific validation (consulting, technical, research)
3. **`check_hallucination_risk`** - Quick hallucination risk assessment
4. **`validate_claims`** - Individual claim extraction and validation
5. **`get_validation_report`** - Generate formatted reports (markdown/JSON/summary)
6. **`batch_validate`** - Compare multiple outputs simultaneously  
7. **`improve_output`** - Iterative improvement suggestions

## Installation

### Quick Setup

1. **Install dependencies:**
```bash
cd /Users/ged/Documents/brain/validation_system
pip3 install mcp
```

2. **Make installation script executable:**
```bash
chmod +x install_mcp.sh
```

3. **Run installation:**
```bash
./install_mcp.sh
```

### Manual Setup

1. **Add to Claude Desktop configuration:**

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "validation-system": {
      "command": "python3",
      "args": [
        "/Users/ged/Documents/brain/validation_system/validation_mcp_server.py"
      ],
      "env": {}
    }
  }
}
```

2. **Restart Claude Desktop**

## Usage Examples

### In Claude Chat

Once installed, you can use natural language or direct tool calls:

#### Natural Language Usage:
```
"Validate this output for hallucination risk: [your text]"
"Check if this consulting recommendation passes validation: [your text]"
"Compare these three versions and tell me which is best: [version1], [version2], [version3]"
```

#### Direct Tool Calls:
```
Use the validate_output tool to check this text with sources: 
- Content: "Market analysis shows 100% success rate"
- Sources: ["Studies show 60-80% success rate", "Results vary by market"]
```

### Tool Descriptions

#### 1. validate_output
Basic validation with configurable detail level.

**Parameters:**
- `content` (required): Text to validate
- `sources`: List of source texts for cross-validation
- `mode`: "quick" | "full" | "detailed"

**Returns:**
```json
{
  "score": 75.5,
  "passed": true,
  "risk": "LOW",
  "singleton_rate": 15.2,
  "key_issues": ["HIGH_AMBIGUITY"],
  "recommendations": ["Add specific data sources"]
}
```

#### 2. validate_with_context
Domain-aware validation with specialized rules.

**Parameters:**
- `content` (required): Text to validate
- `sources`: Source texts
- `domain`: "consulting" | "technical" | "research" | "general"
- `scope`: Scope definition
- `confidence_threshold`: Minimum passing score (0-1)

**Returns:**
```json
{
  "score": 82.3,
  "passed": true,
  "domain": "consulting",
  "risk": "LOW",
  "domain_specific_flags": ["NEEDS_EXECUTIVE_SUMMARY"],
  "meets_threshold": true
}
```

#### 3. check_hallucination_risk
Quick hallucination-specific check.

**Parameters:**
- `content` (required): Text to check
- `sources`: Sources for fact-checking

**Returns:**
```json
{
  "hallucination_risk": "MEDIUM",
  "risk_score": 42.5,
  "singleton_rate": 25.0,
  "unsupported_claims": 3,
  "total_claims": 12,
  "confidence_breakdown": {
    "high": 2,
    "medium": 5,
    "low": 3,
    "uncertain": 2
  },
  "recommendation": "Strengthen claim support"
}
```

#### 4. validate_claims
Extract and analyze individual claims.

**Parameters:**
- `content` (required): Text with claims
- `sources`: Validation sources
- `return_unsupported_only`: Boolean

**Returns:**
```json
{
  "claims": [
    {
      "claim": "Revenue increased by 50%",
      "supported": true,
      "support_count": 2,
      "confidence": "MEDIUM",
      "type": "empirical"
    }
  ],
  "summary": {
    "total_claims": 5,
    "supported_claims": 3,
    "unsupported_claims": 2,
    "support_ratio": 60.0
  }
}
```

#### 5. get_validation_report
Generate formatted validation reports.

**Parameters:**
- `content` (required): Text to validate
- `sources`: Sources
- `format`: "markdown" | "json" | "summary"
- `include_recommendations`: Boolean

**Returns:** Formatted report string

#### 6. batch_validate
Compare multiple text versions.

**Parameters:**
- `contents` (required): List of texts
- `sources`: Shared validation sources
- `compare`: Include comparative analysis

**Returns:**
```json
{
  "results": [...],
  "best_index": 0,
  "worst_index": 2,
  "comparison": {
    "average_score": 72.5,
    "score_range": 25.0,
    "all_passed": false
  }
}
```

#### 7. improve_output
Iterative improvement suggestions.

**Parameters:**
- `content` (required): Text to improve
- `sources`: Sources
- `target_score`: Target validation score (0-1)
- `max_iterations`: Maximum improvement cycles

**Returns:**
```json
{
  "original_score": 65.0,
  "final_score": 85.5,
  "target_achieved": true,
  "iterations_used": 2,
  "improvements": [
    {
      "iteration": 1,
      "score": 65.0,
      "suggestions": [
        {
          "type": "add_uncertainty",
          "priority": "high",
          "suggestion": "Add confidence qualifiers",
          "example": "Replace 'will' with 'likely will'"
        }
      ]
    }
  ]
}
```

## Advanced Features

### Caching
The MCP server includes intelligent caching to avoid re-validating identical content.

### Domain-Specific Rules
Automatically applies specialized validation based on domain:

**Consulting:**
- Requires MECE structure
- Hypothesis validation
- Executive confidence framing

**Technical:**
- Citation requirements
- Computational feasibility checks
- Version compatibility

**Research:**
- Lower singleton threshold (10%)
- Minimum 3 sources
- Methodology requirements

### Error Handling
Comprehensive error handling with informative messages for:
- Invalid inputs
- Missing parameters
- Processing failures

## Integration Patterns

### Pattern 1: Pre-Publication Check
```
Before publishing any report:
1. Use validate_with_context with domain="consulting"
2. If score < 80%, use improve_output
3. Generate final report with get_validation_report
```

### Pattern 2: A/B Testing
```
When choosing between options:
1. Use batch_validate with all versions
2. Review comparative analysis
3. Select highest scoring version
```

### Pattern 3: Iterative Refinement
```
For critical outputs:
1. Initial validate_output with mode="detailed"
2. Apply recommendations
3. Use improve_output with target_score=0.9
4. Final validation with full sources
```

## Troubleshooting

### Server Not Starting
1. Check Python version (3.8+ required)
2. Verify MCP package installed: `pip3 list | grep mcp`
3. Check file permissions: `chmod +x validation_mcp_server.py`

### Tools Not Appearing
1. Restart Claude Desktop
2. Check configuration file syntax
3. Verify path to validation_mcp_server.py is absolute

### Validation Errors
1. Ensure content is string format
2. Sources should be list of strings
3. Check domain values are valid

## Performance Notes

- Quick validation: ~100ms
- Full validation: ~500ms
- Batch validation: ~200ms per item
- Report generation: ~300ms

Cache hits reduce time by ~90%.

## Best Practices

1. **Always provide sources** for better validation accuracy
2. **Use domain-specific validation** when applicable
3. **Start with quick mode** for rapid iteration
4. **Cache warmup** by validating common templates
5. **Batch similar content** for efficiency

## Updates and Maintenance

The validation rules and thresholds can be adjusted in `config.json`:
- Singleton threshold
- Confidence weights
- Domain-specific rules
- Abstention phrases

No server restart needed for config changes.

## Security Notes

- Server runs locally only
- No data transmitted externally
- Cache stored in memory only
- No persistent storage of validated content

## Support

For issues or enhancements:
1. Check logs in terminal where MCP server runs
2. Review validation_engine.py for rule details
3. Modify config.json for threshold adjustments
