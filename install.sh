#!/bin/bash

echo "Installing Transcrybe..."

# Copy app to Applications
echo "Copying app to /Applications..."
if [ -d "/Applications/Transcrybe.app" ]; then
    echo "Removing existing installation..."
    rm -rf "/Applications/Transcrybe.app"
fi
cp -R "Transcrybe.app" "/Applications/"

# Copy Python script to app bundle
echo "Copying Python script..."
cp "menubar_transcriber.py" "/Applications/Transcrybe.app/Contents/Resources/"

# Update the launch script to use the correct path
cat > "/Applications/Transcrybe.app/Contents/MacOS/Transcrybe" << 'EOF'
#!/bin/bash

# Get the directory where the app bundle is located
APP_DIR="/Applications/Transcrybe.app/Contents/Resources"

# Change to the app directory
cd "$APP_DIR"

# Run the Python script
exec python3 "$APP_DIR/menubar_transcriber.py"
EOF

chmod +x "/Applications/Transcrybe.app/Contents/MacOS/Transcrybe"

# Install LaunchAgent for auto-start
echo "Setting up auto-start..."
mkdir -p "$HOME/Library/LaunchAgents"
cp "com.transcrybe.app.plist" "$HOME/Library/LaunchAgents/"

# Load the LaunchAgent
launchctl unload "$HOME/Library/LaunchAgents/com.transcrybe.app.plist" 2>/dev/null
launchctl load "$HOME/Library/LaunchAgents/com.transcrybe.app.plist"

echo "Installation complete!"
echo ""
echo "Transcrybe has been installed and will start automatically on login."
echo "You can start it now by running:"
echo "  open /Applications/Transcrybe.app"
echo ""
echo "To uninstall later:"
echo "  launchctl unload ~/Library/LaunchAgents/com.transcrybe.app.plist"
echo "  rm ~/Library/LaunchAgents/com.transcrybe.app.plist"
echo "  rm -rf /Applications/Transcrybe.app"