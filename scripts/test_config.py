#!/usr/bin/env python3
"""
Simple test script to verify STT configuration
Run this to test basic functionality without Asterisk
"""

import sys
import os

def test_imports():
    """Test if all required libraries can be imported"""
    print("Testing imports...")
    
    try:
        import vosk
        print("✓ Vosk library imported successfully")
        print(f"  Vosk version: {vosk.__version__ if hasattr(vosk, '__version__') else 'unknown'}")
    except ImportError as e:
        print(f"✗ Failed to import Vosk: {e}")
        return False
    
    try:
        from asterisk.agi import AGI
        print("✓ Asterisk AGI library imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import AGI library: {e}")
        print("  Note: This is expected if not running on an Asterisk system")
    
    try:
        from configparser import ConfigParser
        print("✓ ConfigParser imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import ConfigParser: {e}")
        return False
    
    return True

def test_config():
    """Test if configuration file exists and is valid"""
    print("\nTesting configuration...")
    
    from configparser import ConfigParser
    
    config_paths = [
        '/etc/asterisk/stt/stt_config.ini',
        'config/stt_config.ini',
        '/home/runner/work/PiperTTS/PiperTTS/config/stt_config.ini'
    ]
    
    config = None
    config_file = None
    
    for path in config_paths:
        if os.path.exists(path):
            config_file = path
            break
    
    if not config_file:
        print(f"✗ Configuration file not found in any of these paths:")
        for path in config_paths:
            print(f"  - {path}")
        return False
    
    print(f"✓ Configuration file found: {config_file}")
    
    config = ConfigParser()
    try:
        config.read(config_file)
        print(f"✓ Configuration file parsed successfully")
        
        # Test key sections
        if config.has_section('general'):
            print(f"✓ [general] section found")
            print(f"  - Engine: {config.get('general', 'engine', fallback='not set')}")
            print(f"  - Model path: {config.get('general', 'model_path', fallback='not set')}")
            print(f"  - Language: {config.get('general', 'language', fallback='not set')}")
        
        if config.has_section('vicidial'):
            print(f"✓ [vicidial] section found")
            print(f"  - Log path: {config.get('vicidial', 'log_path', fallback='not set')}")
            print(f"  - Log level: {config.get('vicidial', 'log_level', fallback='not set')}")
        
        return True
    except Exception as e:
        print(f"✗ Failed to parse configuration: {e}")
        return False

def test_directories():
    """Test if required directories exist"""
    print("\nTesting directories...")
    
    dirs = {
        'AGI scripts': '/var/lib/asterisk/agi-bin',
        'STT models': '/var/lib/asterisk/models',
        'Logs': '/var/log/asterisk/stt',
        'Recordings': '/var/spool/asterisk/monitor'
    }
    
    all_exist = True
    for name, path in dirs.items():
        if os.path.exists(path):
            print(f"✓ {name} directory exists: {path}")
        else:
            print(f"✗ {name} directory not found: {path}")
            all_exist = False
    
    return all_exist

def test_model():
    """Test if STT model exists and can be loaded"""
    print("\nTesting STT model...")
    
    try:
        from vosk import Model
        from configparser import ConfigParser
        
        config = ConfigParser()
        config_paths = [
            '/etc/asterisk/stt/stt_config.ini',
            'config/stt_config.ini',
            '/home/runner/work/PiperTTS/PiperTTS/config/stt_config.ini'
        ]
        
        for path in config_paths:
            if os.path.exists(path):
                config.read(path)
                break
        
        if not config.has_section('general'):
            print("✗ Cannot test model: configuration not found")
            return False
        
        model_path = config.get('general', 'model_path')
        
        if not os.path.exists(model_path):
            print(f"✗ Model directory not found: {model_path}")
            return False
        
        print(f"✓ Model directory exists: {model_path}")
        
        # Try to load the model (this might take a while)
        print("  Loading model (this may take a moment)...")
        try:
            model = Model(model_path)
            print("✓ Model loaded successfully!")
            return True
        except Exception as e:
            print(f"✗ Failed to load model: {e}")
            return False
            
    except Exception as e:
        print(f"✗ Error testing model: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("STT Configuration Test Suite")
    print("=" * 50)
    
    results = {
        'Imports': test_imports(),
        'Configuration': test_config(),
        'Directories': test_directories(),
        'Model': test_model()
    }
    
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 50)
    if all_passed:
        print("All tests passed! ✓")
        print("Your STT configuration appears to be working correctly.")
        return 0
    else:
        print("Some tests failed. ✗")
        print("Please review the output above for details.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
