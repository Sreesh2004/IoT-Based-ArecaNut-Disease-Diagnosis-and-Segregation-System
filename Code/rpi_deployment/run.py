#!/usr/bin/env python3
"""
Areca Nut Detection - Run Script
===============================
Simple launcher script for the detection system
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if all required files are present"""
    required_files = [
        'config.py',
        'areca_detection_relay.py',
        'models/best.pt'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n💡 Please ensure all files are copied correctly.")
        return False
    
    return True

def main():
    print("🥥 Areca Nut Detection System Launcher")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Run the main detection script
    try:
        print("🚀 Starting detection system...")
        os.system('python3 areca_detection_relay.py')
    except KeyboardInterrupt:
        print("\n👋 System stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()