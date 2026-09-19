import os
import sys
import logging
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# הגדרת לוגים
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# קריאת משתני סביבה
client_id = os.environ.get('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')

# בדיקת משתני סביבה
if not client_id or not client_secret:
    logging.error("X שגיאה: המשנים SPOTIPY_CLIENT_ID או SPOTIPY_CLIENT_SECRET ריקים ב-GitHub!")
    sys.exit(1)

try:
    # תיקון: שימוש בסוגריים עגולים () במקום מסולסלים {}
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    sp = spotipy.Spotify(auth_manager=client_credentials_manager)
    logging.info("V ההתחברות לספוטיפיי עברה בהצלחה!")
except Exception as e:
    logging.error(f"X שגיאת תואמות מול Spotify: {e}")
    sys.exit(1)
