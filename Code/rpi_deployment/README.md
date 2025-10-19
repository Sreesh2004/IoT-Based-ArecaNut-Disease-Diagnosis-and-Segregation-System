# Raspberry Pi 3+ Areca Nut Detection with Relay Control
## Complete Deployment Package

### 🎯 Project Overview
This package contains everything needed to deploy an areca nut spoilage detection system on Raspberry Pi 3+ with automatic relay control.

### 📦 Package Contents

```
rpi_deployment/
├── areca_detection_relay.py    # Main detection script
├── config.py                   # Configuration settings
├── test_relays.py              # Relay testing utility
├── setup.sh                    # Automated setup script
├── run.py                      # Simple launcher script
├── README.md                   # This file
├── models/                     # Model directory
│   └── (copy your best.pt here)
├── scripts/                    # Additional scripts
├── docs/                       # Documentation
└── logs/                       # Log files (created on first run)
```

### 🚀 Quick Start Guide

#### 1. Transfer Files to Raspberry Pi
```bash
# Option A: Using SCP (if Pi has network connection)
scp -r rpi_deployment/ pi@your-pi-ip:~/

# Option B: Copy to USB drive and transfer manually
# Option C: Use network file sharing
```

#### 2. Copy Your Trained Model
```bash
# Copy your trained model file to the models directory
cp /path/to/your/best.pt ~/rpi_deployment/models/
```

#### 3. Run Setup Script
```bash
cd ~/rpi_deployment
chmod +x setup.sh
./setup.sh
```

#### 4. Reboot Raspberry Pi
```bash
sudo reboot
```

#### 5. Test Hardware
```bash
cd ~/rpi_deployment
python3 test_relays.py
```

#### 6. Run Detection System
```bash
# Option A: Direct run
python3 areca_detection_relay.py

# Option B: Using launcher
python3 run.py
```

### 🔌 Hardware Connections

#### 2-Channel Relay Module
```
Raspberry Pi 3+    <-->    2-Channel Relay Module
================           ======================
Pin 2  (5V)        <-->    VCC
Pin 6  (GND)       <-->    GND  
Pin 12 (GPIO 18)   <-->    IN1 (Relay 1)
Pin 35 (GPIO 19)   <-->    IN2 (Relay 2)
```

#### Camera Module
- Connect Raspberry Pi Camera Module to CSI port
- Ensure camera is enabled in raspi-config

### ⚙️ Configuration

Edit `config.py` to customize system behavior:

```python
# Relay trigger sensitivity
DETECTION_CONFIG = {
    'severe_confidence_threshold': 0.7,  # 70% confidence required
    'relay_duration': 3.0,               # Relay active for 3 seconds
    'relay_cooldown': 5.0,               # 5 seconds between triggers
}

# GPIO pins (change if using different pins)
RELAY_CONFIG = {
    'relay1_pin': 18,  # GPIO 18
    'relay2_pin': 19,  # GPIO 19
}
```

### 🎛️ System Operation

#### Normal Operation
- Camera captures frames every 1 second
- Model classifies as "Normal" or "Severe"
- Display shows prediction and confidence
- Console shows detection status

#### Severe Detection
- When "Severe" detected with confidence > threshold
- Both relays activate simultaneously
- Relays stay active for configured duration
- Cooldown period prevents spam triggering

#### Visual Indicators
- **Green border**: Normal condition detected
- **Red border**: Severe condition detected
- **Relay status**: 🔴🔴 ACTIVE or ⚫⚫ INACTIVE
- **Confidence**: Percentage shown on display

### 🔧 Troubleshooting

#### Camera Issues
```bash
# Check camera detection
vcgencmd get_camera

# Test camera manually
libcamera-hello --preview -t 5000
```

#### GPIO Issues
```bash
# Check GPIO status
gpio readall

# Test GPIO permissions
groups $USER  # Should include 'gpio'
```

#### Model Issues
```bash
# Verify model file
ls -la models/best.pt
file models/best.pt

# Test model loading
python3 -c "from ultralytics import YOLO; YOLO('models/best.pt')"
```

### 🔒 Safety Notes

1. **Test with safe loads** before connecting high-power devices
2. **Check relay ratings** - typically 10A at 250VAC maximum
3. **Proper grounding** - ensure all connections are secure
4. **Heat management** - monitor Pi temperature during operation
5. **Emergency stop** - include manual override for critical applications

### 📊 Performance Tips

#### For Better Performance
- Reduce detection interval: `detection_interval = 2.0`
- Lower camera resolution: `width = 320, height = 240`
- Disable video display for headless operation: `show_video = False`

#### For Production Use
- Set up auto-start service (see full documentation)
- Enable logging for monitoring
- Configure network monitoring
- Set up backup power supply

### 📝 File Descriptions

- **`areca_detection_relay.py`**: Main application with camera capture, ML inference, and relay control
- **`config.py`**: All configuration parameters in one place
- **`test_relays.py`**: Hardware testing utility to verify relay connections
- **`setup.sh`**: Automated installation of dependencies and system configuration
- **`run.py`**: Simple launcher with pre-flight checks

### 🔄 Auto-Start Setup (Optional)

To run the system automatically on boot:

```bash
# Create systemd service
sudo nano /etc/systemd/system/areca-detection.service

# Add service configuration
[Unit]
Description=Areca Nut Detection with Relay Control
After=multi-user.target

[Service]
Type=idle
User=pi
WorkingDirectory=/home/pi/rpi_deployment
ExecStart=/usr/bin/python3 /home/pi/rpi_deployment/areca_detection_relay.py
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl enable areca-detection.service
sudo systemctl start areca-detection.service
```

### 📞 Support

1. Check hardware connections
2. Verify all files are present
3. Run test scripts individually
4. Check system logs: `journalctl -f`
5. Monitor system resources: `htop`

---

**🥥 Ready to deploy your areca nut detection system!**