# Lithium - Validation Framework

A powerful, lightweight validation framework for detecting and preventing hallucinations in AI-generated content. Based on mathematical insights from "Why Language Models Hallucinate" (Kalai et al., 2025).

**Lithium: Stabilizing your outputs, reducing manic confidence swings.**

## Why Lithium?

Just as lithium stabilizes mood swings in psychiatry, the Lithium framework stabilizes AI outputs by:
- Detecting overconfident claims (manic assertions)
- Identifying unsupported statements (hallucinations)
- Balancing confidence levels appropriately
- Providing systematic validation and stabilization

## Quick Start

### MCP Integration (Recommended)

```bash
# Install Lithium
cd /Users/ged/Documents/brain/validation_system
chmod +x install_lithium.sh
./install_lithium.sh

# Add to Claude Desktop config, then restart Claude
```

Once installed, in any Claude chat:
- "Use Lithium to validate this text"
- "Check stability with Lithium"
- "Lithium risk assessment for: [text]"

### Command Line

```bash
# Quick validation
python validate.py --text "Your output text"

# With sources
python validate.py --file output.txt --sources source1.txt source2.txt

# Generate Lithium report
python validate.py --file output.txt --report markdown --verbose
```

### Python Integration

```python
from validation_interface import quick_check, ValidationInterface

# Quick Lithium check
result = quick_check("Your text here")
print(f"Lithium Score: {result['score']}%, Stability: {result['risk']}")

# Full Lithium validation
lithium = ValidationInterface()
result = lithium.full_validate("Your text", sources=["source1", "source2"])
```

## Core Features

### Three-Stage Validation Process

1. **Pre-Validation Check**
   - Claim classification (empirical/inferential/hypothetical/arbitrary)
   - Ambiguity detection
   - Scope verification
   - Singleton identification

2. **Output Generation Assessment**
   - Confidence distribution mapping
   - Support analysis
   - Cross-validation checking
   - Computational hardness detection

3. **Quality Assurance**
   - Singleton rate calculation
   - Validation ratio (2:1 rule)
   - Bias detection
   - Hallucination risk scoring

## Lithium MCP Tools

When integrated with Claude Desktop, Lithium provides 7 validation tools:

| Tool | Description | Use Case |
|------|-------------|----------|
| `lithium_validate` | General validation | Quick stability checks |
| `lithium_validate_context` | Domain-specific validation | Consulting, technical, research |
| `lithium_risk_check` | Hallucination risk assessment | Risk-focused analysis |
| `lithium_analyze_claims` | Individual claim validation | Fact-checking |
| `lithium_report` | Generate reports | Documentation |
| `lithium_compare` | Compare multiple versions | A/B testing |
| `lithium_stabilize` | Iterative improvement | Output refinement |

## Key Metrics

### Stability Score
- **80-100%**: Highly Stable ✓
- **60-79%**: Moderately Stable
- **Below 60%**: Unstable ⚠️

### Hallucination Risk
Based on the paper's formula: `err ≥ 2·erriiv - |Vc|/|Ec| - δ`
- **LOW**: < 20% risk score
- **MEDIUM**: 20-50% risk score  
- **HIGH**: > 50% risk score

### Singleton Rate
Fraction of claims appearing only once (no cross-validation)
- **Threshold**: < 20% for stable output

### Validation Ratio
Ratio of supported to unsupported claims
- **Target**: ≥ 2:1 for stability

## Configuration

Customize Lithium behavior in `config.json`:

```json
{
  "validation_settings": {
    "singleton_threshold": 0.2,
    "minimum_sources": 2,
    "passing_score": 0.7
  },
  "domain_specific_rules": {
    "consulting": {
      "require_mece": true,
      "min_confidence_for_recommendations": 0.75
    }
  }
}
```

## Usage Examples

### Stabilizing Consulting Output

```python
# Original unstable output
output = "All companies using this strategy succeed 100% of the time."

# Lithium validation
result = lithium.validate(output)
# Result: HIGH risk, 25% score, UNSTABLE

# After Lithium stabilization
stabilized = "60-80% of companies report positive outcomes, though results vary by implementation."
# Result: LOW risk, 85% score, STABLE
```

### Domain-Specific Validation

```python
# Technical domain validation
lithium.validate_with_context(
    content="System solves NP-hard problems in polynomial time",
    domain="technical"
)
# Flags: COMPUTATIONAL_INTRACTABILITY, UNREALISTIC_CLAIMS
```

## Installation

### Requirements
- Python 3.8+
- MCP package (for Claude integration)

### Setup
```bash
# Clone or navigate to directory
cd /Users/ged/Documents/brain/validation_system

# Install dependencies
pip install -r requirements.txt

# For MCP integration
./install_lithium.sh
```

## Theory Foundation

Lithium implements key findings from the hallucination paper:

1. **Error Lower Bound**: Generation errors ≥ 2 × classification error rate
2. **Singleton Correlation**: Hallucination rate ≥ singleton fact rate
3. **Confidence Thresholds**: Explicit targets reduce hallucinations
4. **Binary Grading Problem**: Most evaluations penalize uncertainty

## Project Structure

```
validation_system/
├── lithium_mcp_server.py    # MCP server for Claude integration
├── validation_engine.py      # Core validation logic
├── validation_interface.py   # User-friendly interface
├── validate.py              # CLI tool
├── config.json              # Configuration
├── install_lithium.sh       # Installation script
└── examples.py              # Usage examples
```

## Best Practices

1. **Always provide sources** for cross-validation
2. **Use domain-specific modes** when applicable
3. **Target 80%+ stability** for critical outputs
4. **Review Lithium recommendations** and iterate
5. **Track validation history** to identify patterns

## Contributing

Lithium is based on academic research and welcomes improvements:
- Enhanced claim extraction algorithms
- Additional domain-specific rules
- Improved bias detection
- Performance optimizations

## Citation

If using Lithium in research or production:

```
Lithium Validation Framework (2024)
Based on: Kalai, A.T., Vempala, S.S. et al. (2025). 
"Why Language Models Hallucinate." arXiv:2509.04664v1
```

## License

MIT License - Use freely with attribution.

---

**Lithium**: Because stable outputs matter. Reducing hallucinations through systematic validation.

*Stabilizing your AI, one validation at a time.*
