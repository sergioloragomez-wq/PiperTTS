#!/usr/bin/env python3
"""
Vicidial STT AGI Script
Speech-to-Text integration for Vicidial using Vosk/other STT engines
"""

import sys
import os
import json
import logging
from configparser import ConfigParser
from pathlib import Path

# Import AGI library
try:
    from asterisk.agi import AGI
except ImportError:
    print("Error: asterisk-agi library not installed")
    print("Install with: pip install pyst2")
    sys.exit(1)

# Import STT engine
try:
    from vosk import Model, KaldiRecognizer
except ImportError:
    print("Error: vosk library not installed")
    print("Install with: pip install vosk")
    sys.exit(1)


class VicidialSTT:
    """Vicidial Speech-to-Text Handler"""
    
    def __init__(self, config_path='/home/runner/work/PiperTTS/PiperTTS/config/stt_config.ini'):
        """Initialize STT handler with configuration"""
        self.config = ConfigParser()
        self.config.read(config_path)
        
        # Setup logging
        log_path = self.config.get('vicidial', 'log_path', fallback='/var/log/asterisk/stt')
        Path(log_path).mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            filename=f"{log_path}/vicidial_stt.log",
            level=getattr(logging, self.config.get('vicidial', 'log_level', fallback='INFO')),
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Load STT model
        model_path = self.config.get('general', 'model_path')
        self.sample_rate = int(self.config.get('general', 'sample_rate', fallback=8000))
        
        try:
            self.model = Model(model_path)
            self.logger.info(f"STT Model loaded from {model_path}")
        except Exception as e:
            self.logger.error(f"Failed to load STT model: {e}")
            raise
    
    def transcribe_audio(self, audio_file):
        """Transcribe audio file to text"""
        try:
            import wave
            
            wf = wave.open(audio_file, "rb")
            
            # Validate audio format
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
                self.logger.error("Audio file must be WAV format mono PCM")
                return None
            
            rec = KaldiRecognizer(self.model, wf.getframerate())
            rec.SetMaxAlternatives(int(self.config.get('vosk', 'alternatives', fallback=3)))
            rec.SetWords(self.config.getboolean('output', 'enable_timestamps', fallback=True))
            
            results = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    results.append(result)
            
            # Get final result
            final_result = json.loads(rec.FinalResult())
            results.append(final_result)
            
            wf.close()
            
            # Extract text from results
            text = " ".join([r.get('text', '') for r in results if r.get('text')])
            confidence = final_result.get('confidence', 0.0)
            
            self.logger.info(f"Transcription: {text} (confidence: {confidence})")
            
            return {
                'text': text,
                'confidence': confidence,
                'full_results': results
            }
            
        except Exception as e:
            self.logger.error(f"Transcription error: {e}")
            return None
    
    def process_call(self, agi):
        """Process incoming call for STT"""
        try:
            # Get call variables
            call_id = agi.get_variable('UNIQUEID')
            campaign = agi.get_variable('campaign')
            
            self.logger.info(f"Processing call {call_id} from campaign {campaign}")
            
            # Record audio for transcription
            recording_path = self.config.get('vicidial', 'recording_path', 
                                           fallback='/var/spool/asterisk/monitor')
            audio_file = f"{recording_path}/stt_{call_id}.wav"
            
            # Record the caller's speech
            timeout = int(self.config.get('performance', 'timeout', fallback=30))
            max_duration = int(self.config.get('performance', 'max_recording_duration', fallback=300))
            
            agi.appexec('Playback', 'beep')  # Signal to start speaking
            agi.appexec('Record', f"{audio_file}:wav,{max_duration},{timeout}")
            
            # Check if file was created
            if not os.path.exists(audio_file):
                self.logger.error(f"Recording file not created: {audio_file}")
                agi.set_variable('STT_STATUS', 'FAILED')
                agi.set_variable('STT_ERROR', 'NO_RECORDING')
                return
            
            # Transcribe
            result = self.transcribe_audio(audio_file)
            
            if result and result.get('text'):
                confidence_threshold = float(self.config.get('output', 'confidence_threshold', 
                                                            fallback=0.5))
                
                if result['confidence'] >= confidence_threshold:
                    agi.set_variable('STT_TEXT', result['text'])
                    agi.set_variable('STT_CONFIDENCE', str(result['confidence']))
                    agi.set_variable('STT_STATUS', 'SUCCESS')
                    self.logger.info(f"STT Success: {result['text']}")
                else:
                    agi.set_variable('STT_STATUS', 'LOW_CONFIDENCE')
                    agi.set_variable('STT_CONFIDENCE', str(result['confidence']))
                    self.logger.warning(f"Low confidence: {result['confidence']}")
            else:
                agi.set_variable('STT_STATUS', 'FAILED')
                agi.set_variable('STT_ERROR', 'NO_TRANSCRIPTION')
                self.logger.error("Transcription failed")
            
            # Cleanup recording file if configured
            if not self.config.getboolean('vicidial', 'keep_recordings', fallback=False):
                try:
                    os.remove(audio_file)
                except:
                    pass
                    
        except Exception as e:
            self.logger.error(f"Error processing call: {e}")
            agi.set_variable('STT_STATUS', 'ERROR')
            agi.set_variable('STT_ERROR', str(e))


def main():
    """Main entry point for AGI script"""
    try:
        agi = AGI()
        stt_handler = VicidialSTT()
        stt_handler.process_call(agi)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
