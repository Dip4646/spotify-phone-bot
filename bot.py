import os
import sys
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# קריאה ישירה למשתנים
client_id = os.environ.get('SPOTIPY_CLIENT_ID') or os.environ.get('SPOTIFY_CLIENT_ID') or ""
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET') or os.environ.get('SPOTIFY_CLIENT_SECRET') or ""

def main():
    logging.info("=== בדיקת משתני סביבה ===")
    logging.info(f"Client ID קיים? {bool(client_id)} (אורך: {len(client_id)})")
    logging.info(f"Client Secret קיים? {bool(client_secret)} (אורך: {len(client_secret)})")

    if not client_id or not client_secret:
        print("❌ שגיאה: המשתנים SPOTIPY_CLIENT_ID או SPOTIPY_CLIENT_SECRET ריקים ב-GitHub!")
        sys.exit(1)

    try:
        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        sp.search(q="test", limit=1)
        logging.info("✅ התחברות לספוטיפיי עברה בהצלחה!")
    except Exception as e:
        logging.error(f"❌ שגיאת אימות מול Spotify: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
