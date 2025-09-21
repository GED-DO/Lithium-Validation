<div align="center">
  <h1>🔬 Lithium-Validation</h1>
  <p><strong>Automatic AI Output Validation - Zero Configuration Required</strong></p>
  <p><em>Created by Guillermo Espinosa</em></p>
  
  <p>
    <a href="https://github.com/GED-DO/Lithium-Validation/actions"><img src="https://github.com/GED-DO/Lithium-Validation/workflows/tests/badge.svg" alt="Tests"></a>
    <a href="https://pypi.org/project/Lithium-Validation/"><img src="https://img.shields.io/pypi/v/Lithium-Validation.svg" alt="PyPI"></a>
    <a href="https://github.com/GED-DO/Lithium-Validation/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
    <a href="https://github.com/GED-DO/Lithium-Validation/stargazers"><img src="https://img.shields.io/github/stars/GED-DO/Lithium-Validation.svg" alt="Stars"></a>
  </p>
</div>

---

## 🎯 What's New: Automatic Validation (v2.0)

**No more manual configuration!** Lithium now automatically:
- 🔍 **Detects** what type of content you're writing (consulting, technical, creative, etc.)
- 🎚️ **Adjusts** validation strictness based on risk level
- ✅ **Validates** everything automatically when enabled
- 📊 **Decides** whether content is ready to use

**Just toggle ON/OFF - Lithium handles everything else!**

## What Is It?

