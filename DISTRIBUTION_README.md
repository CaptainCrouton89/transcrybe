# Transcrybe - Local Speech-to-Text for macOS

Transcrybe is a macOS menu bar application that provides system-wide speech-to-text transcription using OpenAI Whisper. Simply press **Cmd+Shift+Space** to record speech and automatically paste the transcribed text into any application.

## Requirements

- **macOS 10.15 (Catalina)** or later  
- **Python 3.8+** - Install from [python.org](https://www.python.org/downloads/) if not already installed

## Installation

1. **Extract** the Transcrybe distribution folder
2. **Run the installer**:
   ```bash
   ./install.sh
   ```
3. **Grant permissions** when macOS prompts you:
   - Microphone access (for recording speech)
   - Accessibility access (for pasting text)
   - Input monitoring (for global hotkey)

## Usage

1. **Launch** Transcrybe from Applications folder or Spotlight
2. **Look for** the microphone icon (🎙️) in your menu bar
3. **Press** `Cmd+Shift+Space` to start recording
4. **Speak** your text (the icon changes to 🔴)
5. **Press** `Cmd+Shift+Space` again to stop and transcribe
6. **Text** is automatically pasted where your cursor is

## Features

- **System-wide**: Works in any application (Mail, Slack, Documents, etc.)
- **Local processing**: All transcription happens on your Mac (no internet required after initial setup)
- **Fast & accurate**: Powered by OpenAI Whisper
- **Fallback pasting**: Multiple methods ensure text gets pasted reliably
- **Menu bar integration**: Minimal, unobtrusive interface

## Troubleshooting

### App won't start
- Ensure Python 3 is installed: `python3 --version`
- Try running from Terminal: `/Applications/Transcrybe.app/Contents/MacOS/Transcrybe`

### Permissions issues
1. Go to **System Settings** → **Privacy & Security**
2. Grant permissions for:
   - **Microphone** → Add Transcrybe
   - **Accessibility** → Add Transcrybe  
   - **Input Monitoring** → Add Transcrybe
3. Restart Transcrybe

### Hotkey not working
- Check Input Monitoring permission is granted
- Try clicking "Request Permissions" in the Transcrybe menu
- **If still not working**: Use the included `launch_with_permissions.sh` script:
  ```bash
  ./launch_with_permissions.sh
  ```

### Auto-paste not working
- Grant Accessibility permission
- Some apps may require additional permissions

### Python dependencies missing
The app will automatically install required Python packages on first run. If this fails:
```bash
pip3 install -r /Applications/Transcrybe.app/Contents/Resources/requirements.txt
```

## Uninstallation

Run the uninstaller:
```bash
./uninstall.sh
```

Or manually:
```bash
rm -rf /Applications/Transcrybe.app
rm -f ~/Library/LaunchAgents/com.transcrybe.app.plist
launchctl unload ~/Library/LaunchAgents/com.transcrybe.app.plist
```

## Support

- Check logs: Menu bar → Transcrybe → "Show Log File"
- The app logs to: `~/Library/Logs/Transcrybe/`

---

**Privacy**: Transcrybe processes all audio locally on your Mac. No data is sent to external servers.