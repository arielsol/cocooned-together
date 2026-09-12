import time
import threading
from rpi_ws281x import PixelStrip, Color
import global_vars

strip = None
target_brightness = 0
current_brightness = 0
lock = threading.Lock()

def _led_worker():
    """Background thread that continuously steps current_brightness toward target_brightness."""
    global current_brightness
    
    ticks = max(1, global_vars.LED_FADE_S * 33.0)
    step_size = max(1, int(global_vars.LED_BRIGHTNESS / ticks))

    while True:
        with lock:
            if current_brightness < target_brightness:
                current_brightness = min(target_brightness, current_brightness + step_size)
                strip.setBrightness(current_brightness)
                strip.show()
            elif current_brightness > target_brightness:
                current_brightness = max(target_brightness, current_brightness - step_size)
                strip.setBrightness(current_brightness)
                strip.show()

        time.sleep(0.03)

def init_leds():
    global strip, current_brightness, target_brightness

    try:
        strip = PixelStrip(
            global_vars.LED_COUNT,
            global_vars.LED_PIN,
            800000,                  # Signal frequency (800kHz)
            10,                      # DMA channel
            False,                   # Invert signal
            0                        # Start at 0 brightness
        )
        strip.begin()

        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(*global_vars.LED_COLOR))
            
        strip.setBrightness(0)
        strip.show()

        current_brightness = 0
        target_brightness = 0

        worker_thread = threading.Thread(target=_led_worker, daemon=True)
        worker_thread.start()

        print("LED strip initialized")
    except Exception as e:
        strip = None
        print(f"Failed to initialize LED strip: {e}")

def turn_on_leds():
    global target_brightness

    with lock:
        target_brightness = global_vars.LED_BRIGHTNESS

def turn_off_leds():
    global target_brightness

    with lock:
        target_brightness = 0

def quit_leds():
    global current_brightness, target_brightness

    with lock:
        target_brightness = 0
        current_brightness = 0
        strip.setBrightness(0)
        strip.show()
