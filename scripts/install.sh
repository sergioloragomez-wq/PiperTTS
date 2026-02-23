#!/bin/bash
# Installation script for STT Vicidial integration

set -e

echo "========================================="
echo "STT for Vicidial - Installation Script"
echo "========================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root or with sudo"
    exit 1
fi

# Install system dependencies
echo "Installing system dependencies..."
apt-get update
apt-get install -y python3 python3-pip python3-venv wget unzip sox

# Create Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv /opt/vicidial-stt-env
source /opt/vicidial-stt-env/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install vosk pyst2 configparser

# Create necessary directories
echo "Creating directories..."
mkdir -p /var/lib/asterisk/agi-bin
mkdir -p /var/lib/asterisk/models
mkdir -p /var/log/asterisk/stt
mkdir -p /var/spool/asterisk/monitor

# Download Vosk model (Spanish)
echo "Downloading Spanish STT model..."
MODEL_URL="https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip"
MODEL_DIR="/var/lib/asterisk/models"

if [ ! -d "$MODEL_DIR/vosk-model-small-es-0.42" ]; then
    cd "$MODEL_DIR"
    wget "$MODEL_URL" -O vosk-model.zip
    unzip vosk-model.zip
    rm vosk-model.zip
    echo "Model downloaded and extracted"
else
    echo "Model already exists, skipping download"
fi

# Copy AGI script
echo "Installing AGI script..."
cp agi/vicidial_stt.py /var/lib/asterisk/agi-bin/
chmod +x /var/lib/asterisk/agi-bin/vicidial_stt.py

# Update shebang in AGI script to use virtual environment
sed -i "1s|.*|#!/opt/vicidial-stt-env/bin/python3|" /var/lib/asterisk/agi-bin/vicidial_stt.py

# Copy configuration
echo "Installing configuration..."
mkdir -p /etc/asterisk/stt
cp config/stt_config.ini /etc/asterisk/stt/

# Update config paths
sed -i "s|/home/runner/work/PiperTTS/PiperTTS/config/stt_config.ini|/etc/asterisk/stt/stt_config.ini|g" /var/lib/asterisk/agi-bin/vicidial_stt.py
sed -i "s|/var/lib/asterisk/models/vosk-model-es-0.42|$MODEL_DIR/vosk-model-small-es-0.42|g" /etc/asterisk/stt/stt_config.ini

# Set permissions
echo "Setting permissions..."
chown -R asterisk:asterisk /var/lib/asterisk/agi-bin
chown -R asterisk:asterisk /var/log/asterisk/stt
chown -R asterisk:asterisk /var/spool/asterisk/monitor
chown -R asterisk:asterisk /var/lib/asterisk/models

echo ""
echo "========================================="
echo "Installation completed successfully!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Edit /etc/asterisk/stt/stt_config.ini if needed"
echo "2. Add AGI call to your Vicidial dialplan"
echo "3. Test with: asterisk -rx 'agi debug on'"
echo ""
echo "Example dialplan entry:"
echo "  exten => _X.,1,AGI(vicidial_stt.py)"
echo "  exten => _X.,n,NoOp(STT Result: \${STT_TEXT})"
echo "  exten => _X.,n,NoOp(Confidence: \${STT_CONFIDENCE})"
echo ""
