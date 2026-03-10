#!/bin/bash
# Installation script for STT Configuration in Vicidial

set -e

echo "==================================="
echo "STT for Vicidial - Installation"
echo "==================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root or with sudo"
    exit 1
fi

# Create necessary directories
echo "Creating directories..."
mkdir -p /var/lib/asterisk/agi-bin
mkdir -p /var/log/asterisk
mkdir -p /etc/asterisk/stt

# Copy configuration file
echo "Installing configuration..."
cp stt_config.conf /etc/asterisk/stt/

# Install Python dependencies
echo "Installing Python dependencies..."
if command -v python3 &> /dev/null; then
    pip3 install --upgrade pip
    pip3 install speechrecognition
    pip3 install pydub
    pip3 install google-cloud-speech
    pip3 install openai-whisper
    pip3 install pymysql
else
    echo "Python3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Copy AGI scripts
echo "Installing AGI scripts..."
if [ -f "asterisk/agi/stt_recognition.py" ]; then
    cp asterisk/agi/stt_recognition.py /var/lib/asterisk/agi-bin/
    chmod +x /var/lib/asterisk/agi-bin/stt_recognition.py
fi

# Set permissions
echo "Setting permissions..."
chown -R asterisk:asterisk /var/lib/asterisk/agi-bin
chown -R asterisk:asterisk /var/log/asterisk
chown -R asterisk:asterisk /etc/asterisk/stt

echo ""
echo "Installation completed!"
echo ""
echo "Next steps:"
echo "1. Configure your STT engine credentials in /etc/asterisk/stt/stt_config.conf"
echo "2. Update Vicidial dialplan to use the STT AGI script"
echo "3. Test the configuration using the test script"
echo ""
echo "For Google Cloud Speech API:"
echo "  - Place your credentials JSON file at /etc/asterisk/google-credentials.json"
echo ""
echo "For Whisper:"
echo "  - Models will be downloaded automatically on first use"
echo ""
