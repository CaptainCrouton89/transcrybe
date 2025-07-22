#!/bin/bash
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
