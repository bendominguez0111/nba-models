import os

from dotenv import load_dotenv
from oddsapi import OddsApiClient

load_dotenv()

ODDS_API_KEY = os.getenv('ODDS_API_KEY')
odds_api_client = OddsApiClient(api_key=ODDS_API_KEY)

base_dir = os.path.dirname(os.path.abspath(__file__))
export_folder = os.path.join(base_dir, 'exports')