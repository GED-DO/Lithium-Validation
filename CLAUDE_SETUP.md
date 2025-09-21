# 🚀 Quick Claude Desktop Setup - Copy & Paste

## Step 1: Find Your Config File

### Mac:
```bash
open ~/Library/Application\ Support/Claude/
```
Look for `claude_desktop_config.json`

### Windows:
```
Win + R → type: %APPDATA%\Claude
```
Look for `claude_desktop_config.json`

## Step 2: Copy This Configuration

**Copy this ENTIRE block and paste it into your `claude_desktop_config.json`:**

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

## Step 3: Update the Path

**IMPORTANT: Replace the path above with YOUR actual path:**

### How to get your path:
```bash
# Run this command in your Lithium-Validation folder:
pwd
# It will show something like: /Users/YOUR_NAME/path/to/Lithium-Validation

# Your server.py path will be:
# [YOUR_PATH]/lithium_validation/mcp/server.py
```

### Example paths:
- **Mac**: `/Users/ged/Documents/Lithium-Validation/lithium_validation/mcp/server.py`
- **Windows**: `C:\\Users\\YourName\\Documents\\Lithium-Validation\\lithium_validation\\mcp\\server.py`

## Step 4: Restart Claude Desktop

1. Completely quit Claude Desktop (Cmd+Q on Mac, Alt+F4 on Windows)
2. Reopen Claude Desktop
3. Test with: "Use Lithium to validate this text"

---

## 🎯 One-Line Path Finder (Mac/Linux)

Run this in your Lithium folder to get the exact path you need:

```bash
echo "Your path for Claude config:"
echo "\"$(pwd)/lithium_validation/mcp/server.py\""
```

Copy the output and paste it into the "args" section of the config.

---

## ✅ Complete Example Config (Mac)

If your Lithium-Validation is in Documents folder:

```json
{
  "mcpServers": {
    "lithium": {
      "command": "python3",
      "args": [
        "/Users/ged/Documents/Lithium-Validation/lithium_validation/mcp/server.py"
      ],
      "env": {}
    }
  }
}
```

## ✅ Complete Example Config (Windows)

```json
{
  "mcpServers": {
    "lithium": {
      "command": "python",
      "args": [
        "C:\\Users\\Ged\\Documents\\Lithium-Validation\\lithium_validation\\mcp\\server.py"
      ],
      "env": {}
    }
  }
}
```

---

## 🧪 Test Commands

Once configured, test these in Claude:

```
"Use Lithium to validate this text: All companies using AI will succeed 100% of the time."
Expected: HIGH risk warning

"Lithium check: Based on preliminary data, results may vary between 40-60%."
Expected: LOW risk, good uncertainty acknowledgment

"Turn on Lithium auto-validation"
Expected: Confirmation that auto-validation is enabled
```

---

## ⚠️ Common Issues & Fixes

### "Lithium not found"
- Check the path is correct (use the path finder command above)
- Make sure Python 3 is installed: `python3 --version`
- Ensure server.py file exists at the path

### "Module not found: mcp"
```bash
pip install mcp
# or
pip3 install mcp
```

### "Permission denied"
```bash
chmod +x /path/to/your/lithium_validation/mcp/server.py
```

---

## 📋 Quick Checklist

- [ ] Found claude_desktop_config.json
- [ ] Copied the configuration
- [ ] Updated the path to YOUR Lithium location
- [ ] Saved the file
- [ ] Restarted Claude Desktop
- [ ] Tested with a validation command

That's it! Just copy, paste, update path, restart. 🎉
