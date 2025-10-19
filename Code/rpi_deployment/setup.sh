#!/bin/bash
# Raspberry Pi 3+ Setup Script for Areca Nut Detection with Relay Control
# ========================================================================

echo "🥥 Setting up Areca Nut Detection System on Raspberry Pi 3+"
echo "============================================================="

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
sudo apt install -y python3 python3-pip python3-venv
sudo apt install -y python3-opencv
sudo apt install -y libcamera-apps

# Install GPIO library
echo "🔌 Installing GPIO library..."
sudo apt install -y python3-rpi.gpio

# Create virtual environment
echo "🏗️  Creating virtual environment..."
python3 -m venv areca_env
source areca_env/bin/activate

# Install Python packages
echo "📚 Installing Python packages..."
pip install ultralytics
pip install opencv-python
pip install pillow
pip install numpy

# Enable camera
echo "📹 Enabling camera interface..."
sudo raspi-config nonint do_camera 0

# Create GPIO permissions script
echo "🔑 Setting up GPIO permissions..."
sudo usermod -a -G gpio $USER

# Create required directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p saved_frames

# Make scripts executable
echo "🔧 Setting up permissions..."
chmod +x test_relays.py
chmod +x areca_detection_relay.py

echo "✅ Setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Copy your trained model file (best.pt) to the models/ directory"
echo "2. Reboot the Pi: sudo reboot"
echo "3. Test relays: python3 test_relays.py"
echo "4. Run detection system: python3 areca_detection_relay.py"
echo ""
echo "🔌 GPIO Connections for 2-Channel Relay:"
echo "   Relay 1 (IN1) -> GPIO 18 (Pin 12)"
echo "   Relay 2 (IN2) -> GPIO 19 (Pin 35)"
echo "   VCC -> Pin 2 (5V)"
echo "   GND -> Pin 6 (GND)"
echo ""
echo "⚠️  Important: Reboot required for camera and GPIO changes to take effect!"