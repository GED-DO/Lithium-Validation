@echo off
REM Quick MCP Configuration Generator for Claude Desktop (Windows)
REM Run this script to generate the exact config you need

echo Lithium MCP Configuration Generator
echo ====================================
echo.

REM Get the current directory
set CURRENT_DIR=%cd%
set LITHIUM_PATH=%CURRENT_DIR%\lithium_validation\mcp\server.py

REM Check if server.py exists
if not exist "%LITHIUM_PATH%" (
    echo Error: server.py not found at %LITHIUM_PATH%
    echo Make sure you're running this from the Lithium-Validation directory!
    pause
    exit /b 1
)

echo Found Lithium server at:
echo    %LITHIUM_PATH%
echo.

REM Replace backslashes with double backslashes for JSON
set LITHIUM_PATH_JSON=%LITHIUM_PATH:\=\\%

REM Generate the configuration
(
echo {
echo   "mcpServers": {
echo     "lithium": {
echo       "command": "python",
echo       "args": [
echo         "%LITHIUM_PATH_JSON%"
echo       ],
echo       "env": {}
echo     }
echo   }
echo }
) > claude_config.json

echo Configuration generated: claude_config.json
echo.
echo INSTRUCTIONS:
echo =============
echo.
echo 1. Open Claude Desktop settings:
echo    Press Win + R, type: %%APPDATA%%\Claude
echo    Open: claude_desktop_config.json
echo.
echo 2. Copy the contents of claude_config.json into that file
echo.
echo 3. Restart Claude Desktop
echo.
echo 4. Test with: 'Use Lithium to validate this text'
echo.
echo Your configuration has been saved to: claude_config.json
echo.
echo You can also see it here:
echo --------------------------------
type claude_config.json
echo --------------------------------
echo.
pause
