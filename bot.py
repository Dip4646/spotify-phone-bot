import os
import re
import sys
import subprocess
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
YEMOT_SYSTEM_NUMBER = os.getenv("YEMOT_SYSTEM_NUMBER")
YEMOT_PASSWORD = os.getenv("YEMOT_PASSWORD")

PLAYLIST_URL = "https://open.spotify.com/playlist/6fypePpbc1nkCaMCBCB9KP"
YEMOT_TARGET_FOLDER = "ivar/1"

def clean_filename(filename: str) -> str:
    filename = re.sub(r'[/\\:*?"<>|]', '', filename)
    filename = filename.replace(' ', '_')
    return filename[:60]

def main():
    print("==========================================")
    print("🚀 מתחיל סנכרון מלא מ-Spotify לימות המשיח")
    print("==========================================")

    auth_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    playlist_id = PLAYLIST_URL.split("/")[-1].split("?")[0]
    results = sp.playlist_items(playlist_id, limit=50)
    items = results.get('items', [])

    token = f"{YEMOT_SYSTEM_NUMBER}:{YEMOT_PASSWORD}"
    uploaded_count = 0

    for idx, item in enumerate(items, 1):
        track = item.get('track')
        if not track:
            continue

        track_title = track.get('name', 'Unknown')
        artists = ", ".join([artist['name'] for artist in track.get('artists', [])])
        search_query = f"{track_title} {artists} audio"
        clean_title = clean_filename(f"{idx:03d}_{track_title}")
        local_filename = f"{clean_title}.mp3"

        print(f"🔄 [{idx}/{len(items)}] מוריד את: {track_title} - {artists}")

        cmd = [
            "yt-dlp",
            "--default-search", "ytsearch",
            "-x",
            "--audio-format", "mp3",
            "-o", local_filename,
            search_query
        ]
        
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            if os.path.exists(local_filename):
                yemot_url = "https://www.call2all.co.il/ym/api/UploadFile"
                payload = {
                    'token': token,
                    'path': f"{YEMOT_TARGET_FOLDER}/{local_filename}",
                    'convertAudio': 'true'
                }
                
                with open(local_filename, 'rb') as f:
                    files = [('file', (local_filename, f, 'audio/mpeg'))]
                    res = requests.post(yemot_url, data=payload, files=files, timeout=60)
                
                print(f"  ✅ הועלה בהצלחה לימות המשיח: {local_filename}")
                uploaded_count += 1
                os.remove(local_filename)
            else:
                print(f"  ❌ ההורדה נכשלה עבור: {track_title}")

        except Exception as e:
            print(f"  ❌ שגיאה בעיבוד {track_title}: {e}")

    print(f"\n🏁 הסנכרון הסתיים! הועלו {uploaded_count} שירים לשלוחה 1.")

if __name__ == "__main__":
    main()
