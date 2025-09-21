# 🤖 Claude Desktop MCP Integration Guide

## Quick Setup (2 Minutes)

### Step 1: Install Lithium-Validation
```bash
# Clone the repository
git clone https://github.com/GED-DO/Lithium-Validation.git
cd Lithium-Validation

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Add to Claude Desktop Configuration

1. **Open Claude Desktop Settings**
   - Click on your profile icon
   - Select "Settings"
   - Navigate to "Developer" → "MCP Servers"

2. **Add Lithium Configuration**
   
   Click "Add Server" and enter:
   - **Name:** `lithium`
   - **Command:** `python3`
   - **Arguments:** `/path/to/Lithium-Validation/lithium_validation/mcp/server.py`

   Replace `/path/to/` with your actual path, for example:
   - Mac: `/Users/ged/Documents/brain/validation_system/lithium_validation/mcp/server.py`
   - Windows: `C:\Users\YourName\Documents\Lithium-Validation\lithium_validation\mcp\server.py`

### Step 3: Restart Claude Desktop
- Completely quit Claude Desktop (Cmd+Q on Mac, Alt+F4 on Windows)
- Reopen Claude Desktop
- The Lithium tools should now be available

## 🛠 Alternative: Manual Configuration

If you prefer editing the config file directly:

### Mac/Linux:
```bash
# Open the configuration file
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Windows:
```powershell
# Open the configuration file
notepad %APPDATA%\Claude\claude_desktop_config.json
```

### Add this configuration:
```json
{
  "mcpServers": {
    "lithium": {
      "command": "python3",
      "args": [
        "/Users/ged/Documents/brain/validation_system/lithium_validation/mcp/server.py"
      ],
      "env": {}
    }
  }
}
```

## ✅ Verify Installation

After restarting Claude Desktop, test by typing any of these commands:

- "Use Lithium to validate this text"
- "Check stability with Lithium"
- "Lithium risk assessment for: [your text]"

## 📚 Available Lithium Tools

Once installed, you'll have access to 7 validation tools:

| Command | What it does |
|---------|--------------|
| `lithium_validate` | General validation with score and risk level |
| `lithium_validate_context` | Domain-specific validation (consulting, technical) |
| `lithium_risk_check` | Quick hallucination risk assessment |
| `lithium_analyze_claims` | Individual claim validation |
| `lithium_report` | Generate markdown or JSON reports |
| `lithium_compare` | Compare multiple text versions |
| `lithium_stabilize` | Iterative improvement suggestions |

## 💡 Usage Examples

### Basic Validation
```
"Lithium, validate this: Our analysis shows 100% of companies succeed with this strategy."
```
**Result:** High risk, 25% score, recommends adding uncertainty acknowledgment

### Consulting Context
```
"Use Lithium consulting mode to check: Market will grow 50% annually based on our research."
```
**Result:** Checks for MECE structure, confidence levels, and McKinsey-style validation

### Risk Assessment
```
"What's the hallucination risk for my last response?"
```
**Result:** Provides risk score, singleton rate, and stability metrics

### Generate Report
```
"Create a Lithium validation report for the previous analysis"
```
**Result:** Markdown report with scores, issues, and recommendations

## 🔧 Troubleshooting

### "Lithium tools not found"
- Ensure Claude Desktop is completely restarted
- Check the path in configuration is correct
- Verify Python 3.8+ is installed: `python3 --version`

### "ModuleNotFoundError: mcp"
```bash
pip install mcp
# or
pip3 install mcp
```

### "Permission denied"
```bash
chmod +x /Users/ged/Documents/brain/validation_system/lithium_validation/mcp/server.py
```

### Check MCP Server Logs
Look for errors in Claude Desktop's developer console:
- Mac: Cmd+Option+I
- Windows: Ctrl+Shift+I

## 🚀 Quick Install Script

For automatic setup, create and run this script:

```bash
#!/bin/bash
# install_mcp.sh - Lithium MCP Installer

echo "🔬 Installing Lithium-Validation MCP for Claude Desktop"

# Get the current directory
LITHIUM_PATH="$(pwd)/lithium_validation/mcp/server.py"

# Create configuration
cat << EOF > lithium_mcp_config.json
{
  "mcpServers": {
    "lithium": {
      "command": "python3",
      "args": ["$LITHIUM_PATH"],
      "env": {}
    }
  }
}
EOF

echo "✅ Configuration created!"
echo ""
echo "📋 Next steps:"
echo "1. Open Claude Desktop Settings"
echo "2. Go to Developer → MCP Servers"
echo "3. Add the configuration from lithium_mcp_config.json"
echo "4. Restart Claude Desktop"
echo ""
echo "📍 Your Lithium path: $LITHIUM_PATH"
```

## 📖 Additional Documentation

- **Main Repository:** [github.com/GED-DO/Lithium-Validation](https://github.com/GED-DO/Lithium-Validation)
- **Paper Reference:** ["Why Language Models Hallucinate"](https://arxiv.org/abs/2509.04664)
- **Author:** Guillermo Espinosa (hola@ged.do)

## 🎯 Pro Tips

1. **Use with Claude Projects:** Create a project called "Validated Outputs" and always use Lithium tools within it
2. **Set Validation Thresholds:** Aim for 80%+ stability score for client deliverables
3. **Domain Modes:** Use `consulting` mode for business content, `technical` for code/specs
4. **Batch Validation:** Use `lithium_compare` to test multiple versions of your content

---

**Need help?** Open an issue at [github.com/GED-DO/Lithium-Validation/issues](https://github.com/GED-DO/Lithium-Validation/issues)
