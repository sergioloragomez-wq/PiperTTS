# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-02-23

### Added
- Initial release of STT Configuration for Vicidial
- AGI script (`agi/vicidial_stt.py`) for Asterisk integration
  - Full Vosk STT engine integration
  - Spanish language support
  - Confidence threshold validation
  - Comprehensive error handling and logging
- Configuration system (`config/stt_config.ini`)
  - Flexible INI-based configuration
  - Support for multiple STT engines
  - Performance tuning options
  - Output format customization
- Installation scripts
  - Automated installation script (`scripts/install.sh`)
  - System verification script (`scripts/test.sh`)
  - Python configuration tester (`scripts/test_config.py`)
- Documentation
  - Comprehensive Spanish documentation (`docs/README_ES.md`)
  - English documentation (`docs/README_EN.md`)
  - Main README with quick start guide
- Examples
  - Asterisk dialplan examples (`examples/extensions.conf`)
  - IVR implementation example
  - Survey automation example
  - Basic call flow example
- Project infrastructure
  - Python dependencies file (`requirements.txt`)
  - Git ignore file (`.gitignore`)
  - MIT License (`LICENSE`)

### Features
- Speech-to-Text transcription for Vicidial calls
- Real-time audio processing
- Variable confidence threshold
- Multi-language support (configured for Spanish)
- Detailed logging system
- Easy integration with existing Vicidial installations
- Production-ready configuration

### Technical Details
- Python 3.6+ support
- Vosk STT engine integration
- Asterisk AGI protocol implementation
- INI-based configuration management
- Modular and extensible architecture
