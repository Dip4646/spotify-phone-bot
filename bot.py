import os
import re
import sys
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# שליפת נתוני גישה ממשתני הסביבה
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
YEMOT_SYSTEM_NUMBER = os.getenv("YEMOT_SYSTEM_NUMBER")
YEMOT_PASSWORD = os.getenv("YEMOT_PASSWORD")

# כתובת הפלייליסט של ספוטיפיי (מזוהה ונקייה)
PLAYLIST_URL = "https://open.spotify.com/playlist/6fypePpbc1nkCaMCBCB9KP"
YEMOT_TARGET_FOLDER = "ivar/1"  # מעלה ישירות לשלוחה 1

def clean_filename(filename: str) -> str:
    """מנקה תווים שאינם חוקיים במערכת הקבצים של ימות המשיח"""
    filename = re.sub(r'[/\\:*?"<>|]', '', filename)
    filename = filename.replace(' ', '_')
    return filename[:60]  # הגבלת אורך שם הקובץ

def main():
    print("==========================================")
    print("🚀 מתחיל תהליך סנכרון ספוטיפיי -> ימות המשיח")
    print("==========================================")

    # בדיקת משתני סביבה
    missing_vars = []
    if not SPOTIFY_CLIENT_ID: missing_vars.append("SPOTIFY_CLIENT_ID")
    if not SPOTIFY_CLIENT_SECRET: missing_vars.append("SPOTIFY_CLIENT_SECRET")
    if not YEMOT_SYSTEM_NUMBER: missing_vars.append("YEMOT_SYSTEM_NUMBER")
    if not YEMOT_PASSWORD: missing_vars.append("YEMOT_PASSWORD")

    if missing_vars:
        print(f"❌ שגיאה: חסרים משתני הסביבה הבאים ב-GitHub Secrets: {', '.join(missing_vars)}")
        sys.exit(1)

    # חיבור לספוטיפיי
    try:
        auth_manager = SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        print("✅ התחברות ל-Spotify API בוצעה בהצלחה")
    except Exception as e:
        print(f"❌ שגיאה בהתחברות לספוטיפיי: {e}")
        sys.exit(1)

    # חילוץ מזהה פלייליסט
    playlist_id = PLAYLIST_URL.split("/")[-1].split("?")[0]
    print(f"🎵 מושך נתונים עבור פלייליסט מזהה: {playlist_id}")

    try:
        results = sp.playlist_items(playlist_id, limit=100)
        items = results.get('items', [])
        print(f"📊 נמצאו {len(items)} פריטים בפלייליסט")
    except Exception as e:
        print(f"❌ שגיאה במשיכת הפלייליסט מספוטיפיי: {e}")
        sys.exit(1)

    token = f"{YEMOT_SYSTEM_NUMBER}:{YEMOT_PASSWORD}"
    uploaded_count = 0
    skipped_count = 0

    print("\n------------------------------------------")
    print("תחילת העלאת שירים לימות המשיח...")
    print("------------------------------------------")

    for idx, item in enumerate(items, 1):
        track = item.get('track')
        if not track:
            continue

        track_title = track.get('name', 'Unknown')
        artists = ", ".join([artist['name'] for artist in track.get('artists', [])])
        preview_url = track.get('preview_url')

        clean_title = clean_filename(f"{idx:02d}_{track_title}")
        file_name = f"{clean_title}.mp3"

        if not preview_url:
            print(f"⚠️ [{idx}/{len(items)}] דלג: ל-" {track_title} - {artists}" אין Preview URL זמין בספוטיפיי")
            skipped_count += 1
            continue

        print(f"🔄 [{idx}/{len(items)}] מוריד ומעלה: {track_title} ({artists})...")

        try:
            # הורדת השיר לזיכרון
            audio_data = requests.get(preview_url, timeout=15).content

            # העלאה לימות המשיח
            yemot_url = "https://www.call2all.co.il/ym/api/UploadFile"
            payload = {
                'token': token,
                'path': f"{YEMOT_TARGET_FOLDER}/{file_name}",
                'convertAudio': 'true'
            }
            files = [('file', (file_name, audio_data, 'audio/mpeg'))]

            response = requests.post(yemot_url, data=payload, files=files, timeout=30)
            res_json = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}

            if response.status_code == 200 and res_json.get('responseStatus') == 'OK':
                print(f"  ✅ נקלט בהצלחה בשלוחה 1: {file_name}")
                uploaded_count += 1
            else:
                print(f"  ❌ שגיאה בהעלאה: סטטוס {response.status_code}, תגובה: {response.text}")

        except Exception as err:
            print(f"  ❌ שגיאה במהלך העיבוד של השיר {track_title}: {err}")

    print("\n==========================================")
    print(f"🏁 הסנכרון הסתיים!")
    print(f"✔️ הועלו בהצלחה: {uploaded_count} שירים")
    print(f"⏭️ דולגו (ללא Preview): {skipped_count} שירים")
    print("==========================================")

if __name__ == "__main__":
    main()
