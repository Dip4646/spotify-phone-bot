import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

# שליפת המפתחות מהסודות
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
YEMOT_SYSTEM_NUMBER = os.getenv("YEMOT_SYSTEM_NUMBER")
YEMOT_PASSWORD = os.getenv("YEMOT_PASSWORD")

# הלינק לפלייליסט של ספוטיפיי לבחירתך
PLAYLIST_URL = "https://open.spotify.com/playlist/37i9dQZF1DXcBWAsP2311X"

def main():
    print("מתחיל סנכרון...")
    auth_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID, 
        client_secret=SPOTIFY_CLIENT_SECRET
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # שליפת פרטי הפלייליסט
    playlist_id = PLAYLIST_URL.split("/")[-1].split("?")[0]
    results = sp.playlist_items(playlist_id)

    print(f"נמצאו {len(results['items'])} שירים בפלייליסט.")

    for item in results['items']:
        track = item['track']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        preview_url = track['preview_url']

        print(f"מעבד: {track_name} - {artist_name}")

        if preview_url:
            # העלאת השיר לימות המשיח
            yemot_url = "https://www.call2all.co.il/ym/api/UploadFile"
            payload = {
                'token': f"{YEMOT_SYSTEM_NUMBER}:{YEMOT_PASSWORD}",
                'path': f"ivar/1/{track_name}.mp3",
                'convertAudio': 'true'
            }
            file_data = requests.get(preview_url).content
            files = [('file', (f"{track_name}.mp3", file_data, 'audio/mpeg'))]
            
            response = requests.post(yemot_url, data=payload, files=files)
            print(f"סטטוס העלאה: {response.status_code}")
        else:
            print(f"אין תצוגה מקדימה לשיר {track_name}")

if __name__ == "__main__":
    main()

