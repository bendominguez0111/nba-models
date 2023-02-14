from datetime import date

import pandas as pd

from config import export_folder
from config import odds_api_client as client


def convert_totals_to_df(sport_key:str='basketball_nba', region:str='us', mkt:str='totals', save:bool=False) -> pd.DataFrame:
    """
    Converts the totals data from the API to a pandas DataFrame
    :param save: If true, saves the DataFrame to a csv file
    :return: A pandas DataFrame
    """
    res = client.retrieve_odds(sport_key=sport_key, region='us', mkt='totals')
    data = res.json['data']

    df_dict = {
        'id': [],
        'home_team': [],
        'away_team': [],
        'site': [],
        'over_under': [],
        'odds': []
    }

    for prop in data:
        for site in prop['sites']:
            df_dict['id'].append(prop['id'])
            df_dict['home_team'].append(prop['home_team'])
            df_dict['away_team'].append(list(filter(lambda x: x != prop['home_team'], prop['teams']))[0])
            df_dict['site'].append(site['site_key'])
            df_dict['over_under'].append(site['odds']['totals']['points'][0])
            df_dict['odds'].append(site['odds']['totals']['points'][1])
    
    df = pd.DataFrame(df_dict)

    if save:
        today = date.today().strftime('%Y_%m_%d')
        df.to_csv(export_folder + f'/totals_{today}.csv', index=False)

    return df