#!/bin/bash
# Transcrybe Installer

set -e

APP_NAME="Transcrybe.app"
INSTALL_DIR="/Applications"
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing Transcrybe..."

# Check if app bundle exists
if [ ! -d "$CURRENT_DIR/$APP_NAME" ]; then
    echo "Error: $APP_NAME not found in current directory"
    exit 1
fi

# Remove existing installation
if [ -d "$INSTALL_DIR/$APP_NAME" ]; then
    echo "Removing existing installation..."
    rm -rf "$INSTALL_DIR/$APP_NAME"
fi

# Copy app to Applications
echo "Copying $APP_NAME to $INSTALL_DIR..."
cp -R "$CURRENT_DIR/$APP_NAME" "$INSTALL_DIR/"

# Set correct permissions
chmod +x "$INSTALL_DIR/$APP_NAME/Contents/MacOS/Transcrybe"

echo "Installation complete!"
echo ""
echo "Transcrybe has been installed to $INSTALL_DIR/$APP_NAME"
echo ""
echo "To launch Transcrybe:"
echo "1. Open Applications folder"
echo "2. Double-click Transcrybe"
echo "3. Grant required permissions when prompted"
echo "4. Use Cmd+Shift+Space to start transcription"
echo ""
echo "Note: Python 3 is required. Install from python.org if not already installed."
