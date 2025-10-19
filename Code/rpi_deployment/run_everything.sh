#!/bin/bash
# ULTIMATE ONE-LINER FOR ARECA DETECTION
# =====================================
# Copy and paste this ENTIRE command in your Raspberry Pi terminal

echo "🚀 ARECA DETECTION - AUTO SETUP & LAUNCH" && \

# Quick system prep
sudo apt update -qq && sudo apt install -y python3-pip python3-venv python3-opencv v4l-utils -qq && \

# Create and activate environment
python3 -m venv venv && source venv/bin/activate && \

# Install packages quickly
pip install ultralytics opencv-python pillow RPi.GPIO -q && \

# Test and launch
echo "📹 Testing camera..." && \
(timeout 3 python3 -c "import cv2; cap=cv2.VideoCapture(0); print('✅ Camera OK' if cap.isOpened() else '⚠️ Camera issue'); cap.release()" 2>/dev/null || echo "⚠️ Camera test skipped") && \

echo "🔌 Testing GPIO..." && \
(python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); GPIO.cleanup(); print('✅ GPIO OK')" 2>/dev/null || echo "⚠️ GPIO issue") && \

echo "" && \
echo "🎯 LAUNCHING ARECA DETECTION SYSTEM..." && \
echo "🔴 Press CTRL+C to stop" && \
echo "🟢 Point camera at areca nuts" && \
echo "⚡ Relays trigger on SEVERE detection" && \
echo "" && \

# Launch main application
python3 areca_detection_relay.py