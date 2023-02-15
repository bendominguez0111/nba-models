from datetime import date

import pandas as pd
import requests

from config import export_folder
from model.odds_api.config import (EVENT_ODDS_ENDPOINT, RETRIEVE_ODDS_ENDPOINT,
                                   OddsAPISettings)

class OddsAPI:
    """
    This class is used to retrieve data from the Odds API
    :param api_key: The API key to use for the API
    """

    def __init__(self, api_key:str):
        self.api_key = api_key

    def get_all_events(
            self,
            sport_key:str=OddsAPISettings.sports.nba, 
            region:str=OddsAPISettings.regions.us, 
            mkt:str=OddsAPISettings.markets.h2h
        ) -> list:

        """ This function retrieves all future events from the API 
            :param sport_key: The sport key to retrieve events for
            :param region: The region to retrieve events for
            :param mkt: The market to retrieve events for
            :return: A list of event ids
        """
        
        res = requests.get(RETRIEVE_ODDS_ENDPOINT.format(sport=sport_key, api_key=self.api_key, regions=region, markets=mkt))
        data = res.json()
        print(data)
        return [event['id'] for event in data]

    def convert_player_props_to_df(
            self,
            sport_key:OddsAPISettings.sports=OddsAPISettings.sports.nba,
            region:OddsAPISettings.regions=OddsAPISettings.regions.us,
            markets:OddsAPISettings.markets=OddsAPISettings.markets.all_player_props,
            date_format:str='iso',
            odds_format:str='american',
            save:bool=False
        ) -> pd.DataFrame:

        """ This function converts the player props data from the API to a pandas DataFrame 
        
            :param sport_key: The sport key to retrieve events for
            :param region: The region to retrieve events for
            :param markets: The market to retrieve events for
            :param date_format: The date format to retrieve events for
            :param odds_format: The odds format to retrieve events for
            :param save: If true, saves the DataFrame to a csv file
            :return: A pandas DataFrame
        """

        events = self.get_all_events(sport_key=sport_key)

        df_dict = {
            'id': [],
            'prop_type': [],
            'player_name': [],
            'matchup_home_team': [],
            'matchup_away_team': [],
            'sports_book': [],  
            'name': [],
            'price': [],
            'points': []
        }

        for event in events:
            for market in markets:
                res = requests.get(
                    EVENT_ODDS_ENDPOINT.format(
                        sport=sport_key, 
                        event_id=event, 
                        regions=region,
                        markets=market,
                        date_format=date_format, 
                        odds_format=odds_format, 
                        api_key=self.api_key
                    )
                )

                data = res.json()

                for book in data['bookmakers']:
                    for prop in book['markets'][0]['outcomes']:
                        df_dict['id'].append(event)
                        df_dict['prop_type'].append(market)
                        df_dict['player_name'].append(prop['description'])
                        df_dict['matchup_home_team'].append(data['home_team'])
                        df_dict['matchup_away_team'].append(data['away_team'])
                        df_dict['sports_book'].append(book['key'])
                        df_dict['name'].append(prop['name'])
                        df_dict['price'].append(prop['price'])
                        df_dict['points'].append(prop.get('point'))
        
        df = pd.DataFrame(df_dict)

        if save:
            today = date.today().strftime('%Y_%m_%d')
            df.to_csv(export_folder + f'/player_props/{today}.csv', index=False)
        
        return df


    def convert_totals_to_df(
            self,
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

        res = requests.get(RETRIEVE_ODDS_ENDPOINT.format(sport=sport_key, api_key=self.api_key, regions=region, markets=mkt))
        data = res.json()

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