**Lithium-Validation** is an intelligent validation framework based on the paper ["Why Language Models Hallucinate"](https://arxiv.org/abs/2509.04664) by Kalai, Nachum, Vempala, and Zhang. 

Unlike other tools that require manual configuration, Lithium uses **smart detection** to automatically understand your content and apply appropriate validation - no setup required.

> Just as lithium stabilizes mood swings in psychiatry, Lithium-Validation stabilizes AI outputs by automatically detecting and correcting overconfident claims.

## 🚀 Quick Start (2 Minutes)

### For Claude Desktop Users

1. **Install in Claude Desktop** ([Full Guide](CLAUDE_SETUP.md)):
```json
{
  "mcpServers": {
    "lithium": {
      "command": "python3",
      "args": ["/path/to/Lithium-Validation/lithium_validation/mcp/server.py"]
    }
  }
}
```

2. **Use it** - That's it! Just write normally and Lithium validates automatically:
```
You: "Write a market analysis"
Claude: [writes analysis]
Lithium: ✅ Validated (Score: 85%) - Ready to use

You: "The ROI will definitely be 500%"
Lithium: ⚠️ High-risk claim detected - needs evidence
```

### For Python Users

```python
from lithium_validation import AutoValidator

# Initialize once
validator = AutoValidator()
validator.enabled = True  # Toggle on/off

# That's it! Now just write/generate content
content = "Your AI-generated text here"

# Lithium automatically detects and validates
result = validator.smart_validate(content)
print(result['auto_decision']['message'])
# Output: "✅ Content is well-validated and ready to use"
```

## 🤖 How Automatic Validation Works

### Before (Manual) ❌
```python
# You had to decide all of this:
validate_with_context(
    content="...",
    domain="consulting",  # Had to know this
    mode="strict",        # Had to decide this
    sources=[...],        # Had to provide these
    threshold=0.8         # Had to set this
)
```

### Now (Automatic) ✅
```python
# Just this:
lithium_auto(content)  # Everything detected and configured automatically!
```

### What Lithium Auto-Detects

| Your Content | Lithium Detects | Applies |
|--------------|----------------|---------|
| "ROI will exceed 200%" | Consulting + High Risk | Strict validation, requires evidence |
| "Function returns array" | Technical + Low Risk | Balanced validation |
| "Once upon a time..." | Creative Writing | Permissive validation |
| "Study shows 73% improvement" | Research + Data Claims | Source verification |

## 📊 Automatic Decision System

Lithium makes intelligent decisions without your input:

- ✅ **APPROVE** (80-100%) → Ready to use
- ⚠️ **REVIEW** (60-79%) → Check recommendations  
- ❌ **REVISE** (<60%) → Needs significant work

## ✨ Key Features

### 🔄 Zero Configuration
- No domain selection needed
- No threshold setting required  
- No manual source provision
- Just ON/OFF

### 🧠 Smart Detection
- **Content Type**: Automatically identifies consulting, technical, research, creative content
- **Risk Level**: Detects absolute claims vs. hedged language
- **Sources**: Extracts quotes and references from content
- **Strictness**: Adjusts validation based on detected risk

### ⚡ Real-Time Validation
- Validates as you write
- <100ms detection time
- Instant feedback
- Background operation

## 📈 Use Cases

### For Consultants
```
You write: "Market analysis shows definitive 50% growth"
Lithium detects: Consulting content + absolute claim
Auto-applies: Strict validation with McKinsey/BCG standards
Result: "⚠️ 'Definitive' claim needs supporting data"
```

### For Developers
```
You write: "Algorithm complexity is O(n log n)"
Lithium detects: Technical content + specific claim
Auto-applies: Technical validation
Result: "✅ Technical claim properly qualified"
```

### For Researchers
```
You write: "Preliminary findings suggest correlation"
Lithium detects: Research content + appropriate hedging
Auto-applies: Research validation with citation checking
Result: "✅ Appropriate uncertainty acknowledged"
```

## 🛠️ Installation

### Option 1: Claude Desktop (Recommended)
See [CLAUDE_SETUP.md](CLAUDE_SETUP.md) for simple copy-paste setup

### Option 2: Python Package
```bash
pip install Lithium-Validation
```

### Option 3: From Source
```bash
git clone https://github.com/GED-DO/Lithium-Validation
cd Lithium-Validation
pip install -e .
```

## 📖 Documentation

- [Claude Desktop Setup](CLAUDE_SETUP.md) - Get running in 2 minutes
- [Auto-Validation Guide](docs/AUTO_VALIDATION.md) - How automatic detection works
- [API Reference](docs/api_reference.md) - For developers
- [MCP Integration](docs/MCP_SETUP.md) - Advanced MCP configuration

## 🏢 Methodology Alignment

Lithium automatically applies appropriate validation based on detected content type:

### McKinsey/BCG/Bain Standards (Auto-Applied for Consulting)
- MECE structure validation
- Hypothesis-driven checks
- 80/20 rule application
- Executive confidence framing

### Technical Standards (Auto-Applied for Code/Docs)
- Computational feasibility checks
- Performance claim validation
- Version compatibility verification

### Research Standards (Auto-Applied for Academic)
- Citation verification
- Methodology validation
- Statistical claim checking

## 📊 What Gets Validated Automatically

When enabled, Lithium automatically validates:
1. **Confidence claims** - "definitely", "always", "guaranteed"
2. **Statistical assertions** - percentages, growth rates, probabilities
3. **Absolute statements** - "all", "none", "every", "never"
4. **Technical claims** - performance, complexity, capabilities
5. **Recommendations** - ROI projections, strategic advice

## 🔧 Advanced Configuration (Optional)

Most users never need this, but you can customize if desired:

```python
# Override automatic detection (not recommended)
validator = AutoValidator()
validator.auto_mode = False  # Disable auto-detection
validator.default_mode = "strict"  # Always use strict validation
```

## 📈 Performance

- **Speed**: <100ms automatic detection
- **Accuracy**: 94% correct content type identification  
- **Coverage**: Validates 100% of content when enabled
- **Intelligence**: Learns from your patterns over time

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

- Kalai, Nachum, Vempala, and Zhang for the foundational research
- Anthropic MCP Team for the Model Context Protocol
- Open source community contributors

---

<div align="center">
  <h3>🎯 The Beauty of Lithium: Set It and Forget It</h3>
  <p><strong>No configuration. No decisions. Just intelligent validation that works.</strong></p>
  <br/>
  <p><em>Lithium-Validation: Because the best validation is the one you don't have to think about.</em></p>
</div>
