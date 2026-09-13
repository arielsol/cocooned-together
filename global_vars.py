import os

# === GPIO ===
OUT_PIN = 17    # Pin listening to mmWave sensor (BCM 17 / Physical 11)
LED_PIN = 18    # LED Data pin (BCM 18 / Physical Pin 12), must support PWM

# === MMWAVE SENSOR ===
DETECTION_COOLDOWN = 0.5    # How often to check for presence, in seconds

# === AUDIO ===
AUDIO_FILE = "/home/mg/cocooned-together/audio/CocoonRemixEdit_260912.wav" # File path of audio file to play
TRACK_DURATION = 365    # Duration of audio file, in seconds - better to estimate SHORTER than longer
MAX_VOLUME = 1.0        # Full volume scale (0.0 to 1.0)
FADEIN_TIME = 0.2       # Duration of fade-in, in seconds
FADEOUT_TIME = 1.5      # Duration of fade-out, in seconds
RESET_TIME = 3600       # Resets playback start time to beginning of file after this many seconds of no presence detected

# === LIGHTS ===
LED_COUNT = 100                 # Number of LEDs on strip
LED_BRIGHTNESS = 200            # Range: [0, 255]
LED_COLOR = (255, 180, 60)      # [0, 255] for R, G, B // warm white: (255, 180, 60) // Warm red: (255, 172, 184)
LED_FADE_S = 5                  # Duration of fade, in seconds
FADE_STEPS = 100                # Resolution of fade, in number of discrete steps
SHOW_PULSE = True               # If true, plays animation visualizing data below
PULSE_RADIUS = 3                # Radius affected by central pixel: center + PULSE_RADIUS pixels on each side

# === DATA TO VISUALIZE ===
HEARTBEAT_DATA = [              # 8 participants
    {
        "group_id": "S375",
        "center_pixel": 5,
        "bpm": 57,
    },
    {
        "group_id": "N272",
        "center_pixel": 15,
        "bpm": 74,
    },
    {
        "group_id": "U221",
        "center_pixel": 25,
        "bpm": 70,
    },
    {
        "group_id": "O593",
        "center_pixel": 35,
        "bpm": 78,
    },
    {
        "group_id": "J239",
        "center_pixel": 45,
        "bpm": 81,
    },
    {
        "group_id": "G601",
        "center_pixel": 55,
        "bpm": 93,
    },
    {
        "group_id": "H128",
        "center_pixel": 65,
        "bpm": 57,
    },
    {
        "group_id": "H111",
        "center_pixel": 75,
        "bpm": 64,
    },      
]
