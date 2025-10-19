#!/bin/bash
# Ultimate One-Command Setup and Launch for Areca Detection System
# ================================================================
# This script does EVERYTHING: setup, install, configure, and run
# Just paste this single command in your Raspberry Pi terminal!

echo "🚀 ARECA NUT DETECTION SYSTEM - ONE-COMMAND SETUP & LAUNCH"
echo "=========================================================="

# Check if we're in the right directory
if [ ! -f "areca_detection_relay.py" ]; then
    echo "❌ Please run this command from the rpi_deployment directory"
    echo "💡 Usage: cd ~/rpi_deployment && curl -sSL https://your-url/ultimate_setup.sh | bash"
    exit 1
fi

# Function to check command success
check_success() {
    if [ $? -eq 0 ]; then
        echo "✅ $1"
    else
        echo "❌ $1 failed"
        exit 1
    fi
}

# Update system
echo "📦 Updating system packages..."
sudo apt update -qq && sudo apt upgrade -y -qq
check_success "System update"

# Install system dependencies
echo "🔧 Installing system dependencies..."
sudo apt install -y python3-pip python3-venv python3-opencv libopencv-dev \
    python3-picamera2 v4l-utils uvcdynctrl git curl
check_success "System dependencies installation"

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
    check_success "Virtual environment creation"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
check_success "Virtual environment activation"

# Upgrade pip
echo "📈 Upgrading pip..."
pip install --upgrade pip -q
check_success "Pip upgrade"

# Install Python packages
echo "📚 Installing Python packages..."
pip install -r requirements.txt -q
check_success "Python packages installation"

# Enable camera (if not already enabled)
echo "📹 Configuring camera..."
if ! grep -q "^camera_auto_detect=1" /boot/config.txt; then
    echo "camera_auto_detect=1" | sudo tee -a /boot/config.txt > /dev/null
fi
if ! grep -q "^start_x=1" /boot/config.txt; then
    echo "start_x=1" | sudo tee -a /boot/config.txt > /dev/null
fi

# Enable GPIO
echo "🔌 Configuring GPIO..."
sudo systemctl enable pigpio
sudo systemctl start pigpio 2>/dev/null || true

# Test camera availability
echo "🔍 Checking camera availability..."
if lsusb | grep -i "camera\|webcam\|video" > /dev/null; then
    echo "✅ External camera detected via USB"
elif [ -e /dev/video0 ]; then
    echo "✅ Camera device found at /dev/video0"
else
    echo "⚠️  No camera detected, but continuing..."
fi

# Test GPIO setup
echo "🧪 Testing GPIO access..."
if python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); GPIO.cleanup()" 2>/dev/null; then
    echo "✅ GPIO access working"
else
    echo "⚠️  GPIO test failed, but continuing..."
fi

# Quick relay test
echo "🔧 Testing relay connections..."
python3 scripts/test_relays.py --quick 2>/dev/null || echo "⚠️  Relay test skipped"

# Final camera test
echo "📸 Final camera test..."
timeout 5 python3 -c "
import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened():
    ret, frame = cap.read()
    if ret:
        print('✅ Camera working perfectly!')
    else:
        print('⚠️  Camera opened but no frames')
    cap.release()
else:
    # Try other camera indices
    for i in [1, 2]:
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f'✅ Camera working on index {i}!')
                cap.release()
                break
            cap.release()
    else:
        print('⚠️  No working camera found')
" 2>/dev/null || echo "⚠️  Camera test timeout"

echo ""
echo "🎉 SETUP COMPLETE! LAUNCHING ARECA DETECTION SYSTEM..."
echo "=========================================================="
echo "🔴 Press CTRL+C to stop the system"
echo "🟢 Point camera at areca nuts to start detection"
echo "⚡ Relays will trigger when SEVERE condition detected"
echo ""

# Launch the main application
echo "🚀 Starting detection system in 3 seconds..."
sleep 1 && echo "3..." && sleep 1 && echo "2..." && sleep 1 && echo "1..." && sleep 1

# Run with error handling
if python3 areca_detection_relay.py; then
    echo "✅ Detection system completed successfully"
else
    echo "❌ Detection system encountered an error"
    echo "💡 Check the troubleshooting guide in docs/TROUBLESHOOTING.md"
    exit 1
fi