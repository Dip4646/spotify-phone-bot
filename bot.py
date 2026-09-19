import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# 1. שליפת המפתחות מכל שם משתנה אפשרי (SPOTIPY או SPOTIFY)
CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID') or os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET') or os.environ.get('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI') or os.environ.get('SPOTIFY_REDIRECT_URI') or 'http://localhost:8888/callback'

# פרטי המערכת של ימות המשיח
YEMOT_SYSTEM_NUMBER = os.environ.get('YEMOT_SYSTEM_NUMBER')
YEMOT_PASSWORD = os.environ.get('YEMOT_PASSWORD')

def main():
    print("Starting sync from Spotify to Yemot...")
    
    # בדיקה שהמפתחות אכן קיימים
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError(f"Missing Spotify Credentials! ID: {bool(CLIENT_ID)}, Secret: {bool(CLIENT_SECRET)}")

    # 2. יצירת החיבור לספוטיפיי באופן מפורש
    auth_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    print("Successfully authenticated with Spotify!")

if __name__ == "__main__":
    main()
