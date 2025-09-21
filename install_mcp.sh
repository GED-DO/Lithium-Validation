#!/bin/bash

# Validation System MCP Installation Script
# This script sets up the MCP server for the validation system

echo "Installing Validation System MCP Server..."

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
echo "Installing MCP package..."
pip3 install -r "$SCRIPT_DIR/requirements.txt"

# Create configuration for Claude Desktop
echo "Creating Claude Desktop configuration..."

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
cat > "$SCRIPT_DIR/claude_config_snippet.json" << EOF
{
  "mcpServers": {
    "validation-system": {
      "command": "python3",
      "args": [
        "$SCRIPT_DIR/validation_mcp_server.py"
      ],
      "env": {}
    }
  }
}
EOF

echo "Configuration snippet created at: $SCRIPT_DIR/claude_config_snippet.json"

# Instructions for manual setup
echo ""
echo "======================================"
echo "Installation almost complete!"
echo "======================================"
echo ""
echo "To finish setup, you need to:"
echo ""
echo "1. Add the validation-system MCP server to Claude Desktop:"
echo "   - Open Claude Desktop settings"
echo "   - Go to Developer > MCP Servers"
echo "   - Add this configuration:"
echo ""
echo "   Name: validation-system"
echo "   Command: python3"
echo "   Arguments: $SCRIPT_DIR/validation_mcp_server.py"
echo ""
echo "2. OR manually add this to your claude_desktop_config.json:"
echo "   Location: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo ""
cat "$SCRIPT_DIR/claude_config_snippet.json"
echo ""
echo "3. Restart Claude Desktop"
echo ""
echo "4. Test by typing: 'Use the validation tools to check this text'"
echo ""
echo "======================================"
echo "Available validation tools:"
echo "- validate_output: General validation"
echo "- validate_with_context: Domain-specific validation"
echo "- check_hallucination_risk: Quick risk check"
echo "- validate_claims: Individual claim analysis"
echo "- get_validation_report: Formatted reports"
echo "- batch_validate: Multiple text comparison"
echo "- improve_output: Improvement suggestions"
echo "======================================"

# Make the MCP server executable
chmod +x "$SCRIPT_DIR/validation_mcp_server.py"

echo ""
echo "Installation script complete!"
