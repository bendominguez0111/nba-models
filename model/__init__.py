import os
from datetime import date

import pandas as pd

from config import ODDS_API_KEY
from model.odds_api import OddsAPI
from model.stats_api import StatsAPI

from config import RAPID_API_KEY, ODDS_API_KEY

def run_model():

    """
    Runs the model and returns the results
    """

    model = None

    odds_api = OddsAPI(api_key=ODDS_API_KEY)
    stats_api = StatsAPI(api_key=RAPID_API_KEY)

    today = date.today().strftime('%Y_%m_%d')
    if not os.path.exists(f'/exports/player_props/{today}.csv'):
        odds_df = odds_api.convert_player_props_to_df(save=True)
    else:
        odds_df = pd.read_csv(f'/exports/player_props/{today}.csv')
    
    print(odds_df.head())
    return model