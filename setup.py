#!/usr/bin/env python3
"""
Setup script for Transcrybe - macOS menu bar speech-to-text transcriber
"""

from setuptools import setup, find_packages
import os

def read_requirements():
    """Read requirements.txt file"""
    with open('requirements.txt', 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def get_version():
    """Get version from app"""
    return "1.0.0"

setup(
    name="transcrybe",
    version=get_version(),
    description="macOS menu bar speech-to-text transcriber using OpenAI Whisper",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Silas Rhyneer",
    python_requires=">=3.8",
    install_requires=read_requirements(),
    py_modules=["menubar_transcriber"],
    entry_points={
        'console_scripts': [
            'transcrybe=menubar_transcriber:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: MacOS X",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Utilities",
    ],
    keywords="speech-to-text whisper macos transcription menubar",
)