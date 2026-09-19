import os
import sys
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# הגדרת הלוגים למעקב בריצה ב-GitHub Actions
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_env_variable(keys):
    """שליפת משתנה סביבה מתוך כמה שמות אפשריים"""
    for key in keys:
        val = os.environ.get(key)
        if val and val.strip():
            return val.strip()
    return None

# 1. טעינת פרטי ה-API מכל משתנה סביבה אפשרי (SPOTIPY או SPOTIFY)
CLIENT_ID = get_env_variable(['SPOTIPY_CLIENT_ID', 'SPOTIFY_CLIENT_ID'])
CLIENT_SECRET = get_env_variable(['SPOTIPY_CLIENT_SECRET', 'SPOTIFY_CLIENT_SECRET'])

def main():
    logging.info("=== מתחיל סנכרון מול ספוטיפיי ===")

    # בדיקה מקיפה אם המפתחות התקבלו
    if not CLIENT_ID or not CLIENT_SECRET:
        logging.error("❌ לא נמצאו מפתחות אימות!")
        logging.error(f"סטטוס CLIENT_ID: {'קיים' if CLIENT_ID else 'חסר'}")
        logging.error(f"סטטוס CLIENT_SECRET: {'קיים' if CLIENT_SECRET else 'חסר'}")
        raise ValueError("Spotify credentials are missing from environment variables.")

    try:
        # התחברות לספוטיפיי עם המפתחות המפורשים
        auth_manager = SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        # בדיקת תקשורת (שאילתת ניסיון לספוטיפיי)
        sp.search(q="test", limit=1)
        logging.info("✅ התחברות לספוטיפיי עברה בהצלחה מלאה!")

    except Exception as e:
        logging.error(f"❌ שגיאה בחיבור לספוטיפיי: {e}")
        raise e

if __name__ == "__main__":
    main()
