import logging
import os
import sys

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

#Authentication with APIs
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
ODDS_API_KEY = os.getenv('ODDS_API_KEY')

RAPID_API_HOST = "api-basketball.p.rapidapi.com"

# file stuff
base_dir = os.path.dirname(os.path.abspath(__file__))
export_folder = os.path.join(base_dir, 'exports')

# betting model settings
KELLY_CRITERION_SETTING = 0.5