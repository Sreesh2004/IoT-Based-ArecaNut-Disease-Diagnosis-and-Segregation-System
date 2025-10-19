#!/usr/bin/env python3
"""
Relay Test Script for Raspberry Pi 3+
=====================================
This script tests the 2-channel relay module independently
to ensure proper hardware connections before running the main detection system.
"""

import time
import sys

# Try to import RPi.GPIO
try:
    import RPi.GPIO as GPIO
    print("✅ RPi.GPIO imported successfully")
    RPI_AVAILABLE = True
except ImportError:
    print("❌ RPi.GPIO not available")
    print("💡 This script must be run on a Raspberry Pi with RPi.GPIO installed")
    sys.exit(1)

class RelayTester:
    def __init__(self, relay1_pin=18, relay2_pin=19):
        self.relay1_pin = relay1_pin
        self.relay2_pin = relay2_pin
        
        print(f"🔧 Initializing relay test - GPIO {relay1_pin} and GPIO {relay2_pin}")
        
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Setup pins as outputs
        GPIO.setup(self.relay1_pin, GPIO.OUT)
        GPIO.setup(self.relay2_pin, GPIO.OUT)
        
        # Initialize relays as OFF
        GPIO.output(self.relay1_pin, GPIO.HIGH)  # HIGH = OFF
        GPIO.output(self.relay2_pin, GPIO.HIGH)  # HIGH = OFF
        
        print("✅ GPIO setup completed")
    
    def test_relay1(self, duration=2):
        """Test relay 1"""
        print(f"🔴 Testing Relay 1 (GPIO {self.relay1_pin}) for {duration}s...")
        GPIO.output(self.relay1_pin, GPIO.LOW)   # LOW = ON
        time.sleep(duration)
        GPIO.output(self.relay1_pin, GPIO.HIGH)  # HIGH = OFF
        print("⚫ Relay 1 test completed")
    
    def test_relay2(self, duration=2):
        """Test relay 2"""
        print(f"🔴 Testing Relay 2 (GPIO {self.relay2_pin}) for {duration}s...")
        GPIO.output(self.relay2_pin, GPIO.LOW)   # LOW = ON
        time.sleep(duration)
        GPIO.output(self.relay2_pin, GPIO.HIGH)  # HIGH = OFF
        print("⚫ Relay 2 test completed")
    
    def test_both_relays(self, duration=2):
        """Test both relays simultaneously"""
        print(f"🔴🔴 Testing BOTH relays for {duration}s...")
        GPIO.output(self.relay1_pin, GPIO.LOW)   # LOW = ON
        GPIO.output(self.relay2_pin, GPIO.LOW)   # LOW = ON
        time.sleep(duration)
        GPIO.output(self.relay1_pin, GPIO.HIGH)  # HIGH = OFF
        GPIO.output(self.relay2_pin, GPIO.HIGH)  # HIGH = OFF
        print("⚫⚫ Both relays test completed")
    
    def interactive_test(self):
        """Interactive relay testing"""
        print("\n🎮 Interactive Relay Test Mode")
        print("Commands:")
        print("  1 - Test Relay 1")
        print("  2 - Test Relay 2") 
        print("  3 - Test Both Relays")
        print("  q - Quit")
        
        while True:
            try:
                cmd = input("\nEnter command: ").strip().lower()
                
                if cmd == '1':
                    self.test_relay1()
                elif cmd == '2':
                    self.test_relay2()
                elif cmd == '3':
                    self.test_both_relays()
                elif cmd == 'q':
                    break
                else:
                    print("❌ Invalid command. Use 1, 2, 3, or q")
                    
            except KeyboardInterrupt:
                break
        
        print("\n👋 Exiting interactive mode...")
    
    def cleanup(self):
        """Clean up GPIO"""
        GPIO.cleanup()
        print("✅ GPIO cleanup completed")

def main():
    print("🔌 Raspberry Pi Relay Test Utility")
    print("="*40)
    
    try:
        # Initialize tester with default GPIO pins
        tester = RelayTester(relay1_pin=18, relay2_pin=19)
        
        print("\n📋 Hardware Check:")
        print("   - Relay Module VCC -> Pi Pin 2 (5V)")
        print("   - Relay Module GND -> Pi Pin 6 (GND)")
        print("   - Relay Module IN1 -> Pi Pin 12 (GPIO 18)")
        print("   - Relay Module IN2 -> Pi Pin 35 (GPIO 19)")
        print("\n⚠️  CAUTION: Ensure no high-power devices are connected during testing!")
        
        # Run automatic tests
        print("\n🔄 Running automatic tests...")
        time.sleep(2)
        
        print("\nStep 1: Testing Relay 1...")
        tester.test_relay1(2)
        time.sleep(1)
        
        print("\nStep 2: Testing Relay 2...")
        tester.test_relay2(2)
        time.sleep(1)
        
        print("\nStep 3: Testing Both Relays...")
        tester.test_both_relays(2)
        time.sleep(1)
        
        print("\n✅ Automatic tests completed!")
        
        # Ask for interactive mode
        response = input("\nDo you want to enter interactive test mode? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            tester.interactive_test()
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
    
    finally:
        if 'tester' in locals():
            tester.cleanup()
        print("🏁 Relay test completed")

if __name__ == "__main__":
    main()