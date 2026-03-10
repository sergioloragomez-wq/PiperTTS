# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-02-23

### Added
- Initial release of STT configuration for Vicidial
- Main configuration file (`stt_config.conf`) with support for multiple STT engines
- Installation script (`install.sh`) for automated setup
- AGI script (`asterisk/agi/stt_recognition.py`) for Asterisk integration
- Dialplan examples (`asterisk/extensions_stt.conf`) for common use cases
- Test script (`test_stt_config.py`) for validating configuration
- Comprehensive documentation in Spanish (`DOCUMENTACION.md`)
- Usage guide with practical examples (`GUIA_USO.md`)
- Python requirements file (`requirements.txt`)
- Example configurations:
  - English language configuration
  - Whisper offline engine configuration
  - Google Cloud credentials template
- Support for multiple STT engines:
  - Google Cloud Speech API
  - OpenAI Whisper (offline)
  - CMU Sphinx
- Database integration for storing transcriptions
- Logging and monitoring capabilities
- Multi-language support (Spanish, English, Portuguese, etc.)

### Features
- Automatic call transcription
- Post-call survey with voice responses
- Voice-enabled IVR menus
- Voicemail transcription
- Voice-based data verification
- Batch processing capabilities
- Quality monitoring tools

### Documentation
- Complete README in Spanish
- Detailed installation instructions
- Configuration guide
- Usage examples for common scenarios
- Database query examples
- Troubleshooting guide
- Best practices recommendations

[1.0.0]: https://github.com/sergioloragomez-wq/PiperTTS/releases/tag/v1.0.0
