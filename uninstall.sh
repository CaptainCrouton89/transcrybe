#!/bin/bash

echo "Uninstalling Transcrybe..."

# Stop and unload LaunchAgent
echo "Stopping auto-start service..."
launchctl unload "$HOME/Library/LaunchAgents/com.transcrybe.app.plist" 2>/dev/null

# Remove LaunchAgent
echo "Removing auto-start configuration..."
rm -f "$HOME/Library/LaunchAgents/com.transcrybe.app.plist"

# Remove app from Applications
echo "Removing application..."
rm -rf "/Applications/Transcrybe.app"

echo "Transcrybe has been completely uninstalled."