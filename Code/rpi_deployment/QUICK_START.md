# 🚀 SINGLE COMMAND TO RUN EVERYTHING ON RASPBERRY PI

## Method 1: Super Simple (Recommended)
Just navigate to your `rpi_deployment` folder and run:

```bash
python3 simple_run.py
```

This single Python script will:
- ✅ Install all required packages
- ✅ Test your external webcam
- ✅ Test GPIO connections  
- ✅ Launch the detection system

## Method 2: One-Liner Command
Copy the ENTIRE command from `ONE_COMMAND.txt` and paste it in your terminal.

## Method 3: Bash Script
Make executable and run:
```bash
chmod +x ultimate_setup.sh
./ultimate_setup.sh
```

---

## 📹 External Webcam Support
✅ **External webcams work perfectly!** The system will automatically:
- Try camera indices 0, 1, 2 to find your webcam
- Configure optimal settings for real-time detection
- Handle USB webcam connection automatically

## 🔌 What Happens When You Run
1. **Auto-detection**: Finds your external webcam
2. **Model loading**: Loads your trained YOLOv8n model
3. **Camera preview**: Shows live video feed
4. **Real-time detection**: Classifies areca nuts as Normal/Severe
5. **Relay control**: Triggers both relays for 2 seconds when "Severe" detected

## 🎯 Quick Start Commands

### For Fresh Raspberry Pi:
```bash
cd ~/rpi_deployment
python3 simple_run.py
```

### If you have issues:
```bash
# Test camera first
python3 scripts/test_relays.py

# Then run detection
python3 simple_run.py
```

## 🔧 Hardware Connections
- **GPIO 18 (Pin 12)** → Relay 1 Control
- **GPIO 19 (Pin 35)** → Relay 2 Control  
- **5V (Pin 2)** → Relay VCC
- **GND (Pin 6)** → Relay GND
- **USB Port** → External Webcam

## 🛑 How to Stop
Press **CTRL+C** in the terminal to stop the detection system.

---
**Status: Ready for Single-Command Deployment** ✅