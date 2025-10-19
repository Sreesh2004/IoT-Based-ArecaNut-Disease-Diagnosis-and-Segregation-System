#!/usr/bin/env python3
"""
ULTIMATE SIMPLE LAUNCHER - Just run this one file!
================================================
This single Python script will:
1. Install all dependencies
2. Setup GPIO
3. Test camera
4. Launch detection system

Usage: python3 simple_run.py
"""

import subprocess
import sys
import os
import time

def run_command(cmd, description="", check=True):
    """Run shell command with nice output"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if check and result.returncode != 0:
            print(f"❌ {description} failed: {result.stderr}")
            return False
        else:
            print(f"✅ {description}")
            return True
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def install_package(package):
    """Install Python package if not already installed"""
    try:
        __import__(package.replace('-', '_'))
        print(f"✅ {package} already installed")
        return True
    except ImportError:
        print(f"📦 Installing {package}...")
        return run_command(f"{sys.executable} -m pip install {package} -q", f"{package} installation")

def main():
    print("🚀 ARECA NUT DETECTION - SIMPLE LAUNCHER")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("areca_detection_relay.py"):
        print("❌ areca_detection_relay.py not found!")
        print("💡 Make sure you're in the rpi_deployment directory")
        return False
    
    # Install essential packages
    packages = ["ultralytics", "opencv-python", "pillow"]
    for package in packages:
        if not install_package(package):
            print(f"❌ Failed to install {package}")
            return False
    
    # Try to install RPi.GPIO (might fail on non-Pi systems)
    try:
        import RPi.GPIO as GPIO
        print("✅ RPi.GPIO already available")
    except ImportError:
        print("📦 Installing RPi.GPIO...")
        run_command(f"{sys.executable} -m pip install RPi.GPIO -q", "RPi.GPIO installation", check=False)
    
    # Quick camera test
    print("📹 Testing camera...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                print("✅ External webcam working perfectly!")
            else:
                # Try other camera indices
                cap.release()
                for i in [1, 2]:
                    cap = cv2.VideoCapture(i)
                    if cap.isOpened():
                        ret, frame = cap.read()
                        if ret and frame is not None:
                            print(f"✅ Camera working on index {i}!")
                            break
                        cap.release()
                else:
                    print("⚠️  Camera test inconclusive, but continuing...")
            cap.release()
        else:
            print("⚠️  Camera not detected, but continuing...")
    except Exception as e:
        print(f"⚠️  Camera test failed: {e}")
    
    # GPIO test
    print("🔌 Testing GPIO...")
    try:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        print("✅ GPIO working")
    except Exception as e:
        print(f"⚠️  GPIO test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 LAUNCHING ARECA DETECTION SYSTEM")
    print("=" * 50)
    print("🔴 Press CTRL+C to stop the system")
    print("🟢 Point camera at areca nuts")
    print("⚡ Relays trigger when SEVERE detected")
    print("=" * 50)
    
    # Small delay for dramatic effect
    for i in range(3, 0, -1):
        print(f"🚀 Starting in {i}...")
        time.sleep(1)
    
    print("\n🏁 LAUNCHING NOW!\n")
    
    # Launch the main detection system
    try:
        import areca_detection_relay
        # The script will run when imported
    except KeyboardInterrupt:
        print("\n🛑 Detection system stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Check that your camera is connected and model file exists")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)