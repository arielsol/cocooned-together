import time
import sys
import pygame
import global_vars

is_playing = False

def init_audio():
    try:
        pygame.mixer.init()
        print(f"Audio mixer initialized.")
    except Exception as e:
        print(f"Failed to initialize audio mixer: {e}")
        sys.exit(1)

def play_audio(fade_in_s=global_vars.FADEIN_TIME):
    global is_playing

    if not is_playing:
        fade_in_ms = int(fade_in_s * 1000)

        print(f"Playing {global_vars.AUDIO_FILE}")
        pygame.mixer.music.stop()
        pygame.mixer.music.load(global_vars.AUDIO_FILE)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(loops=-1, fade_ms=fade_in_ms)
        
        is_playing = True

def stop_audio(fade_out_s=global_vars.FADEOUT_TIME):
    global is_playing
    
    if is_playing:
        fade_out_ms = int(fade_out_s * 1000)
        print(f"Stopping {global_vars.AUDIO_FILE}")
        pygame.mixer.music.fadeout(fade_out_ms)
        
        is_playing = False

def quit_audio():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.quit()