import time
import math
import threading
import atexit
from rpi_ws281x import PixelStrip, Color, ws
import global_vars

strip = None
target_brightness = 0
current_brightness = 0
lock = threading.Lock()

active_pulses = {}  # Format: { group_id: {"active": True, "thread": Thread} }

def init_leds():
    global strip, current_brightness, target_brightness

    try:
        strip = PixelStrip(
            global_vars.LED_COUNT,       # num
            global_vars.LED_PIN,         # pin
            800000,                      # freq_hz (800kHz)
            10,                          # dma
            False,                       # invert
            0,                           # brightness
            0,                           # channel
            ws.WS2811_STRIP_RBG          # strip_type
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

        print("LED strip initialized.")

    except Exception as e:
        strip = None
        print(f"Failed to initialize LED strip: {e}")

def _led_worker():
    print("LED worker thread active.")
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

            if current_brightness > 0:
                strip.show()

        time.sleep(0.03)

def _pulse_group_worker(group_id, center_pixel, radius, bpm):
    print("LED pulse thread active.")

    omega = (2 * math.pi * bpm) / 60.0
    base_r, base_g, base_b = global_vars.LED_COLOR
    start_time = time.time()

    affected_pixels = []
    pixel_peak_factors = {}

    for i in range(center_pixel - radius, center_pixel + radius + 1):
        distance = abs(i - center_pixel)
        
        if distance >= radius:
            peak_factor = 0.5 
        else:
            peak_factor = 1.0 - (0.5 * (distance / radius))
            
        affected_pixels.append(i)
        pixel_peak_factors[i] = peak_factor

    while active_pulses.get(group_id, {}).get("active", False):
        elapsed = time.time() - start_time
        wave = 0.5 + 0.5 * math.sin(omega * elapsed)

        with lock:
            if strip is not None:
                for idx in affected_pixels:
                    if 0 <= idx < strip.numPixels():
                        peak = pixel_peak_factors[idx]
                        factor = 0.5 + (wave * (peak - 0.5))

                        pulsed_color = Color(
                            int(base_r * factor),
                            int(base_g * factor),
                            int(base_b * factor)
                        )
                        strip.setPixelColor(idx, pulsed_color)

        time.sleep(0.03)

    with lock:
        if strip is not None:
            static_color = Color(*global_vars.LED_COLOR)
            for idx in affected_pixels:
                if 0 <= idx < strip.numPixels():
                    strip.setPixelColor(idx, static_color)


def pulse_leds(center_pixel, bpm, radius=global_vars.PULSE_RADIUS, group_id="default"):
    min_pixel = center_pixel - radius
    max_pixel = center_pixel + radius

    if min_pixel < 0 or max_pixel >= global_vars.LED_COUNT:
        print(f"ERROR: Pulse zone around pixel {center_pixel} (span: {min_pixel}..{max_pixel}) exceeds LED_COUNT ({global_vars.LED_COUNT}).")
        return

    stop_pulse(group_id)

    active_pulses[group_id] = {"active": True, "thread": None}

    thread = threading.Thread(
        target=_pulse_group_worker,
        args=(group_id, center_pixel, radius, bpm),
        daemon=True
    )
    active_pulses[group_id]["thread"] = thread
    thread.start()

def start_all_pulses():
    print("Starting LED pulses...")
    for i in global_vars.HEARTBEAT_DATA:
        pulse_leds(
            center_pixel=i["center_pixel"],
            bpm=i["bpm"],
            group_id=i["group_id"]
        )

def stop_pulse(group_id="default"): # Stops one pulse effect
    if group_id in active_pulses:
        active_pulses[group_id]["active"] = False
        thread = active_pulses[group_id].get("thread")
        if thread and thread.is_alive():
            thread.join(timeout=0.1)
        del active_pulses[group_id]

def stop_all_pulses(): # Stops all pulse effects
    group_ids = list(active_pulses.keys())
    for gid in group_ids:
        stop_pulse(gid)

def turn_on_leds():
    global target_brightness

    with lock:
        if global_vars.SHOW_PULSE:
            target_brightness = int(0.5 * global_vars.LED_BRIGHTNESS)
        else:
            target_brightness = global_vars.LED_BRIGHTNESS

def turn_off_leds():
    global target_brightness

    with lock:
        target_brightness = 0

def quit_leds():
    global current_brightness, target_brightness

    stop_all_pulses()

    with lock:
        target_brightness = 0
        current_brightness = 0
        strip.setBrightness(0)
        strip.show()

def cleanup():
    global strip

    if strip is not None:
        try:
            strip.setBrightness(0)
            strip.show()
            strip._cleanup()
        except Exception:
            pass

atexit.register(cleanup)