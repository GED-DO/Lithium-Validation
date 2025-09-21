<div align="center">
  <h1>🔬 Lithium-Validation</h1>
  <p><strong>Stabilizing AI outputs through systematic validation</strong></p>
  <p><em>Created by Guillermo Espinosa</em></p>
  
  <p>
    <a href="https://github.com/GED-DO/Lithium-Validation/actions"><img src="https://github.com/GED-DO/Lithium-Validation/workflows/tests/badge.svg" alt="Tests"></a>
    <a href="https://pypi.org/project/Lithium-Validation/"><img src="https://img.shields.io/pypi/v/Lithium-Validation.svg" alt="PyPI"></a>
    <a href="https://github.com/GED-DO/Lithium-Validation/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
    <a href="https://github.com/GED-DO/Lithium-Validation/stargazers"><img src="https://img.shields.io/github/stars/GED-DO/Lithium-Validation.svg" alt="Stars"></a>
  </p>
</div>

---

## What Is It?

**Lithium-Validation** is a Python-based validation engine based on the paper ["Why Language Models Hallucinate"](https://arxiv.org/abs/2509.04664) by Adam Tauman Kalai, Ofir Nachum, Santosh S. Vempala, and Edwin Zhang.

Building explicit uncertainty acknowledgment into your frameworks isn't a weakness - **it's a mathematical requirement** for reliable outputs. The paper proves that without this, even the most sophisticated systems will hallucinate at predictable rates.

> Just as lithium stabilizes mood swings in psychiatry, the Lithium-Validation framework stabilizes AI outputs by detecting overconfident claims and identifying unsupported statements.

## 🎯 The Three-Stage Validation Process

### 1. **Pre-Validation Stage** (Using Context Model Protocol)
- Classify insight type (empirical/inferential/hypothetical)
- Identify singleton vs. validated insights
- Set explicit confidence thresholds

### 2. **Output Generation**
- Tag each claim with confidence level
- Include "abstention value" - what the client gains from knowing what you don't know
- Build in cross-validation from multiple sources

### 3. **Quality Assurance**
- Apply the 2:1 rule from the paper - ensure validated insights outweigh unvalidated ones 2:1
- Check for "computational hardness" - are you claiming insights that would require impossible analysis?
- Verify scope boundaries are explicit

## ✨ What Makes It Valuable

It translates **academic research** into **practical checks**:
- Pattern recognition for claim types
- Statistical analysis of support ratios
- Rule-based bias detection
- Mathematical scoring based on the paper's proofs
- ✅ No external dependencies or APIs
- ✅ Based on published academic research
- ✅ Not a model, but a framework

Think of it like a **sophisticated checklist system** that:
- Counts and categorizes claims
- Checks against sources
- Calculates ratios and scores
- Applies the paper's mathematical insights

It's similar to grammar checkers or linting tools - algorithmic validation based on rules, not a trained AI model.

## 🚀 Quick Start

### Installation

```bash
# Via pip
pip install Lithium-Validation

# Via GitHub
git clone https://github.com/GED-DO/Lithium-Validation
cd Lithium-Validation
pip install -e .
```

### Basic Usage

Just ask something like:
- "Validate this output: [your text]"
- "Check this for hallucination risk: [your text]"
- "Run validation on my last response"

```python
from lithium_validation import quick_check, ValidationInterface

# Quick validation
result = quick_check("Your AI-generated text here")
print(f"Score: {result['score']}%, Risk: {result['risk']}")

# You'll get:
# - Overall score (0-100%)
# - Hallucination risk (LOW/MEDIUM/HIGH)
# - Key issues found
# - Specific recommendations

# Full validation with sources
lithium = ValidationInterface()
result = lithium.full_validate(
    content="Your text",
    sources=["Source 1", "Source 2"],
    domain="consulting"
)
```

### Command Line

```bash
# Quick check
lithium-validate --text "Your output text"

# With sources
lithium-validate --file output.txt --sources source1.txt source2.txt

# Generate report
lithium-report --file output.txt --format markdown
```

## 🤖 Claude Desktop Integration

Add Lithium-Validation to your Claude Desktop for real-time validation:

```bash
# Install MCP server
lithium-validate install-mcp

# Add to Claude configuration
lithium-validate configure-claude
```

Then in Claude:
- "Use Lithium to validate this text"
- "Check stability with Lithium"
- "Lithium risk assessment for: [text]"

[Full MCP Setup Guide](./docs/MCP_SETUP.md)

## 📊 Validation Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Stability Score | ≥80% | Overall output quality |
| Hallucination Risk | <20% | Risk of unsupported claims |
| Singleton Rate | <20% | Claims without cross-validation |
| Validation Ratio | ≥2:1 | Supported vs unsupported claims |

## 🏢 Specific Methodology for Consulting (McKinsey/BCG/Bain)

Given the preference for top-tier consulting methodologies, Lithium integrates these findings into:

### **Enhanced Hypothesis-Driven Approach:**
- Start with confidence-weighted hypotheses
- Build explicit "unknown tracking" into MECE trees
- Create "validation debt" metrics for each branch of analysis

### **Modified Issue Trees:**
- Add confidence scores to each branch
- Identify which branches have "singleton support" (only one data point)
- Build parallel validation paths for critical decisions

This framework provides mathematical proof for why Context Model Protocol approaches are correct - it's not just good practice, it's **statistically necessary** to avoid systematic errors in complex analytical work.

## 🔍 What Lithium Checks For

When you request validation, Lithium evaluates:
1. **Singleton claims** (facts appearing only once)
2. **Confidence distribution** (balance of certain vs uncertain)
3. **Support ratio** (validated vs unvalidated claims)
4. **Biases** (confirmation, recency, geographic)
5. **Computational impossibilities**
6. **Appropriate uncertainty acknowledgment**

## 📖 Documentation

- [Installation Guide](docs/installation.md)
- [Quick Start Tutorial](docs/quickstart.md)
- [API Reference](docs/api_reference.md)
- [MCP Integration](docs/MCP_SETUP.md)
- [Theoretical Foundation](docs/theory.md)

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 🔬 Academic Foundation

Based on:
> Kalai, A.T., Nachum, O., Vempala, S.S., Zhang, E. (2025). "Why Language Models Hallucinate." arXiv:2509.04664v1

## 👨‍💻 Author

**Guillermo Espinosa**
- GitHub: [@GED-DO](https://github.com/GED-DO)
- Email: hola@ged.do
- LinkedIn: [Guillermo Espinosa](https://www.linkedin.com/in/guillermo-espinosa/)

## 🙏 Acknowledgments

- Adam Tauman Kalai, Ofir Nachum, Santosh S. Vempala, and Edwin Zhang for the foundational research
- Anthropic MCP Team for the Model Context Protocol
- Open source community contributors

---

<div align="center">
  <strong>Lithium-Validation: Stabilizing your AI, one validation at a time.</strong>
</div>
