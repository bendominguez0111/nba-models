import logging
import os
import sys
from datetime import date

from dotenv import load_dotenv

load_dotenv()

#logging settings
root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

STR_TODAY = date.today().strftime('%Y_%m_%d')
#Authentication with APIs
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
ODDS_API_KEY = os.getenv('ODDS_API_KEY')

RAPID_API_HOST = "api-basketball.p.rapidapi.com"

# file stuff
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_FOLDER = os.path.join(BASE_DIR, 'exports')

# betting model settings
KELLY_CRITERION_SETTING = 0.5
BOOKS = ['bovada']