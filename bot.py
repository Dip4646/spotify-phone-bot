import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# שליפת המפתחות מהסודות ב-GitHub
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
YEMOT_SYSTEM_NUMBER = os.getenv("YEMOT_SYSTEM_NUMBER")
YEMOT_PASSWORD = os.getenv("YEMOT_PASSWORD")

def main():
    print("התחברת בהצלחה למערכת!")
    print(f"עובד מול מערכת ימות המשיח מספר: {YEMOT_SYSTEM_NUMBER}")

if __name__ == "__main__":
    main()
