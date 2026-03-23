import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="user-modify-playback-state user-read-playback-state"
))

def get_active_device():
    devices = sp.devices()
    for device in devices['devices']:
        if device['is_active']:
            return device['id']
    if devices['devices']:
        return devices['devices'][0]['id']
    return None

def play():
    sp.transfer_playback(device_id=get_active_device(), force_play=True)

def pause():
    sp.pause_playback()

def next_song():
    sp.next_track()

def prev_song():
    sp.previous_track()