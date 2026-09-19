import os
import sys
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# הגדרת הלוגים להצגת הודעות ברורות ב-GitHub Actions
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_env_variable(keys, default=""):
    """שליפת משתנה סביבה מתוך רשימת שמות אפשריים"""
    for key in keys:
        val = os.environ.get(key)
        if val and val.strip():
            return val.strip()
    return default

# 1. שליפת הפרטים מתוך משתני הסביבה (או הזנה ישירה במידת הצורך)
CLIENT_ID = get_env_variable(['SPOTIPY_CLIENT_ID', 'SPOTIFY_CLIENT_ID']) or "הכנס_כאן_את_ה-CLIENT_ID_אם_תרצה"
CLIENT_SECRET = get_env_variable(['SPOTIPY_CLIENT_SECRET', 'SPOTIFY_CLIENT_SECRET']) or "הכנס_כאן_את_ה-CLIENT_SECRET_אם_תרצה"

def main():
    logging.info("=== מתחיל סנכרון מול Spotify ===")

    # בדיקה מקיפה אם המפתחות קיימים
    if not CLIENT_ID or "הכנס_כאן" in CLIENT_ID:
        logging.error("❌ חסר SPOTIPY_CLIENT_ID במערכת!")
    if not CLIENT_SECRET or "הכנס_כאן" in CLIENT_SECRET:
        logging.error("❌ חסר SPOTIPY_CLIENT_SECRET במערכת!")

    if not CLIENT_ID or not CLIENT_SECRET or "הכנס_כאן" in CLIENT_ID or "הכנס_כאן" in CLIENT_SECRET:
        raise ValueError("Spotify Credentials are missing! Please check GitHub Secrets or bot.py")

    # 2. התחברות לספוטיפיי עם המפתחות המפורשים
    auth_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # 3. שאילתת בדיקה לוודא שהאימות עובד
    sp.search(q="test", limit=1)
    logging.info("✅ התחברות לספוטיפיי עברה בהצלחה מלאה!")

if __name__ == "__main__":
    main()
