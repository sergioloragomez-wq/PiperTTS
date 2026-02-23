#!/bin/bash
# Quick setup script for testing STT configuration locally

echo "STT Configuration Quick Test Setup"
echo "===================================="
echo ""

# Create local test directories
mkdir -p test_environment/recordings
mkdir -p test_environment/logs
mkdir -p test_environment/config

# Copy configuration to test environment
cp stt_config.conf test_environment/config/

echo "Test environment created in ./test_environment/"
echo ""
echo "Directory structure:"
tree test_environment/ 2>/dev/null || ls -R test_environment/
echo ""

# Create a simple test audio file info
cat > test_environment/README.txt << 'EOF'
STT Test Environment
====================

This directory contains a test environment for STT configuration.

Directories:
- recordings/  : Place test audio files here (.wav format)
- logs/       : Test logs will be stored here
- config/     : Configuration files

To test STT recognition:
1. Place a .wav audio file in recordings/
2. Run: python3 ../asterisk/agi/stt_recognition.py

Note: You'll need to modify the script to run in standalone mode
for testing outside of Asterisk.
EOF

echo "Created test environment structure"
echo ""
echo "Next steps:"
echo "1. Place test audio files in test_environment/recordings/"
echo "2. Configure your STT engine credentials"
echo "3. Run test_stt_config.py to verify setup"
echo ""
