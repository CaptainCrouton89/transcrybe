#!/bin/bash
# Debug version of Transcrybe launcher

set -x  # Enable debug output

echo "=== Debug Info ==="
echo "Script path: $0"
echo "PWD: $(pwd)"

# Get the directory containing this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo "SCRIPT_DIR: $SCRIPT_DIR"

BUNDLE_DIR="$(dirname "$SCRIPT_DIR")"
echo "BUNDLE_DIR: $BUNDLE_DIR"

RESOURCES_DIR="$BUNDLE_DIR/Contents/Resources"
echo "RESOURCES_DIR: $RESOURCES_DIR"

# Check for menubar_transcriber.py in Resources
PYTHON_SCRIPT="$RESOURCES_DIR/menubar_transcriber.py"
echo "PYTHON_SCRIPT: $PYTHON_SCRIPT"
echo "File exists: $(test -f "$PYTHON_SCRIPT" && echo "YES" || echo "NO")"

if [ -f "$PYTHON_SCRIPT" ]; then
    echo "Found Python script, launching..."
    python3 "$PYTHON_SCRIPT"
else
    echo "Python script not found!"
    ls -la "$RESOURCES_DIR"
fi