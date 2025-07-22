#!/bin/bash
# Launch script for Transcrybe - handles environment setup and permissions

set -e

# Get the directory containing this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
BUNDLE_DIR="$(dirname "$SCRIPT_DIR")"
RESOURCES_DIR="$BUNDLE_DIR/Contents/Resources"

# Set up Python environment
export PYTHONPATH="$RESOURCES_DIR:$PYTHONPATH"

# Check for required permissions and show alerts if missing
check_permissions() {
    local missing_perms=""
    
    # Check microphone permission
    if ! system_profiler SPAudioDataType 2>/dev/null | grep -q "Built-in Microphone"; then
        missing_perms="$missing_perms\n• Microphone access"
    fi
    
    # Check accessibility permission by testing if we can enable assistive access
    if ! sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db "SELECT service FROM access WHERE client='com.transcrybe.app' AND service='kTCCServiceAccessibility'" 2>/dev/null | grep -q "kTCCServiceAccessibility"; then
        missing_perms="$missing_perms\n• Accessibility access"
    fi
    
    if [ ! -z "$missing_perms" ]; then
        osascript -e "display dialog \"Transcrybe requires additional permissions to function properly:$missing_perms\n\nThe app will request these permissions when launched. Please grant them in System Settings.\" with title \"Transcrybe - Permissions Required\" buttons {\"Continue\"} default button \"Continue\""
    fi
}

# Find Python executable
find_python() {
    # Try common Python locations
    for python_cmd in python3 /usr/bin/python3 /usr/local/bin/python3 /opt/homebrew/bin/python3; do
        if command -v "$python_cmd" &> /dev/null; then
            echo "$python_cmd"
            return 0
        fi
    done
    
    # If no Python found, show error
    osascript -e "display dialog \"Python 3 is required but not found. Please install Python 3 and try again.\" with title \"Transcrybe - Error\" buttons {\"OK\"} default button \"OK\""
    exit 1
}

# Check if running from .app bundle
if [[ "$SCRIPT_DIR" == *.app/Contents/MacOS ]]; then
    # Running from app bundle
    APP_BUNDLE=true
    PYTHON_SCRIPT="$RESOURCES_DIR/menubar_transcriber.py"
else
    # Running from development directory
    APP_BUNDLE=false
    PYTHON_SCRIPT="$SCRIPT_DIR/menubar_transcriber.py"
fi

# Check permissions (only in app bundle mode)
if [ "$APP_BUNDLE" = true ]; then
    check_permissions
fi

# Find Python
PYTHON_CMD=$(find_python)

# Install requirements if in development mode
if [ "$APP_BUNDLE" = false ]; then
    if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
        echo "Installing/updating requirements..."
        "$PYTHON_CMD" -m pip install --user -r "$SCRIPT_DIR/requirements.txt" 2>/dev/null || true
    fi
fi

# Launch the application
echo "Starting Transcrybe..."
cd "$SCRIPT_DIR"
exec "$PYTHON_CMD" "$PYTHON_SCRIPT"