import logging

import numpy as np
import pandas as pd
import requests
from nba_api.stats.static import teams
from tqdm import tqdm

from model.nba_api_helpers import get_player_id, get_player_team_id
from model.odds_api.config import OddsAPIEndpoints, OddsAPISettings


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
        
        res = requests.get(OddsAPIEndpoints.RETRIEVE_ODDS_ENDPOINT.format(sport=sport_key, api_key=self.api_key, regions=region, markets=mkt))
        data = res.json()
      
        return [event['id'] for event in data]

    def convert_player_props_to_df(
            self,
            sport_key:OddsAPISettings.sports=OddsAPISettings.sports.nba,
            region:OddsAPISettings.regions=OddsAPISettings.regions.us,
            markets:OddsAPISettings.markets=OddsAPISettings.markets.all_player_props,
            date_format:str='iso',
            odds_format:str='american'
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
            'player_team': [],
            'defensive_matchup': [],
            'sports_book': [],  
            'name': [],
            'price': [],
            'points': [],
            'nba_api_player_id': []
        }

        for event in tqdm(events, desc=f'Grabbing player props from {len(events)} NBA games today...'):
            for market in markets:
                res = requests.get(
                    OddsAPIEndpoints.EVENT_ODDS_ENDPOINT.format(
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
                        
                        df_dict['sports_book'].append(book['key'])
                        df_dict['name'].append(prop['name'])
                        df_dict['price'].append(prop['price'])
                        df_dict['points'].append(prop.get('point'))
                        
                        home_team = data['home_team']
                        away_team = data['away_team']
                        home_team = teams.find_teams_by_full_name(home_team)[0]['abbreviation']
                        away_team = teams.find_teams_by_full_name(away_team)[0]['abbreviation']

                        #nba api stuff
                        nba_api_player_id = get_player_id(prop['description'])
                        df_dict['nba_api_player_id'].append(nba_api_player_id)
                    
                        try:
                            player_team_id = get_player_team_id(nba_api_player_id, timeout=30, res_wait=1)
                        except Exception as e:
                            logging.error(f'Error getting player team id for {prop["description"]}: {e}')
                            df_dict['player_team'].append(np.nan)
                            df_dict['defensive_matchup'].append(np.nan)
                            continue
                        player_team = teams.find_team_name_by_id(player_team_id)['abbreviation']
                        df_dict['player_team'].append(player_team)

                        if player_team == home_team:
                            df_dict['defensive_matchup'].append(away_team)
                        elif player_team == away_team:
                            df_dict['defensive_matchup'].append(home_team)
                        else:
                            df_dict['defensive_matchup'].append(np.nan)
        
        df = pd.DataFrame(df_dict)
        
        return df


    def convert_totals_to_df(
            self,
            sport_key:str=OddsAPISettings.sports.nba, 
            region:str=OddsAPISettings.regions.us, 
            mkt:str=OddsAPISettings.markets.totals
        ) -> pd.DataFrame:

        """
        Converts the totals data from the API to a pandas DataFrame
        :param save: If true, saves the DataFrame to a csv file
        :return: A pandas DataFrame
        """

        res = requests.get(OddsAPIEndpoints.RETRIEVE_ODDS_ENDPOINT\
            .format(sport=sport_key, api_key=self.api_key, regions=region, markets=mkt
        ))
        
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

        return df