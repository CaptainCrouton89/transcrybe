#!/bin/bash
# Install Transcrybe as a background service that auto-starts

set -e

LAUNCHAGENT_DIR="$HOME/Library/LaunchAgents"
LAUNCHAGENT_FILE="com.silas.transcrybe.plist"
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing Transcrybe background service..."

# Create LaunchAgents directory if it doesn't exist
mkdir -p "$LAUNCHAGENT_DIR"

# Stop any existing service
echo "Stopping existing service..."
launchctl unload "$LAUNCHAGENT_DIR/$LAUNCHAGENT_FILE" 2>/dev/null || true

# Kill any running instances
pkill -f "menubar_transcriber.py" 2>/dev/null || true

# Wait for processes to stop
sleep 2

# Copy the plist file
echo "Installing LaunchAgent..."
cp "$CURRENT_DIR/$LAUNCHAGENT_FILE" "$LAUNCHAGENT_DIR/"

# Set proper permissions
chmod 644 "$LAUNCHAGENT_DIR/$LAUNCHAGENT_FILE"

# Load and start the service
echo "Starting background service..."
launchctl load "$LAUNCHAGENT_DIR/$LAUNCHAGENT_FILE"

# Give it a moment to start
sleep 3

# Check if it's running
if pgrep -f "menubar_transcriber.py" > /dev/null; then
    echo "✅ Success! Transcrybe is now running as a background service."
    echo ""
    echo "Service details:"
    echo "• Starts automatically on login"
    echo "• Restarts if it crashes"
    echo "• Look for 🎙️ icon in your menu bar"
    echo "• Use Cmd+Shift+Space to record"
    echo ""
    echo "Logs are available at:"
    echo "• ~/Library/Logs/Transcrybe/"
    echo ""
    echo "To stop the service:"
    echo "  launchctl unload ~/Library/LaunchAgents/$LAUNCHAGENT_FILE"
else
    echo "⚠️ Service installed but may not be running properly."
    echo "Check logs at ~/Library/Logs/Transcrybe/"
fi

echo ""
echo "Installation complete!"