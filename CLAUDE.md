# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Transcrybe is a macOS menu bar application for local speech-to-text transcription using OpenAI Whisper. It provides system-wide transcription that works in any application with a global hotkey (Cmd+Shift+Space).

## Architecture

### Core Components

- **TranscribeApp**: Main rumps-based menu bar application class that orchestrates all functionality
- **Audio Pipeline**: Records audio using sounddevice → saves as WAV → transcribes with Whisper → auto-pastes text
- **Global Hotkey System**: Uses pynput for system-wide Cmd+Shift+Space hotkey detection
- **Multi-method Pasting**: Implements fallback pasting strategies (pynput, Quartz framework) to handle different app contexts
- **Permission Management**: Automatically requests macOS permissions for microphone, accessibility, and input monitoring

### Key Design Patterns

- **Threading Model**: Separates UI thread from blocking operations (model loading, audio recording, transcription)
- **State Management**: Uses instance variables (`is_recording`, `model`, `audio_data`) with thread-safe access patterns
- **Error Handling**: Graceful degradation with user notifications for each failure mode
- **Resource Cleanup**: Temporary file cleanup and proper stream management

### Audio Processing Flow

1. Global hotkey triggers `_toggle_recording()`
2. `_start_recording()` → `_record_audio()` collects audio chunks in background thread
3. Second hotkey press → `_stop_recording()` → `_process_recording()` transcribes and pastes
4. Auto-cleanup of temporary WAV files

## Development Commands

### Setup and Installation
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Run the menu bar app
python3 menubar_transcriber.py
```

### Testing and Development
```bash
# Run with debugging output (view print statements)
python3 menubar_transcriber.py

# Test permissions manually (use menu bar "Request Permissions")
# Test global hotkey: Cmd+Shift+Space
# Test in different apps: TextEdit, Safari, Slack, etc.
```

### Dependencies
- **whisper**: OpenAI Whisper for local speech recognition
- **rumps**: macOS menu bar app framework
- **sounddevice**: Audio recording from microphone
- **pynput**: Global hotkey detection and keyboard simulation
- **pyperclip**: Clipboard operations
- **numpy/scipy**: Audio data processing

## macOS Integration Requirements

### Required Permissions
The app requires three macOS permissions that are automatically requested:
1. **Microphone Access**: For audio recording
2. **Accessibility Access**: For simulating Cmd+V keypresses
3. **Input Monitoring**: For global hotkey detection

### System Integration Points
- Menu bar icon with status indicators (🎙️ ready, 🔴 recording, ⏳ processing)
- Native macOS notifications for status updates
- System-wide paste functionality across all applications
- Quartz framework integration as fallback for keyboard simulation

## Code Patterns

### Thread Safety
- UI updates only on main thread via rumps notifications
- Background threads for blocking operations (model loading, recording, transcription)
- State changes use simple boolean flags with careful ordering

### Error Recovery
- Multiple pasting strategies with graceful fallbacks
- Comprehensive try/catch blocks around system calls
- User-friendly error notifications with actionable guidance
- Resource cleanup in finally blocks

### Performance Considerations
- Whisper model loaded once at startup in background
- Audio recorded in chunks to prevent memory buildup
- Temporary files automatically cleaned up
- 16kHz sampling rate for optimal Whisper performance