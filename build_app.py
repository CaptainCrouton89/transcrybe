#!/usr/bin/env python3
"""
Build script for creating a standalone Transcrybe.app bundle
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def run_command(cmd, check=True):
    """Run a shell command"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        sys.exit(1)
    return result

def create_app_bundle():
    """Create the .app bundle structure"""
    print("Creating Transcrybe.app bundle...")
    
    app_name = "Transcrybe.app"
    bundle_dir = Path(app_name)
    contents_dir = bundle_dir / "Contents"
    macos_dir = contents_dir / "MacOS"
    resources_dir = contents_dir / "Resources"
    
    # Clean up existing bundle
    if bundle_dir.exists():
        shutil.rmtree(bundle_dir)
    
    # Create directory structure
    macos_dir.mkdir(parents=True)
    resources_dir.mkdir(parents=True)
    
    # Copy Info.plist
    info_plist_content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Transcrybe</string>
    <key>CFBundleIdentifier</key>
    <string>com.silas.transcrybe</string>
    <key>CFBundleName</key>
    <string>Transcrybe</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSUIElement</key>
    <true/>
    <key>NSMicrophoneUsageDescription</key>
    <string>Transcrybe needs microphone access to record speech for transcription.</string>
    <key>NSAppleEventsUsageDescription</key>
    <string>Transcrybe needs to simulate keystrokes to paste transcribed text.</string>
    <key>NSAccessibilityUsageDescription</key>
    <string>Transcrybe needs accessibility access to paste transcribed text into any application.</string>
    <key>NSSystemAdministrationUsageDescription</key>
    <string>Transcrybe needs input monitoring to detect the global hotkey (Cmd+Shift+Space).</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>CFBundleDocumentTypes</key>
    <array/>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.productivity</string>
</dict>
</plist>'''
    
    with open(contents_dir / "Info.plist", "w") as f:
        f.write(info_plist_content)
    
    # Create launcher script
    launcher_script = '''#!/bin/bash
# Transcrybe app launcher

# Get the directory containing this script (MacOS directory)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# Go up one level to Contents directory  
CONTENTS_DIR="$(dirname "$SCRIPT_DIR")"
RESOURCES_DIR="$CONTENTS_DIR/Resources"

# Find Python executable - prioritize pyenv
find_python() {
    # First try pyenv python (where packages are likely installed)
    if [ -f "$HOME/.pyenv/versions/3.11.1/bin/python3" ]; then
        echo "$HOME/.pyenv/versions/3.11.1/bin/python3"
        return 0
    fi
    
    # Try other common locations
    for python_cmd in python3 /usr/bin/python3 /usr/local/bin/python3 /opt/homebrew/bin/python3; do
        if command -v "$python_cmd" &> /dev/null; then
            echo "$python_cmd"
            return 0
        fi
    done
    
    osascript -e "display dialog \\"Python 3 is required but not found. Please install Python 3 from python.org and try again.\\" with title \\"Transcrybe - Missing Python\\" buttons {\\"OK\\"} default button \\"OK\\""
    exit 1
}

# Install requirements if needed
install_requirements() {
    local python_cmd="$1"
    local requirements_file="$RESOURCES_DIR/requirements.txt"
    
    if [ -f "$requirements_file" ]; then
        echo "Installing Python dependencies..."
        "$python_cmd" -m pip install --user -q -r "$requirements_file" 2>/dev/null || {
            osascript -e "display dialog \\"Failed to install required Python packages. Please ensure pip is installed and try again.\\" with title \\"Transcrybe - Installation Error\\" buttons {\\"OK\\"} default button \\"OK\\""
            exit 1
        }
    fi
}

# Check for menubar_transcriber.py in Resources
PYTHON_SCRIPT="$RESOURCES_DIR/menubar_transcriber.py"
if [ ! -f "$PYTHON_SCRIPT" ]; then
    osascript -e "display dialog \\"Application files are missing or corrupted. Please reinstall Transcrybe.\\" with title \\"Transcrybe - Error\\" buttons {\\"OK\\"} default button \\"OK\\""
    exit 1
fi

# Find and launch with Python
PYTHON_CMD=$(find_python)

# Install requirements on first run
install_requirements "$PYTHON_CMD"

# Launch the application
exec "$PYTHON_CMD" "$PYTHON_SCRIPT"
'''
    
    launcher_path = macos_dir / "Transcrybe"
    with open(launcher_path, "w") as f:
        f.write(launcher_script)
    
    # Make launcher executable
    os.chmod(launcher_path, 0o755)
    
    # Copy Python script and requirements
    shutil.copy2("menubar_transcriber.py", resources_dir)
    shutil.copy2("requirements.txt", resources_dir)
    
    print(f"Created {app_name} bundle successfully!")
    return bundle_dir

def create_installer():
    """Create an installer script"""
    installer_script = '''#!/bin/bash
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
'''
    
    with open("install.sh", "w") as f:
        f.write(installer_script)
    os.chmod("install.sh", 0o755)
    
    print("Created install.sh installer script!")

def create_uninstaller():
    """Create an uninstaller script"""
    uninstaller_script = '''#!/bin/bash
# Transcrybe Uninstaller

APP_NAME="Transcrybe.app"
INSTALL_DIR="/Applications"

echo "Uninstalling Transcrybe..."

# Remove app bundle
if [ -d "$INSTALL_DIR/$APP_NAME" ]; then
    echo "Removing $INSTALL_DIR/$APP_NAME..."
    rm -rf "$INSTALL_DIR/$APP_NAME"
    echo "Transcrybe has been uninstalled."
else
    echo "Transcrybe is not installed in $INSTALL_DIR"
fi

# Remove logs (optional)
LOG_DIR="$HOME/Library/Logs/Transcrybe"
if [ -d "$LOG_DIR" ]; then
    read -p "Remove log files in $LOG_DIR? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$LOG_DIR"
        echo "Log files removed."
    fi
fi

echo "Uninstallation complete!"
'''
    
    with open("uninstall.sh", "w") as f:
        f.write(uninstaller_script)
    os.chmod("uninstall.sh", 0o755)
    
    print("Created uninstall.sh uninstaller script!")

def main():
    """Main build process"""
    print("Building Transcrybe standalone app...")
    
    # Check requirements
    if not Path("menubar_transcriber.py").exists():
        print("Error: menubar_transcriber.py not found!")
        sys.exit(1)
    
    if not Path("requirements.txt").exists():
        print("Error: requirements.txt not found!")
        sys.exit(1)
    
    # Create app bundle
    bundle_dir = create_app_bundle()
    
    # Create installer/uninstaller
    create_installer()
    create_uninstaller()
    
    print("\nBuild complete! Files created:")
    print(f"• {bundle_dir} - The application bundle")
    print("• install.sh - Installer script")  
    print("• uninstall.sh - Uninstaller script")
    print("\nTo install: ./install.sh")
    print("To test locally: open Transcrybe.app")

if __name__ == "__main__":
    main()