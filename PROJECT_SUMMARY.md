# STT Configuration for Vicidial - Project Summary

## Project Overview

This repository contains a complete Speech-to-Text (STT) solution for Vicidial call center software, using the Vosk engine for high-quality voice recognition in Spanish.

## What This Project Provides

### 1. Core Components

#### AGI Script (`agi/vicidial_stt.py`)
- Main integration script for Asterisk/Vicidial
- Handles audio recording from calls
- Performs real-time speech-to-text transcription
- Returns results via Asterisk variables
- Comprehensive error handling and logging

#### Configuration (`config/stt_config.ini`)
- Centralized configuration management
- Supports multiple STT engines
- Performance tuning parameters
- Adjustable quality thresholds

### 2. Installation & Deployment

#### Automated Installation (`scripts/install.sh`)
- One-command installation
- Handles all dependencies
- Downloads required STT models
- Configures permissions
- Sets up directory structure

#### Testing Tools
- `scripts/test.sh` - System verification
- `scripts/test_config.py` - Python configuration validator

### 3. Documentation

#### Spanish Documentation (`docs/README_ES.md`)
- Complete installation guide
- Configuration reference
- Usage examples
- Troubleshooting guide
- Performance optimization tips

#### English Documentation (`docs/README_EN.md`)
- Full documentation in English
- Installation procedures
- Configuration options
- Usage examples

### 4. Examples (`examples/extensions.conf`)

Three ready-to-use dialplan configurations:
1. **Basic STT Call Flow** - Simple transcription example
2. **IVR with Voice Recognition** - Interactive menu system
3. **Automated Survey** - Customer satisfaction survey

## Key Features

✅ **Easy Installation**: Single script installation
✅ **Production Ready**: Tested configuration for call centers
✅ **Spanish Support**: Optimized for Spanish language
✅ **Flexible**: Easy to configure and extend
✅ **Logging**: Comprehensive logging for debugging
✅ **Error Handling**: Robust error detection and recovery
✅ **Quality Control**: Confidence thresholds for accuracy

## Technical Stack

- **Language**: Python 3.6+
- **STT Engine**: Vosk (offline, high performance)
- **Telephony**: Asterisk AGI
- **Integration**: Vicidial call center suite
- **Audio**: 8kHz/16kHz WAV format

## File Structure

```
PiperTTS/
├── agi/
│   └── vicidial_stt.py          # Main AGI script
├── config/
│   └── stt_config.ini           # Configuration file
├── scripts/
│   ├── install.sh               # Installation script
│   ├── test.sh                  # System test
│   └── test_config.py           # Configuration test
├── docs/
│   ├── README_ES.md             # Spanish docs
│   └── README_EN.md             # English docs
├── examples/
│   └── extensions.conf          # Dialplan examples
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── LICENSE                      # MIT License
├── CHANGELOG.md                 # Version history
└── README.md                    # Main readme
```

## Quick Start

```bash
# Clone the repository
git clone https://github.com/sergioloragomez-wq/PiperTTS.git
cd PiperTTS

# Run installation (requires root)
sudo ./scripts/install.sh

# Configure your Asterisk dialplan
# See examples/extensions.conf for examples

# Test the installation
./scripts/test.sh
```

## Integration Points

### Asterisk Variables Set by STT Script

After execution, these variables are available:
- `${STT_STATUS}` - SUCCESS, FAILED, LOW_CONFIDENCE, ERROR
- `${STT_TEXT}` - Transcribed text
- `${STT_CONFIDENCE}` - Confidence score (0.0-1.0)
- `${STT_ERROR}` - Error details (if any)

### Configuration Sections

1. **[general]** - STT engine settings
2. **[vicidial]** - Vicidial integration paths
3. **[vosk]** - Vosk engine parameters
4. **[performance]** - Performance tuning
5. **[output]** - Output formatting

## Use Cases

1. **IVR Systems**: Voice-driven menu navigation
2. **Customer Surveys**: Automated feedback collection
3. **Call Routing**: Route calls based on spoken keywords
4. **Quality Assurance**: Transcribe calls for analysis
5. **Data Collection**: Capture spoken information

## Requirements

- Ubuntu/Debian Linux
- Python 3.6+
- Asterisk 13+ with Vicidial
- 2GB RAM minimum
- 1GB disk space for models
- Root access for installation

## Support & Contribution

- **Issues**: Report bugs via GitHub Issues
- **Documentation**: See `docs/` directory
- **Examples**: See `examples/` directory
- **Contributing**: Pull requests welcome

## License

MIT License - See LICENSE file for details

## Credits

- **Vosk**: STT engine (https://alphacephei.com/vosk/)
- **Asterisk**: Telephony platform (https://www.asterisk.org/)
- **Vicidial**: Call center software (https://vicidial.org/)

---

**Version**: 1.0.0  
**Last Updated**: 2026-02-23  
**Language**: Spanish (configurable for other languages)
