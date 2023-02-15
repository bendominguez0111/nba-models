import os
from datetime import date

import pandas as pd

from config import ODDS_API_KEY
from model.odds_api import OddsAPI

def run_model():

    """
    Runs the model and returns the results
    """

    model = None

    client = OddsAPI(api_key=ODDS_API_KEY)
    today = date.today().strftime("%Y_%m_%d")

    #save on requests made per day
    if os.path.exists(f'exports/player_props/{today}.csv'):
        df = pd.read_csv(f'exports/player_props/{today}.csv')
    else:
        df = client.convert_player_props_to_df(save=True)

    print(df.head())

    return model