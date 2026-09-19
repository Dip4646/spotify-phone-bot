import os
import sys
import logging
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyException

# הגדרת הלוגים למעקב ברור ב-GitHub Actions
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def get_env_variable(keys, default=None):
    """שליפת משתנה סביבה מתוך כמה שמות אפשריים"""
    for key in keys:
        val = os.environ.get(key)
        if val:
            return val
    return default

# 1. טעינת פרטי ספוטיפיי (תומך בכל וריאציה של שם משתנה)
CLIENT_ID = get_env_variable(['SPOTIPY_CLIENT_ID', 'SPOTIFY_CLIENT_ID'])
CLIENT_SECRET = get_env_variable(['SPOTIPY_CLIENT_SECRET', 'SPOTIFY_CLIENT_SECRET'])
REDIRECT_URI = get_env_variable(['SPOTIPY_REDIRECT_URI', 'SPOTIFY_REDIRECT_URI'], 'http://localhost:8888/callback')

# 2. טעינת פרטי ימות המשיח
YEMOT_SYSTEM_NUMBER = get_env_variable(['YEMOT_SYSTEM_NUMBER', 'YEMOT_PHONE'])
YEMOT_PASSWORD = get_env_variable(['YEMOT_PASSWORD', 'YEMOT_PASS'])

def init_spotify():
    """אימות מול ספוטיפיי עם טיפול בשגיאות"""
    logging.info("מתחיל אימות מול Spotify...")
    
    if not CLIENT_ID or not CLIENT_SECRET:
        logging.error("❌ חסרים מפתחות אימות של ספוטיפיי! ודא שהגדרת ב-GitHub Secrets את SPOTIPY_CLIENT_ID ו-SPOTIPY_CLIENT_SECRET")
        raise ValueError("Missing Spotify Credentials")

    try:
        auth_manager = SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        # בדיקת חיבור על ידי שאילתת ניסיון
        sp.search(q="test", limit=1)
        logging.info("✅ התחברות לספוטיפיי עברה בהצלחה!")
        return sp
    except SpotifyException as e:
        logging.error(f"❌ שגיאת אימות בספוטיפיי: {e}")
        raise
    except Exception as e:
        logging.error(f"❌ שגיאה בלתי צפויה בהתחברות לספוטיפיי: {e}")
        raise

def sync_to_yemot(data):
    """סנכרון הנתונים למערכת ימות המשיח"""
    if not YEMOT_SYSTEM_NUMBER or not YEMOT_PASSWORD:
        logging.warning("⚠️ לא הוגדרו פרטי ימות המשיח (YEMOT_SYSTEM_NUMBER / YEMOT_PASSWORD), מדלג על שליחה.")
        return

    logging.info("שולח עדכון למערכת ימות המשיח...")
    url = "https://www.call2all.co.il/ym/api/Login"
    params = {
        'token': f"{YEMOT_SYSTEM_NUMBER}:{YEMOT_PASSWORD}"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            logging.info("✅ התחברות לימות המשיח עברה בהצלחה!")
        else:
            logging.error(f"❌ שגיאה בהתחברות לימות המשיח: {response.status_code}")
    except Exception as e:
        logging.error(f"❌ שגיאה בתקשורת מול ימות המשיח: {e}")

def main():
    logging.info("=== התחלת הרצת בוט ספוטיפיי לטלפון ===")
    
    # הפעלת האימות בספוטיפיי
    sp = init_spotify()
    
    # סנכרון מול ימות המשיח
    sync_to_yemot(sp)
    
    logging.info("=== הריצה הסתיימה בהצלחה! ===")

if __name__ == "__main__":
    main()
