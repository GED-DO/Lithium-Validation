# Output Validation System

A comprehensive validation framework for checking output quality and hallucination risk, based on insights from "Why Language Models Hallucinate" (Kalai et al., 2025).

## Overview

This validation system implements a three-stage process to evaluate outputs for:
- **Hallucination risk** - Identifying unsupported or singleton claims
- **Confidence distribution** - Assessing the balance of certain vs uncertain statements
- **Quality issues** - Detecting biases, ambiguities, and structural problems

## Quick Start

### Basic Command Line Usage

```bash
# Quick validate text
python validate.py --text "Your output text here"

# Validate a file
python validate.py --file report.txt

# Validate with source checking
python validate.py --file output.txt --sources source1.txt source2.txt

# Generate detailed report
python validate.py --file output.txt --report markdown --verbose
```

### Python Usage

```python
from validation_interface import quick_check, validate_with_sources

# Quick validation
result = quick_check("Your output text")
print(f"Score: {result['score']}%, Risk: {result['risk']}")

# Validation with sources
sources = ["Source text 1", "Source text 2"]
result = validate_with_sources("Your output", sources)
```

## Three-Stage Validation Process

### Stage 1: Pre-Validation Check
- **Claim Classification**: Categorizes claims as empirical, inferential, hypothetical, or arbitrary
- **Ambiguity Detection**: Identifies vague or uncertain language
- **Scope Verification**: Ensures boundaries and constraints are defined
- **Singleton Identification**: Finds claims that appear only once in sources

### Stage 2: Output Generation Assessment
- **Confidence Distribution**: Maps claims to confidence levels (High/Medium/Low/Uncertain)
- **Support Analysis**: Checks if claims are backed by sources
- **Cross-Validation**: Identifies which claims appear in multiple sources
- **Computational Hardness**: Flags computationally intractable claims

### Stage 3: Quality Assurance
- **Singleton Rate Calculation**: Measures percentage of unsupported unique claims
- **Validation Ratio**: Ensures 2:1 ratio of validated to unvalidated claims
- **Bias Detection**: Checks for confirmation, recency, and geographic biases
- **Hallucination Risk Score**: Calculates overall risk based on paper's formulas

## Key Metrics

### Singleton Rate (sr)
The fraction of claims that appear only once or have no cross-validation. Based on the paper's finding that hallucination rate ≥ singleton rate.

**Threshold**: < 20% for passing

### Validation Ratio
The ratio of supported to unsupported claims. The paper suggests a 2:1 minimum ratio.

**Threshold**: ≥ 2.0 for passing

### Confidence-Weighted Score
Weighted average of claim confidence levels:
- High confidence (t=0.9): Weight 1.0
- Medium confidence (t=0.75): Weight 0.75  
- Low confidence (t=0.5): Weight 0.5
- Uncertain: Weight 0.0

### Overall Score
Composite score combining:
- Pre-validation (30%)
- Generation assessment (40%)
- Quality assurance (30%)

**Passing threshold**: ≥ 70%

## Configuration

Edit `config.json` to customize:
- Validation thresholds
- Confidence weights
- Domain-specific rules
- Bias detection settings
- Abstention phrases

### Domain-Specific Rules

```json
"consulting": {
  "require_mece": true,
  "require_hypothesis": true,
  "min_confidence_for_recommendations": 0.75
}
```

## Validation Flags

The system generates flags for issues found:

- `HIGH_SINGLETON_RATE`: Too many unsupported unique claims
- `POOR_VALIDATION_RATIO`: Insufficient cross-validated claims
- `UNSUPPORTED_CLAIMS`: Claims without source backing
- `COMPUTATIONAL_INTRACTABILITY`: Claims requiring impossible computation
- `UNDEFINED_SCOPE`: Missing boundaries or constraints
- `HIGH_AMBIGUITY`: Excessive uncertain language
- `MISSING_UNCERTAINTY_ACKNOWLEDGMENT`: No abstentions despite low confidence
- `CONFIRMATION_BIAS`: One-sided or absolute claims
- `RECENCY_BIAS`: Overemphasis on newest information
- `GEOGRAPHIC_BIAS`: Regional perspective imbalance

## Report Formats

### Markdown Report
Comprehensive report with:
- Overall score and status
- Confidence distribution breakdown
- Key metrics visualization
- Issues and recommendations
- Detailed analysis

### JSON Report
Structured data for programmatic use:
```json
{
  "overall_score": 0.75,
  "passed": true,
  "hallucination_risk": "LOW",
  "singleton_rate": 0.15,
  "validation_flags": ["FLAG1", "FLAG2"],
  "recommendations": ["..."]
}
```

### Text Report
Simple plain text summary for quick review

## Integration Examples

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
for file in $(git diff --cached --name-only --diff-filter=ACM | grep ".txt\|.md"); do
  python validation_system/validate.py --file "$file" --threshold 0.7
  if [ $? -ne 0 ]; then
    echo "Validation failed for $file"
    exit 1
  fi
done
```

### CI/CD Pipeline

```yaml
# .github/workflows/validate.yml
- name: Validate Output Quality
  run: |
    python validation_system/validate.py \
      --file output.txt \
      --sources data/*.txt \
      --report markdown \
      --output validation_report.md
```

### Python Integration

```python
from validation_interface import ValidationInterface

class ConsultingReport:
    def __init__(self):
        self.validator = ValidationInterface()
    
    def generate_section(self, content, sources):
        # Generate content
        result = self.validator.full_validate(content, sources)
        
        if not result.passed:
            # Apply recommendations
            for rec in result.recommendations:
                content = self.apply_recommendation(content, rec)
            
            # Re-validate
            result = self.validator.full_validate(content, sources)
        
        return content, result
```

## Theory Behind the System

Based on the paper's key findings:

1. **Error Lower Bound**: `err ≥ 2·erriiv - |Vc|/|Ec| - δ`
   - Generation errors are at least twice the classification error rate
   - Implemented through validation ratio checking

2. **Singleton Rate Correlation**: Hallucination rate ≥ fraction of singleton facts
   - Tracked through singleton detection and cross-validation

3. **Confidence Thresholds**: Explicit confidence targets reduce hallucinations
   - Implemented via confidence level classification

4. **Binary Grading Problem**: Most evaluations penalize uncertainty
   - Addressed by rewarding appropriate abstentions

## Best Practices

1. **Always provide sources** for cross-validation
2. **Set appropriate domain** for context-specific rules
3. **Review recommendations** and iterate on content
4. **Track validation history** to identify patterns
5. **Adjust thresholds** based on use case requirements

## Troubleshooting

### High Singleton Rate
- Add more sources for cross-validation
- Remove unsupported speculative claims
- Increase citation density

### Poor Validation Ratio
- Strengthen evidence for key claims
- Remove or qualify weak assertions
- Add explicit uncertainty acknowledgments

### High Hallucination Risk
- Reduce arbitrary fact claims
- Increase empirical support
- Add confidence qualifiers

## References

Kalai, A.T., Vempala, S.S. et al. (2025). "Why Language Models Hallucinate." 
arXiv:2509.04664v1

## License

MIT License - Use and modify freely for your validation needs.
