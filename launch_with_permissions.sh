#!/bin/bash
# Launch Transcrybe with proper permissions
# Use this if the regular app doesn't have hotkey permissions

echo "Launching Transcrybe with permissions..."

# Kill any existing instances
pkill -f "menubar_transcriber.py" 2>/dev/null || true

# Wait a moment
sleep 1

# Launch from terminal to ensure proper permissions
/Applications/Transcrybe.app/Contents/MacOS/Transcrybe &

echo "Transcrybe launched! The hotkey (Cmd+Shift+Space) should now work."
echo "Look for the microphone icon (🎙️) in your menu bar."