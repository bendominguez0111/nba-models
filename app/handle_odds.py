from datetime import date

import pandas as pd

import requests

from config import (
    RETRIEVE_ODDS_ENDPOINT, EVENT_ODDS_ENDPOINT, ODDS_API_KEY, OddsAPISettings,
    export_folder
)


def convert_player_props_to_df(
        sport_key:OddsAPISettings.sports=OddsAPISettings.sports.nba,
        event_id:str='',
        region:OddsAPISettings.regions=OddsAPISettings.regions.us,
        markets:OddsAPISettings.markets=OddsAPISettings.markets.player_points,
        date_format:str='iso',
        odds_format:str='american',
        save:bool=False
    ) -> pd.DataFrame:
    """ This function converts the player props data from the API to a pandas DataFrame """
    return


def convert_totals_to_df(
        sport_key:str=OddsAPISettings.sports.nba, 
        region:str=OddsAPISettings.regions.us, 
        mkt:str=OddsAPISettings.markets.totals, 
        save:bool=False
    ) -> pd.DataFrame:
    """
    Converts the totals data from the API to a pandas DataFrame
    :param save: If true, saves the DataFrame to a csv file
    :return: A pandas DataFrame
    """
    res = requests.get(RETRIEVE_ODDS_ENDPOINT.format(sport=sport_key, api_key=ODDS_API_KEY, regions=region, markets=mkt))
    data = res.json()
    if res.ok:
        print(res.url)

    df_dict = {
        'id': [],
        'home_team': [],
        'away_team': [],
        'book': [],
        'over_under': [],
        'over_odds': [],
        'under_odds': []
    }

    for prop in data:
        for book in prop['bookmakers']:
            df_dict['id'].append(prop['id'])
            df_dict['home_team'].append(prop['home_team'])
            df_dict['away_team'].append(prop['away_team'])
            df_dict['book'].append(book['key'])
            df_dict['over_under'].append([x for x in book['markets'][0]['outcomes'] if x['name'] == 'Over'][0]['point'])
            df_dict['over_odds'].append([x for x in book['markets'][0]['outcomes'] if x['name'] == 'Over'][0]['price'])
            df_dict['under_odds'].append([x for x in book['markets'][0]['outcomes'] if x['name'] == 'Under'][0]['price'])
    
    df = pd.DataFrame(df_dict)

    if save:
        today = date.today().strftime('%Y_%m_%d')
        df.to_csv(export_folder + f'/totals_{today}.csv', index=False)

    return df