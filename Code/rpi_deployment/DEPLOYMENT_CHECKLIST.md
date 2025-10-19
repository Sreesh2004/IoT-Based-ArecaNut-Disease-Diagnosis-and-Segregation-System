# Raspberry Pi Deployment Checklist

## ✅ Pre-Transfer Verification
- [x] Trained model copied to `models/best.pt`
- [x] All required scripts created
- [x] Configuration files ready
- [x] Documentation complete

## 📦 Transfer Package Contents
```
rpi_deployment/
├── areca_detection_relay.py     # Main detection application
├── config.py                    # Configuration settings
├── run.py                      # Simple launcher script
├── setup.sh                   # Automated setup script
├── requirements.txt           # Python dependencies
├── README.md                 # Complete documentation
├── DEPLOYMENT_CHECKLIST.md  # This checklist
├── models/
│   └── best.pt              # Your trained YOLOv8n model
├── scripts/
│   └── test_relays.py       # Relay testing utility
└── docs/
    ├── HARDWARE_SETUP.md    # Wiring diagrams
    ├── TROUBLESHOOTING.md   # Common issues
    └── API_REFERENCE.md     # Code documentation
```

## 🔧 Hardware Requirements
- [ ] Raspberry Pi 3+ with camera module
- [ ] 2-Channel 5V Relay Module
- [ ] Jumper wires for connections
- [ ] 5V power supply for relays

## 🔌 Wiring Connections
- [ ] GPIO 18 (Pin 12) → Relay 1 Control
- [ ] GPIO 19 (Pin 35) → Relay 2 Control
- [ ] 5V (Pin 2) → Relay VCC
- [ ] GND (Pin 6) → Relay GND

## 🚀 Deployment Steps

### 1. Transfer Files
```bash
# Copy entire rpi_deployment folder to your Raspberry Pi
scp -r rpi_deployment/ pi@your_pi_ip:~/
```

### 2. Initial Setup
```bash
# SSH into your Raspberry Pi
ssh pi@your_pi_ip

# Navigate to deployment folder
cd ~/rpi_deployment

# Run automated setup
chmod +x setup.sh
./setup.sh
```

### 3. Test Hardware
```bash
# Test relay connections
python3 scripts/test_relays.py
```

### 4. Run Detection System
```bash
# Start the detection system
python3 run.py
```

## 🔍 Quick Verification
- [ ] Camera preview shows correctly
- [ ] "Normal" detection: No relay activation
- [ ] "Severe" detection: Both relays activate for 2 seconds
- [ ] Press 'q' to quit application

## 📞 Support Commands
```bash
# Check camera
vcgencmd get_camera

# Test GPIO
gpio readall

# Monitor system resources
htop

# View logs
tail -f detection_logs.txt
```

## ⚡ Quick Start (After Setup)
```bash
cd ~/rpi_deployment
python3 run.py
```

---
**Status: Ready for Transfer** ✅
**Model Size: ~6MB**
**Total Package: ~8MB**