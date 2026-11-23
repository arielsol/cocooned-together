# Cocooned Together

Cocooned Together is a multidisciplinary project that weaves fiber art, technology, and music into an immersive space for rest and collective care. Through community fiber workshops, participants' biometric data are translated into original music, culminating in a cocoon-like installation where visitors are invited to slow down, listen, and find comfort.

This repo is the installation's runtime: a Raspberry Pi script that senses when someone is inside the cocoon and responds with sound and light.

## How it works

An LD2410C mmWave radar sensor watches the space. When a visitor enters:

- The soundtrack fades in (0.2 s), resuming from wherever the last visitor left it.
- A 100-pixel WS281x LED strip fades up to warm white over 5 s.
- Optionally (`SHOW_PULSE`), eight zones on the strip pulse at the resting heart rates of eight workshop participants.

When the space empties, audio fades out over 1.5 s and the lights fade to black. If nobody has been inside for an hour (`RESET_TIME`), the next visitor hears the track from the beginning.

Playback position is tracked by wall-clock time, not queried from the mixer, so the piece feels continuous across visitors rather than restarting every time someone walks in.

## Hardware

| Part | Connection |
| --- | --- |
| Raspberry Pi (with `rpi_ws281x` support) | |
| LD2410C mmWave presence sensor | OUT → GPIO 17 (physical pin 11) |
| WS281x LED strip, 100 pixels, RBG byte order | DIN → GPIO 18 (physical pin 12, PWM) |
| Audio output | ALSA device `hw:0,0` |
| Speakers / amp | |

GPIO 18 drives the LEDs via PWM, which conflicts with the Pi's onboard analog audio. Use an external DAC or USB/HDMI audio. The ALSA device is set at the top of `main.py`; change `AUDIODEV` if your output isn't card 0.

Power the LED strip from its own 5 V supply and share ground with the Pi.

## Software setup

On Raspberry Pi OS:

```bash
sudo apt install git git-lfs python3-pip
git lfs install
git clone https://github.com/arielsol/cocooned-together.git /home/mg/cocooned-together
cd /home/mg/cocooned-together
sudo pip3 install pygame gpiozero rpi_ws281x --break-system-packages
```

`AUDIO_FILE` in `global_vars.py` is an absolute path (`/home/mg/cocooned-together/...`). Update it if you clone somewhere else.

## Running

`rpi_ws281x` needs root for DMA/PWM access:

```bash
sudo python3 main.py
```

`Ctrl+C` fades out the audio, blacks out the strip, and exits cleanly.

To test the strip on its own, `sudo python3 test_leds.py` lights all 100 pixels warm white for 10 seconds.

## Configuration

Everything tunable lives in `global_vars.py`.

| Setting | Default | Notes |
| --- | --- | --- |
| `OUT_PIN` | 17 | Sensor input (BCM) |
| `LED_PIN` | 18 | LED data (BCM), must be PWM-capable |
| `DETECTION_COOLDOWN` | 0.5 | Sensor poll interval, seconds |
| `AUDIO_FILE` | `.../CocoonRemixEdit_260912.wav` | Absolute path |
| `TRACK_DURATION` | 365 | Track length in seconds, used to wrap the resume position |
| `MAX_VOLUME` | 0.7 | Master volume |
| `FADEIN_TIME` / `FADEOUT_TIME` | 0.2 / 1.5 | Audio fades, seconds |
| `RESET_TIME` | 3600 | Seconds of vacancy before the track restarts from 0 |
| `LED_COUNT` | 100 | Pixels on the strip |
| `LED_BRIGHTNESS` | 200 | 0–255 |
| `LED_COLOR` | (255, 180, 60) | Warm white. Alt warm red: (255, 172, 184) |
| `LED_FADE_S` | 5 | Light fade duration, seconds |
| `SHOW_PULSE` | False | Enables heartbeat pulses |
| `PULSE_RADIUS` | 3 | Pixels on each side of a pulse center |
| `HEARTBEAT_DATA` | 8 entries | Participant ID, center pixel, BPM |

## Files

```
main.py           Presence loop: sensor polling, triggers audio and lights
handle_audio.py   pygame mixer playback, fades, resume-position tracking
handle_lights.py  LED strip init, brightness fade worker, heartbeat pulse threads
global_vars.py    All configuration
test_leds.py      Standalone strip test
audio/            Soundtrack (Git LFS)
```

## Known issues

- If the LED strip fails to initialize, the script keeps running audio-only, but `quit_leds()` throws on shutdown because it doesn't check for a missing strip.

## Credits

Ariel Sol, otodojo, and weathercitizen. 
Music by Marion Hayden.
