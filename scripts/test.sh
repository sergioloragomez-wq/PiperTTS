#!/bin/bash
# Test script for STT functionality

echo "Testing STT Configuration..."

# Check Python dependencies
echo "Checking Python dependencies..."
python3 -c "import vosk" 2>/dev/null && echo "✓ Vosk installed" || echo "✗ Vosk not installed"
python3 -c "from asterisk.agi import AGI" 2>/dev/null && echo "✓ AGI library installed" || echo "✗ AGI library not installed"

# Check directories
echo ""
echo "Checking directories..."
[ -d "/var/lib/asterisk/agi-bin" ] && echo "✓ AGI directory exists" || echo "✗ AGI directory missing"
[ -d "/var/log/asterisk/stt" ] && echo "✓ Log directory exists" || echo "✗ Log directory missing"
[ -d "/var/lib/asterisk/models" ] && echo "✓ Models directory exists" || echo "✗ Models directory missing"

# Check files
echo ""
echo "Checking files..."
[ -f "/var/lib/asterisk/agi-bin/vicidial_stt.py" ] && echo "✓ AGI script exists" || echo "✗ AGI script missing"
[ -f "/etc/asterisk/stt/stt_config.ini" ] && echo "✓ Config file exists" || echo "✗ Config file missing"

# Check model
echo ""
echo "Checking STT model..."
if [ -d "/var/lib/asterisk/models/vosk-model-small-es-0.42" ]; then
    echo "✓ Spanish model installed"
else
    echo "✗ Spanish model not found"
fi

echo ""
echo "Test complete!"
