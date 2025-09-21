#!/bin/bash

# Lithium - Validation Framework MCP Installation Script
# Stabilizing your AI outputs through systematic validation

echo "╔══════════════════════════════════════════╗"
echo "║   Lithium - Validation Framework        ║"
echo "║   MCP Server Installation                ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.8 or higher is required (found $python_version)"
    exit 1
fi

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Install dependencies
echo "Installing MCP package for Lithium..."
pip3 install -r "$SCRIPT_DIR/requirements.txt"

# Create configuration for Claude Desktop
echo "Creating Lithium configuration for Claude Desktop..."

# Claude Desktop config path (adjust if needed)
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

# Create directory if it doesn't exist
mkdir -p "$CLAUDE_CONFIG_DIR"

# Check if config file exists
if [ -f "$CLAUDE_CONFIG_FILE" ]; then
    echo "Existing Claude configuration found. Creating backup..."
    cp "$CLAUDE_CONFIG_FILE" "$CLAUDE_CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Create or update the configuration
cat > "$SCRIPT_DIR/lithium_config_snippet.json" << EOF
{
  "mcpServers": {
    "lithium": {
      "command": "python3",
      "args": [
        "$SCRIPT_DIR/lithium_mcp_server.py"
      ],
      "env": {}
    }
  }
}
EOF

echo "Lithium configuration snippet created at: $SCRIPT_DIR/lithium_config_snippet.json"

# Instructions for manual setup
echo ""
echo "═══════════════════════════════════════════"
echo "       LITHIUM INSTALLATION COMPLETE       "
echo "═══════════════════════════════════════════"
echo ""
echo "To activate Lithium in Claude Desktop:"
echo ""
echo "1. Add the Lithium MCP server to Claude Desktop:"
echo "   - Open Claude Desktop settings"
echo "   - Go to Developer > MCP Servers"
echo "   - Add this configuration:"
echo ""
echo "   Name: lithium"
echo "   Command: python3"
echo "   Arguments: $SCRIPT_DIR/lithium_mcp_server.py"
echo ""
echo "2. OR manually add this to your claude_desktop_config.json:"
echo "   Location: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo ""
cat "$SCRIPT_DIR/lithium_config_snippet.json"
echo ""
echo "3. Restart Claude Desktop"
echo ""
echo "4. Test by typing: 'Use Lithium to validate this text'"
echo ""
echo "═══════════════════════════════════════════"
echo "        LITHIUM VALIDATION TOOLS           "
echo "═══════════════════════════════════════════"
echo ""
echo "• lithium_validate      - General validation"
echo "• lithium_validate_context - Domain-specific"
echo "• lithium_risk_check    - Hallucination risk"
echo "• lithium_analyze_claims - Claim analysis"
echo "• lithium_report        - Formatted reports"
echo "• lithium_compare       - Compare versions"
echo "• lithium_stabilize     - Improve outputs"
echo ""
echo "═══════════════════════════════════════════"
echo ""
echo "Lithium: Stabilizing your outputs, one validation at a time."
echo ""

# Make the MCP server executable
chmod +x "$SCRIPT_DIR/lithium_mcp_server.py"

echo "Installation complete! Lithium is ready to stabilize your outputs."
