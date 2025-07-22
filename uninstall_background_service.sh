#!/bin/bash
# Uninstall Transcrybe background service

LAUNCHAGENT_DIR="$HOME/Library/LaunchAgents"
LAUNCHAGENT_FILE="com.silas.transcrybe.plist"

echo "Uninstalling Transcrybe background service..."

# Stop and unload the service
if [ -f "$LAUNCHAGENT_DIR/$LAUNCHAGENT_FILE" ]; then
    echo "Stopping service..."
    launchctl unload "$LAUNCHAGENT_DIR/$LAUNCHAGENT_FILE" 2>/dev/null || true
    
    # Remove the plist file
    rm -f "$LAUNCHAGENT_DIR/$LAUNCHAGENT_FILE"
    echo "LaunchAgent removed."
else
    echo "LaunchAgent not found."
fi

# Kill any running instances
echo "Stopping running instances..."
pkill -f "menubar_transcriber.py" 2>/dev/null || true

echo ""
echo "Background service uninstalled."
echo ""
echo "Note: The Transcrybe.app is still installed in /Applications/"
echo "To completely remove Transcrybe, also run: ./uninstall.sh"