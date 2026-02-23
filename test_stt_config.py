#!/usr/bin/env python3
"""
Test script for STT configuration
"""

import os
import sys
import configparser

def check_dependencies():
    """Check if required Python packages are installed"""
    print("Checking Python dependencies...")
    required_packages = [
        'speech_recognition',
        'pydub',
        'pymysql'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - MISSING")
            missing.append(package)
    
    return len(missing) == 0

def check_config():
    """Check if configuration file exists and is valid"""
    print("\nChecking configuration...")
    config_file = '/etc/asterisk/stt/stt_config.conf'
    
    if not os.path.exists(config_file):
        print(f"  ✗ Configuration file not found: {config_file}")
        print(f"    Using local config instead: ./stt_config.conf")
        config_file = './stt_config.conf'
        if not os.path.exists(config_file):
            print(f"  ✗ Local configuration file not found")
            return False
    
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
        
        # Check required sections
        required_sections = ['general', 'vicidial']
        for section in required_sections:
            if config.has_section(section):
                print(f"  ✓ Section [{section}] found")
            else:
                print(f"  ✗ Section [{section}] missing")
                return False
        
        # Check engine configuration
        engine = config.get('general', 'engine', fallback='google')
        print(f"  ✓ STT Engine: {engine}")
        
        language = config.get('general', 'language', fallback='es-ES')
        print(f"  ✓ Language: {language}")
        
        return True
    except Exception as e:
        print(f"  ✗ Error reading configuration: {e}")
        return False

def check_directories():
    """Check if required directories exist"""
    print("\nChecking directories...")
    directories = [
        '/var/lib/asterisk/agi-bin',
        '/var/log/asterisk',
        '/var/spool/asterisk/monitor'
    ]
    
    all_exist = True
    for directory in directories:
        if os.path.exists(directory):
            print(f"  ✓ {directory}")
        else:
            print(f"  ✗ {directory} - does not exist")
            all_exist = False
    
    return all_exist

def check_agi_script():
    """Check if AGI script is installed"""
    print("\nChecking AGI script...")
    script_path = '/var/lib/asterisk/agi-bin/stt_recognition.py'
    
    if os.path.exists(script_path):
        print(f"  ✓ Script found: {script_path}")
        if os.access(script_path, os.X_OK):
            print(f"  ✓ Script is executable")
            return True
        else:
            print(f"  ✗ Script is not executable")
            return False
    else:
        print(f"  ✗ Script not found: {script_path}")
        return False

def test_google_api():
    """Test Google Cloud Speech API credentials"""
    print("\nChecking Google Cloud credentials...")
    credentials_file = '/etc/asterisk/google-credentials.json'
    
    if os.path.exists(credentials_file):
        print(f"  ✓ Credentials file found: {credentials_file}")
        return True
    else:
        print(f"  ℹ Credentials file not found: {credentials_file}")
        print(f"    Will use free Google Web Speech API")
        return True

def main():
    """Run all checks"""
    print("=" * 50)
    print("STT Configuration Test")
    print("=" * 50)
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Configuration", check_config),
        ("Directories", check_directories),
        ("AGI Script", check_agi_script),
        ("Google API", test_google_api)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\nError in {name} check: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    
    all_passed = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("\n✓ All checks passed! STT configuration is ready.")
        sys.exit(0)
    else:
        print("\n✗ Some checks failed. Please review the errors above.")
        print("\nTo install dependencies, run: sudo bash install.sh")
        sys.exit(1)

if __name__ == '__main__':
    main()
