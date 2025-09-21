#!/bin/bash
# Quick MCP Configuration Generator for Claude Desktop
# Run this script to generate the exact config you need

echo "🔬 Lithium MCP Configuration Generator"
echo "======================================"
echo ""

# Get the current directory
CURRENT_DIR=$(pwd)
LITHIUM_PATH="$CURRENT_DIR/lithium_validation/mcp/server.py"

# Check if server.py exists
if [ ! -f "$LITHIUM_PATH" ]; then
    echo "❌ Error: server.py not found at $LITHIUM_PATH"
    echo "Make sure you're running this from the Lithium-Validation directory!"
    exit 1
fi

echo "✅ Found Lithium server at:"
echo "   $LITHIUM_PATH"
echo ""

# Generate the configuration
cat << EOF > claude_config.json
{
  "mcpServers": {
    "lithium": {
      "command": "python3",
      "args": [
        "$LITHIUM_PATH"
      ],
      "env": {}
    }
  }
}
EOF

echo "📋 Configuration generated: claude_config.json"
echo ""
echo "INSTRUCTIONS:"
echo "============="
echo ""
echo "1. Open Claude Desktop settings:"
echo "   - Mac: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo "   - Windows: %APPDATA%\\Claude\\claude_desktop_config.json"
echo ""
echo "2. Copy the contents of claude_config.json into that file"
echo ""
echo "3. Restart Claude Desktop"
echo ""
echo "4. Test with: 'Use Lithium to validate this text'"
echo ""
echo "📄 Your configuration has been saved to: claude_config.json"
echo ""
echo "You can also copy it from here:"
echo "--------------------------------"
cat claude_config.json
echo "--------------------------------"
