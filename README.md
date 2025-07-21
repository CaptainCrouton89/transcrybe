# 🎙️ Transcrybe - Local Speech-to-Text Menu Bar App

A local, privacy-focused speech-to-text transcriber that lives in your macOS menu bar and works system-wide in any application.

## Features

- **🔒 100% Local**: Uses OpenAI Whisper locally, no internet required
- **🌍 System-wide**: Works in any app - Safari, Slack, TextEdit, etc.
- **⚡ Fast**: Instant transcription with auto-paste
- **📱 Menu Bar App**: Clean interface, always accessible
- **🎯 Simple**: Just press Cmd+Shift+Space to record and transcribe
- **🔐 Private**: All audio processing happens on your machine

## Quick Start

1. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Run the menu bar app**:
   ```bash
   python3 menubar_transcriber.py
   ```

3. **Grant permissions** when prompted:
   - Microphone access
   - Accessibility access  
   - Input Monitoring access

4. **Use anywhere**:
   - Press `Cmd+Shift+Space` to start recording (🔴 appears in menu bar)
   - Speak your text
   - Press `Cmd+Shift+Space` again to stop and transcribe
   - Text automatically pastes at your cursor!

## Menu Bar Features

- **🎙️ Icon**: Shows recording status (🎙️ ready, 🔴 recording, ⏳ processing)
- **Click menu**: Start recording, request permissions, settings, quit
- **Notifications**: Real-time status updates

## Requirements

- macOS (tested on macOS Monterey+)
- Python 3.7+
- Dependencies in requirements.txt

## Permissions Needed

The app will automatically request:
- **Microphone**: To record your speech
- **Accessibility**: To paste text in other applications
- **Input Monitoring**: To detect global hotkey

You can also click "Request Permissions" in the menu bar menu.

## How It Works

1. Menu bar app runs in background
2. Global hotkey listener detects Cmd+Shift+Space
3. Records audio from microphone
4. Transcribes using local Whisper model
5. Auto-pastes text at cursor using multiple methods

## Troubleshooting

- **Menu bar app not appearing**: Check if Python process is running
- **No permissions dialog**: Click menu bar icon → "Request Permissions"
- **Auto-paste not working**: Ensure all three permissions are granted
- **No transcription**: Check microphone permissions and try speaking louder