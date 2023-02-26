import os
from datetime import date

from dotenv import load_dotenv

load_dotenv()

DEBUG = int(os.getenv('DEBUG', 1))

STR_TODAY = date.today().strftime('%Y_%m_%d')

#Authentication with APIs
ODDS_API_KEY = os.getenv('ODDS_API_KEY')

# file stuff
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_FOLDER = os.path.join(BASE_DIR, 'exports')
LOGS_FOLDER = os.path.join(BASE_DIR, 'logs')