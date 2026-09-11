import os

# === GPIO ===
OUT_PIN = 17 # Pin listening to mmWave sensor (BCM 17 / Physical 11)
LED_PIN = 18 # LED Data pin (BCM 18 / Physical Pin 12), must support PWM

# === AUDIO ===
AUDIO_FILE = os.path.expanduser("~/cocooned-together/audio/CocoonRemixEdit.wav") # File path of audio file to play
TRACK_DURATION = 360  # Duration of audio file, in seconds - better to estimate SHORTER than longer
MAX_VOLUME = 1.0    # Full volume scale (0.0 to 1.0)
FADEIN_TIME = 0.2     # Duration of fade-in, in seconds
FADEOUT_TIME = 1.5  # Duration of fade-out, in seconds
RESET_TIME = 3600   # Resets playback start time to beginning of file after this many seconds of no presence detected

# === LIGHTS ===
LED_COUNT = 100      # Number of LEDs on strip
LED_BRIGHTNESS = 200 # Range: [0, 255]
LED_COLOR = (255, 180, 60)
LED_FADE_S = 5     # Duration of fade, in seconds
FADE_STEPS = 100    # Resolution of fade

# === MMWAVE SENSOR ===
DETECTION_COOLDOWN = 0.5    # How often to check for presence, in seconds



'''
Ari's notes to self:
    We may need to account for some edge cases with people exiting and immediately entering or vice versa
    Could add a threshold time to prevent jitter
    Or the detection cooldown time could be increased, but then responsivity would suffer 

    To-do: data visualization LED behavior

    RX/TX mode instead of just OUT?

    Might need a multi-thread approach for fading edge cases... but that strikes me as overcomplicated
'''