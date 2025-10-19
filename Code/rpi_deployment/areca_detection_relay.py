#!/usr/bin/env python3
"""
Areca Nut Spoilage Detection with Relay Control for Raspberry Pi 3+
================================================================
This script runs YOLOv8n classification model on Raspberry Pi camera
and triggers relays when "Severe" condition is detected.

Hardware Requirements:
- Raspberry Pi 3+ with camera module
- 2-channel relay module
- GPIO connections for relays

GPIO Connections:
- Relay 1: GPIO 18 (Pin 12)
- Relay 2: GPIO 19 (Pin 35)
- GND: Pin 6 or Pin 14
- VCC: Pin 2 (5V) or Pin 4 (5V)
"""

import cv2
import time
import tempfile
import threading
import queue
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO
import os

# Import configuration
try:
    from config import *
except ImportError:
    print("⚠️  Configuration file not found, using default settings")
    RELAY_CONFIG = {'relay1_pin': 18, 'relay2_pin': 19}
    DETECTION_CONFIG = {
        'severe_confidence_threshold': 0.7,
        'detection_interval': 1.0,
        'relay_duration': 3.0,
        'relay_cooldown': 5.0,
    }
    CAMERA_CONFIG = {'width': 640, 'height': 480, 'fps': 30}
    MODEL_CONFIG = {'model_path': "models/best.pt"}

# Raspberry Pi GPIO imports
try:
    import RPi.GPIO as GPIO
    RPI_AVAILABLE = True
    print("✅ RPi.GPIO imported successfully")
except ImportError:
    print("⚠️  RPi.GPIO not available - running in simulation mode")
    RPI_AVAILABLE = False

class RelayController:
    """Controls 2-channel relay module on Raspberry Pi"""
    
    def __init__(self, relay1_pin=18, relay2_pin=19):
        self.relay1_pin = relay1_pin
        self.relay2_pin = relay2_pin
        self.relay1_active = False
        self.relay2_active = False
        
        if RPI_AVAILABLE:
            self.setup_gpio()
        else:
            print("🔧 GPIO simulation mode - no physical relays controlled")
    
    def setup_gpio(self):
        """Initialize GPIO pins for relay control"""
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            
            # Setup relay pins as outputs
            GPIO.setup(self.relay1_pin, GPIO.OUT)
            GPIO.setup(self.relay2_pin, GPIO.OUT)
            
            # Initialize relays as OFF (HIGH = OFF for most relay modules)
            GPIO.output(self.relay1_pin, GPIO.HIGH)
            GPIO.output(self.relay2_pin, GPIO.HIGH)
            
            print(f"✅ GPIO initialized - Relay1: GPIO{self.relay1_pin}, Relay2: GPIO{self.relay2_pin}")
        except Exception as e:
            print(f"❌ GPIO setup failed: {e}")
    
    def activate_relay1(self, duration=2.0):
        """Activate relay 1 for specified duration"""
        if RPI_AVAILABLE:
            GPIO.output(self.relay1_pin, GPIO.LOW)  # LOW = ON
            self.relay1_active = True
            print(f"🔴 Relay 1 ACTIVATED for {duration}s")
            
            # Use threading to turn off relay after duration
            threading.Timer(duration, self.deactivate_relay1).start()
        else:
            print(f"🔧 [SIMULATION] Relay 1 would activate for {duration}s")
    
    def activate_relay2(self, duration=2.0):
        """Activate relay 2 for specified duration"""
        if RPI_AVAILABLE:
            GPIO.output(self.relay2_pin, GPIO.LOW)  # LOW = ON
            self.relay2_active = True
            print(f"🔴 Relay 2 ACTIVATED for {duration}s")
            
            # Use threading to turn off relay after duration
            threading.Timer(duration, self.deactivate_relay2).start()
        else:
            print(f"🔧 [SIMULATION] Relay 2 would activate for {duration}s")
    
    def deactivate_relay1(self):
        """Deactivate relay 1"""
        if RPI_AVAILABLE:
            GPIO.output(self.relay1_pin, GPIO.HIGH)  # HIGH = OFF
            self.relay1_active = False
            print("⚫ Relay 1 DEACTIVATED")
        else:
            print("🔧 [SIMULATION] Relay 1 deactivated")
    
    def deactivate_relay2(self):
        """Deactivate relay 2"""
        if RPI_AVAILABLE:
            GPIO.output(self.relay2_pin, GPIO.HIGH)  # HIGH = OFF
            self.relay2_active = False
            print("⚫ Relay 2 DEACTIVATED")
        else:
            print("🔧 [SIMULATION] Relay 2 deactivated")
    
    def activate_both_relays(self, duration=2.0):
        """Activate both relays simultaneously"""
        self.activate_relay1(duration)
        self.activate_relay2(duration)
        print(f"🔴🔴 BOTH RELAYS ACTIVATED for {duration}s")
    
    def cleanup(self):
        """Clean up GPIO resources"""
        if RPI_AVAILABLE:
            try:
                GPIO.cleanup()
                print("✅ GPIO cleanup completed")
            except Exception as e:
                print(f"⚠️  GPIO cleanup warning: {e}")

