#!/usr/bin/env python3
"""
STT Recognition AGI Script for Vicidial/Asterisk
This script performs speech-to-text recognition on audio files
"""

import sys
import os
import configparser
import logging
from datetime import datetime

try:
    import speech_recognition as sr
except ImportError:
    print("ERROR: speech_recognition module not installed")
    sys.exit(1)


class AGI:
    """Simple AGI class for Asterisk communication"""
    
    def __init__(self):
        self.env = {}
        self._read_environment()
    
    def _read_environment(self):
        """Read AGI environment variables"""
        while True:
            line = sys.stdin.readline().strip()
            if not line:
                break
            key, value = line.split(':', 1)
            self.env[key.strip()] = value.strip()
    
    def verbose(self, message, level=1):
        """Send verbose message to Asterisk"""
        sys.stdout.write(f'VERBOSE "{message}" {level}\n')
        sys.stdout.flush()
        return self._read_response()
    
    def set_variable(self, name, value):
        """Set Asterisk channel variable"""
        sys.stdout.write(f'SET VARIABLE {name} "{value}"\n')
        sys.stdout.flush()
        return self._read_response()
    
    def get_variable(self, name):
        """Get Asterisk channel variable"""
        sys.stdout.write(f'GET VARIABLE {name}\n')
        sys.stdout.flush()
        response = self._read_response()
        if '(' in response:
            return response.split('(')[1].split(')')[0]
        return ""
    
    def _read_response(self):
        """Read response from Asterisk"""
        return sys.stdin.readline().strip()


class STTRecognizer:
    """Speech-to-Text Recognizer"""
    
    def __init__(self, config_file='/etc/asterisk/stt/stt_config.conf'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.recognizer = sr.Recognizer()
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_file = self.config.get('vicidial', 'log_file', 
                                   fallback='/var/log/asterisk/stt.log')
        log_level = self.config.get('vicidial', 'log_level', 
                                    fallback='INFO')
        
        logging.basicConfig(
            filename=log_file,
            level=getattr(logging, log_level),
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def recognize_audio(self, audio_file):
        """
        Recognize speech from audio file
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            Transcription text or error message
        """
        try:
            engine = self.config.get('general', 'engine', fallback='google')
            language = self.config.get('general', 'language', fallback='es-ES')
            
            self.logger.info(f"Processing audio file: {audio_file}")
            self.logger.info(f"Using engine: {engine}, language: {language}")
            
            # Load audio file
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            
            # Perform recognition based on engine
            if engine == 'google':
                text = self._recognize_google(audio, language)
            elif engine == 'whisper':
                text = self._recognize_whisper(audio, language)
            elif engine == 'sphinx':
                text = self._recognize_sphinx(audio, language)
            else:
                text = f"Unknown engine: {engine}"
                self.logger.error(text)
            
            self.logger.info(f"Recognition result: {text}")
            return text
            
        except sr.UnknownValueError:
            error_msg = "Could not understand audio"
            self.logger.warning(error_msg)
            return error_msg
        except sr.RequestError as e:
            error_msg = f"API error: {str(e)}"
            self.logger.error(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.logger.error(error_msg)
            return error_msg
    
    def _recognize_google(self, audio, language):
        """Recognize using Google Cloud Speech API"""
        # Check if API key file exists
        api_key_file = self.config.get('google', 'api_key_file', 
                                       fallback='/etc/asterisk/google-credentials.json')
        
        if os.path.exists(api_key_file):
            # Use Google Cloud Speech with credentials
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_key_file
            return self.recognizer.recognize_google_cloud(audio, language=language)
        else:
            # Use free Google Web Speech API
            return self.recognizer.recognize_google(audio, language=language)
    
    def _recognize_whisper(self, audio, language):
        """Recognize using OpenAI Whisper"""
        model = self.config.get('whisper', 'model', fallback='base')
        return self.recognizer.recognize_whisper(audio, model=model, language=language.split('-')[0])
    
    def _recognize_sphinx(self, audio, language):
        """Recognize using CMU Sphinx"""
        return self.recognizer.recognize_sphinx(audio, language=language)
    
    def save_result(self, call_id, audio_file, transcription):
        """Save transcription result to database"""
        try:
            import pymysql
            
            db_config = {
                'host': self.config.get('vicidial', 'db_host', fallback='localhost'),
                'port': self.config.getint('vicidial', 'db_port', fallback=3306),
                'user': self.config.get('vicidial', 'db_user', fallback='cron'),
                'password': self.config.get('vicidial', 'db_pass', fallback='1234'),
                'database': self.config.get('vicidial', 'db_name', fallback='asterisk')
            }
            
            connection = pymysql.connect(**db_config)
            cursor = connection.cursor()
            
            # Create table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stt_transcriptions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    call_id VARCHAR(50),
                    audio_file VARCHAR(255),
                    transcription TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_call_id (call_id)
                )
            """)
            
            # Insert transcription
            cursor.execute("""
                INSERT INTO stt_transcriptions (call_id, audio_file, transcription)
                VALUES (%s, %s, %s)
            """, (call_id, audio_file, transcription))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            self.logger.info(f"Saved transcription for call {call_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving to database: {str(e)}")
            return False


def main():
    """Main AGI script execution"""
    # Initialize AGI
    agi = AGI()
    
    # Initialize STT recognizer
    try:
        stt = STTRecognizer()
    except Exception as e:
        agi.verbose(f"Error initializing STT: {str(e)}", 1)
        sys.exit(1)
    
    # Get audio file path from AGI variable
    audio_file = agi.get_variable('RECORDING_FILE')
    call_id = agi.get_variable('UNIQUEID')
    
    if not audio_file:
        agi.verbose("No audio file specified", 1)
        agi.set_variable('STT_RESULT', 'ERROR: No audio file')
        sys.exit(1)
    
    agi.verbose(f"Processing audio file: {audio_file}", 1)
    
    # Perform speech recognition
    transcription = stt.recognize_audio(audio_file)
    
    # Set result variable
    agi.set_variable('STT_RESULT', transcription)
    agi.set_variable('STT_SUCCESS', '1' if 'error' not in transcription.lower() else '0')
    
    # Save to database if enabled
    if call_id and audio_file:
        stt.save_result(call_id, audio_file, transcription)
    
    agi.verbose(f"Transcription: {transcription}", 1)
    
    sys.exit(0)


if __name__ == '__main__':
    main()
