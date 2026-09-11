import time
import sys
from gpiozero import DigitalInputDevice
import global_vars
import handle_audio
import handle_lights

def main():
    handle_audio.init_audio()
    handle_lights.init_leds()
    
    sensor = DigitalInputDevice(global_vars.OUT_PIN, pull_up=False)
    
    print(f"Listening for presence on GPIO {global_vars.OUT_PIN}...")
    try:
        while True:
            if sensor.is_active:  # HIGH signal detected from LD2410C OUT pin
                handle_audio.play_audio()
                handle_lights.turn_on_leds()
            else: 
                handle_audio.stop_audio()
                handle_lights.turn_off_leds()
            
            time.sleep(global_vars.DETECTION_COOLDOWN)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
        handle_audio.quit_audio()
        handle_lights.quit_leds()
        sys.exit(0)

if __name__ == "__main__":
    main()