class ArecaDetectorWithRelay:
    """Real-time areca nut detection with relay control"""
    
    def __init__(self):
        print("🥥 Initializing Areca Nut Detection System with Relay Control")
        print("=" * 70)
        
        # Initialize relay controller
        self.relay_controller = RelayController(
            relay1_pin=RELAY_CONFIG['relay1_pin'],
            relay2_pin=RELAY_CONFIG['relay2_pin']
        )
        
        # Load model
        model_path = MODEL_CONFIG['model_path']
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model not found at {model_path}. Please copy your trained model to models/best.pt")
        
        print("🤖 Loading YOLOv8n model...")
        self.model = YOLO(model_path)
        
        # Initialize camera with external webcam support
        print("📹 Initializing camera...")
        camera_found = False
        camera_indices = [0, 1, 2, -1]  # Try multiple camera indices
        
        for idx in camera_indices:
            print(f"   Trying camera index {idx}...")
            self.cap = cv2.VideoCapture(idx)
            
            if self.cap.isOpened():
                # Test if we can actually read frames
                ret, test_frame = self.cap.read()
                if ret and test_frame is not None:
                    print(f"✅ Successfully connected to camera {idx}")
                    camera_found = True
                    break
                else:
                    self.cap.release()
            else:
                if self.cap is not None:
                    self.cap.release()
        
        if not camera_found:
            raise RuntimeError("❌ No working camera found. Check external webcam connection.")
        
        # Set camera resolution for RPi optimization
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_CONFIG['width'])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_CONFIG['height'])
        self.cap.set(cv2.CAP_PROP_FPS, CAMERA_CONFIG['fps'])
        
        # Additional settings for external webcams
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer for real-time
        
        # Get actual camera settings
        actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        actual_fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        print(f"📹 Camera ready: {actual_width}x{actual_height} @ {actual_fps}fps")
        
        # Detection variables
        self.current_prediction = "No Detection"
        self.current_confidence = 0.0
        self.last_detection_time = time.time()
        self.detection_interval = DETECTION_CONFIG['detection_interval']
        
        # Relay trigger settings
        self.severe_confidence_threshold = DETECTION_CONFIG['severe_confidence_threshold']
        self.relay_duration = DETECTION_CONFIG['relay_duration']
        self.last_relay_trigger = 0
        self.relay_cooldown = DETECTION_CONFIG['relay_cooldown']
        
        # Color settings
        self.colors = {
            'Normal': (0, 255, 0),    # Green
            'Severe': (0, 0, 255),    # Red
            'No Detection': (128, 128, 128)  # Gray
        }
        
        # Threading for async detection
        self.detection_queue = queue.Queue(maxsize=2)
        self.result_queue = queue.Queue(maxsize=2)
        self.detection_thread = None
        self.running = False
        
        print("✅ Areca detection system with relay control initialized!")
    
    def detection_worker(self):
        """Background thread for model inference"""
        while self.running:
            try:
                if not self.detection_queue.empty():
                    frame = self.detection_queue.get_nowait()
                    
                    # Convert to PIL Image and resize
                    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    processed_frame = pil_image.resize((224, 224))
                    
                    # Save to temporary file for YOLO
                    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                        processed_frame.save(temp_file.name, 'JPEG')
                        temp_path = temp_file.name
                    
                    # Run prediction
                    results = self.model(temp_path)
                    
                    # Clean up temp file
                    Path(temp_path).unlink()
                    
                    # Extract results
                    probs = results[0].probs
                    class_names = results[0].names
                    predicted_class = class_names[probs.top1]
                    confidence = probs.top1conf.item()
                    
                    # Put result in queue
                    if not self.result_queue.full():
                        self.result_queue.put((predicted_class, confidence))
                        
                        # Check for severe condition and trigger relay
                        self.check_and_trigger_relay(predicted_class, confidence)
                
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                
            except Exception as e:
                print(f"⚠️  Detection error: {e}")
                time.sleep(0.5)
    
    def check_and_trigger_relay(self, predicted_class, confidence):
        """Check if relay should be triggered based on detection results"""
        current_time = time.time()
        
        # Check if we should trigger relay
        if (predicted_class == "Severe" and 
            confidence >= self.severe_confidence_threshold and
            current_time - self.last_relay_trigger >= self.relay_cooldown):
            
            print(f"🚨 SEVERE CONDITION DETECTED! Confidence: {confidence:.1%}")
            print(f"🔴 Triggering relays for {self.relay_duration}s")
            
            # Trigger both relays
            self.relay_controller.activate_both_relays(self.relay_duration)
            
            # Update last trigger time
            self.last_relay_trigger = current_time
            
        elif predicted_class == "Severe" and confidence < self.severe_confidence_threshold:
            print(f"⚠️  Severe detected but confidence too low: {confidence:.1%} < {self.severe_confidence_threshold:.1%}")
    
    def draw_info_on_frame(self, frame):
        """Draw detection info and relay status on frame"""
        height, width = frame.shape[:2]
        
        # Create overlay
        overlay = frame.copy()
        
        # Draw main detection box
        box_height = 120
        cv2.rectangle(overlay, (10, 10), (width-10, box_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Draw border
        color = self.colors.get(self.current_prediction, (128, 128, 128))
        cv2.rectangle(frame, (10, 10), (width-10, box_height), color, 3)
        
        # Add text
        cv2.putText(frame, f"Prediction: {self.current_prediction}", 
                   (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, f"Confidence: {self.current_confidence:.1%}", 
                   (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Relay status
        relay_status = "🔴🔴 ACTIVE" if (self.relay_controller.relay1_active or 
                                        self.relay_controller.relay2_active) else "⚫⚫ INACTIVE"
        cv2.putText(frame, f"Relays: {relay_status}", 
                   (20, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        # Instructions
        cv2.putText(frame, "Press 'q' to quit", 
                   (width-200, height-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        return frame
    
    def run(self):
        """Main detection loop"""
        print("\n🚀 Starting real-time areca nut detection with relay control...")
        print("📋 System Configuration:")
        print(f"   - Severe threshold: {self.severe_confidence_threshold:.1%}")
        print(f"   - Relay duration: {self.relay_duration}s")
        print(f"   - Relay cooldown: {self.relay_cooldown}s")
        print("📋 Instructions:")
        print("   - Hold areca nut in front of camera")
        print("   - Relays will trigger when Severe condition is detected")
        print("   - Press 'q' to quit")
        print("\n🎥 Camera feed starting...")
        
        self.running = True
        
        # Start detection thread
        self.detection_thread = threading.Thread(target=self.detection_worker, daemon=True)
        self.detection_thread.start()
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Failed to read from camera")
                    break
                
                current_time = time.time()
                
                # Add frame to detection queue if it's time
                if (current_time - self.last_detection_time >= self.detection_interval and
                    not self.detection_queue.full()):
                    self.detection_queue.put(frame.copy())
                    self.last_detection_time = current_time
                
                # Get latest results
                while not self.result_queue.empty():
                    try:
                        self.current_prediction, self.current_confidence = self.result_queue.get_nowait()
                    except queue.Empty:
                        break
                
                # Draw info on frame
                display_frame = self.draw_info_on_frame(frame)
                
                # Show frame
                cv2.imshow('Areca Nut Detection with Relay Control', display_frame)
                
                # Check for quit
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("\n👋 Stopping detection system...")
                    break
                    
        except KeyboardInterrupt:
            print("\n👋 Detection interrupted by user...")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.running = False
        
        if self.detection_thread and self.detection_thread.is_alive():
            self.detection_thread.join(timeout=2)
        
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        
        cv2.destroyAllWindows()
        
        # Cleanup relays
        self.relay_controller.cleanup()
        
        print("✅ Detection system stopped")
        print("🏁 All resources cleaned up")

def main():
    """Main function"""
    try:
        # Initialize and run detector
        detector = ArecaDetectorWithRelay()
        detector.run()
        
    except FileNotFoundError as e:
        print(f"❌ Model file error: {e}")
        print("💡 Please ensure you have copied your trained model to models/best.pt")
    except RuntimeError as e:
        print(f"❌ Camera error: {e}")
        print("💡 Please check your camera connection.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        print("🏁 Program finished")

if __name__ == "__main__":
    main()