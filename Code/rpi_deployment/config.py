"""
Raspberry Pi 3+ Configuration for Areca Nut Detection with Relay Control
========================================================================

This file contains all the configuration settings for the detection system.
Modify these values according to your hardware setup.
"""

# GPIO Pin Configuration
RELAY_CONFIG = {
    'relay1_pin': 18,  # GPIO 18 (Physical Pin 12) - Relay 1
    'relay2_pin': 19,  # GPIO 19 (Physical Pin 35) - Relay 2
}

# Detection Thresholds
DETECTION_CONFIG = {
    'severe_confidence_threshold': 0.7,   # Trigger relay if Severe confidence > 70%
    'detection_interval': 1.0,           # Run detection every 1 second
    'relay_duration': 3.0,               # Keep relay active for 3 seconds
    'relay_cooldown': 5.0,               # Wait 5 seconds between relay triggers
}

# Camera Configuration
CAMERA_CONFIG = {
    'width': 640,
    'height': 480,
    'fps': 30,
    'camera_index': 0,  # Use 0 for RPi camera, try 1 if using USB camera
}

# Model Configuration
MODEL_CONFIG = {
    'model_path': "models/best.pt",  # Path to your trained model
    'input_size': 224,               # Model input size
}

# Display Configuration
DISPLAY_CONFIG = {
    'show_video': True,    # Set to False for headless operation
    'font_scale': 0.8,
    'thickness': 2,
}

# Logging Configuration
LOGGING_CONFIG = {
    'log_detections': True,
    'log_file': "detection_log.txt",
    'log_relay_triggers': True,
}