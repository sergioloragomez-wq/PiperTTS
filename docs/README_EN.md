# STT Configuration for Vicidial

This project provides a Speech-to-Text (STT) integration for Vicidial using the Vosk engine.

## Features

- ✅ Complete Vicidial integration via AGI scripts
- ✅ Spanish voice recognition support
- ✅ High-performance Vosk STT engine
- ✅ Flexible configuration via INI file
- ✅ Detailed logging of all transcriptions
- ✅ Confidence handling to validate transcriptions
- ✅ Compatible with Asterisk and Vicidial

## System Requirements

- Ubuntu/Debian Linux
- Python 3.6 or higher
- Asterisk 13+ with Vicidial
- At least 2GB RAM
- 1GB disk space for STT models

## Installation

### Automatic Installation

```bash
sudo chmod +x scripts/install.sh
sudo ./scripts/install.sh
```

### Manual Installation

1. **Install system dependencies:**
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv wget unzip sox
```

2. **Create Python virtual environment:**
```bash
python3 -m venv /opt/vicidial-stt-env
source /opt/vicidial-stt-env/bin/activate
```

3. **Install Python dependencies:**
```bash
pip install --upgrade pip
pip install vosk pyst2 configparser
```

4. **Create necessary directories:**
```bash
sudo mkdir -p /var/lib/asterisk/agi-bin
sudo mkdir -p /var/lib/asterisk/models
sudo mkdir -p /var/log/asterisk/stt
sudo mkdir -p /var/spool/asterisk/monitor
```

5. **Download Spanish STT model:**
```bash
cd /var/lib/asterisk/models
wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
unzip vosk-model-small-es-0.42.zip
rm vosk-model-small-es-0.42.zip
```

6. **Copy files:**
```bash
sudo cp agi/vicidial_stt.py /var/lib/asterisk/agi-bin/
sudo chmod +x /var/lib/asterisk/agi-bin/vicidial_stt.py
sudo mkdir -p /etc/asterisk/stt
sudo cp config/stt_config.ini /etc/asterisk/stt/
```

7. **Set permissions:**
```bash
sudo chown -R asterisk:asterisk /var/lib/asterisk/agi-bin
sudo chown -R asterisk:asterisk /var/log/asterisk/stt
sudo chown -R asterisk:asterisk /var/lib/asterisk/models
```

## Configuration

### Configuration File

The main configuration file is located at `/etc/asterisk/stt/stt_config.ini`:

```ini
[general]
engine = vosk
model_path = /var/lib/asterisk/models/vosk-model-small-es-0.42
sample_rate = 8000
language = es-ES

[vicidial]
agi_path = /var/lib/asterisk/agi-bin
log_path = /var/log/asterisk/stt
recording_path = /var/spool/asterisk/monitor
enable_logging = true
log_level = INFO
```

### Vicidial Integration

#### Option 1: Add to Asterisk Dialplan

Edit `/etc/asterisk/extensions.conf` or your Vicidial extensions file:

```
[vicidial-stt]
exten => _X.,1,Answer()
exten => _X.,n,Wait(1)
exten => _X.,n,AGI(vicidial_stt.py)
exten => _X.,n,NoOp(STT Status: ${STT_STATUS})
exten => _X.,n,NoOp(Text: ${STT_TEXT})
exten => _X.,n,NoOp(Confidence: ${STT_CONFIDENCE})
exten => _X.,n,GotoIf($["${STT_STATUS}" = "SUCCESS"]?success:failed)
exten => _X.,n(success),Playback(thank-you-for-calling)
exten => _X.,n,Hangup()
exten => _X.,n(failed),Playback(sorry)
exten => _X.,n,Hangup()
```

## Usage

### Available Asterisk Variables

After running the AGI script, the following variables will be available:

- `${STT_STATUS}` - Transcription status: SUCCESS, FAILED, LOW_CONFIDENCE, ERROR
- `${STT_TEXT}` - Transcribed text
- `${STT_CONFIDENCE}` - Confidence level (0.0 - 1.0)
- `${STT_ERROR}` - Error message (if applicable)

## Testing

Run automated tests:

```bash
chmod +x scripts/test.sh
./scripts/test.sh
```

## Troubleshooting

### AGI script doesn't execute
- Check permissions: `ls -la /var/lib/asterisk/agi-bin/vicidial_stt.py`
- Verify the shebang points to the correct Python
- Check Asterisk logs: `tail -f /var/log/asterisk/full`

### Low transcription quality
- Use a larger model
- Adjust `confidence_threshold` in configuration
- Verify audio input quality
- Use audio with 8000 Hz or 16000 Hz sample rate

## Logs

Logs are saved in:
- Main: `/var/log/asterisk/stt/vicidial_stt.log`
- Asterisk: `/var/log/asterisk/full`

## License

This project is licensed under the MIT License.

## Credits

- STT Engine: [Vosk](https://alphacephei.com/vosk/)
- Telephony: [Asterisk](https://www.asterisk.org/)
- Call Center: [Vicidial](https://vicidial.org/)
