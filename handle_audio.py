import time
import sys
import pygame
import global_vars

is_playing = False
playback_position = 0.0  # Saved playback position in seconds
play_start_time = 0.0    # Timestamp when play() was last called
track_duration = global_vars.TRACK_DURATION

def init_audio():
    try:
        import os
        os.environ['SDL_AUDIODRIVER'] = 'alsa'
        os.environ['AUDIODEV'] = 'plughw:1,0'
        pygame.mixer.init()
        print(f"Audio mixer initialized.")
        reset_position()
    except Exception as e:
        print(f"Failed to initialize audio mixer: {e}")
        sys.exit(1)

def reset_position():
    global playback_position
    playback_position = 0.0

def play_audio(fade_in_s=global_vars.FADEIN_TIME):
    global is_playing, playback_position, play_start_time

    if not is_playing:
        fade_in_ms = int(fade_in_s * 1000)

        print(f"Playing {global_vars.AUDIO_FILE} from {playback_position:.1f}s")
        pygame.mixer.music.stop()
        pygame.mixer.music.load(global_vars.AUDIO_FILE)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(loops=-1, start=playback_position, fade_ms=fade_in_ms)
        
        play_start_time = time.time()
        is_playing = True

def stop_audio(fade_out_s=global_vars.FADEOUT_TIME):
    global is_playing, playback_position, play_start_time

    elapsed_session = time.time() - play_start_time
    playback_position += elapsed_session

    if track_duration > 0:
            playback_position %= track_duration

    if is_playing:
        fade_out_ms = int(fade_out_s * 1000)
        print(f"Stopping {global_vars.AUDIO_FILE} at {playback_position:.1f}s")
        pygame.mixer.music.fadeout(fade_out_ms)
        
        is_playing = False

def quit_audio():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.quit()
