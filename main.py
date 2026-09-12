import os
os.environ['SDL_AUDIODRIVER'] = 'alsa'
os.environ['AUDIODEV'] = 'hw:0,0'
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
    
    current_presence = False
    vacant_since = None
    
    print(f"Listening for presence on GPIO {global_vars.OUT_PIN}...")
    try:
        while True:
            presence_detected = sensor.is_active  # HIGH signal from LD2410C OUT pin

            if presence_detected and not current_presence:
                print("Presence detected.")
                current_presence = True

                if vacant_since is not None:
                    vacant_duration = time.time() - vacant_since
                    if vacant_duration >= global_vars.RESET_TIME:
                        handle_audio.reset_position()

                handle_audio.play_audio()
                handle_lights.turn_on_leds()

            elif not presence_detected and current_presence:
                print("Presence lost.")
                current_presence = False
                vacant_since = time.time() 

                handle_audio.stop_audio()
                handle_lights.turn_off_leds()
            
            time.sleep(global_vars.DETECTION_COOLDOWN)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
        if handle_audio.is_playing:
            handle_audio.stop_audio(fade_out_s=0.1)
        
        handle_audio.quit_audio()
        handle_lights.quit_leds()

        sys.exit(0)

if __name__ == "__main__":
    main()
