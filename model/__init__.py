import os

import pandas as pd
import logging

from config import STR_TODAY
from model.nba_api_helpers import get_player_game_log
from model.odds_api import OddsAPI

class Model:

    def __init__(self, export_folder, odds_api_key, books:list=['bovada'], save:bool=True):
        self.export_folder = export_folder
        self.odds_api_client = OddsAPI(api_key=odds_api_key)
        self.books = books
        self.save = save
        self.odds_df = pd.DataFrame()
        self.game_logs_df = pd.DataFrame()

    def load_data(self):
        #caching
        logging.info('Loading odds data...')
        if not os.path.exists(self.export_folder + f'/player_props/{STR_TODAY}.csv'):
            self.odds_df = self.odds_api_client.convert_player_props_to_df()
        else:
            self.odds_df = pd.read_csv(self.export_folder + f'/player_props/{STR_TODAY}.csv')

        logging.info('Loading game logs...')
        for player_id in self.odds_df['nba_api_player_id'].unique():

            try:
                player_id = str(int(player_id))
            except ValueError:
                logging.debug(f'Player id {player_id} is not an integer; cannot download game logs')
                continue
            
            player_game_log = get_player_game_log(player_id, '2022')
            game_logs_df = pd.concat([self.game_logs_df, player_game_log])
            self.game_logs_df = game_logs_df

    def save_data(self):

        #prepare folders
        logging.info('Preparing export folders...')
        if not os.path.exists(self.export_folder):
            os.mkdir(self.export_folder)

        if not os.path.exists(self.export_folder + '/player_props'):
            os.mkdir(self.export_folder + '/player_props')

        if not os.path.exists(self.export_folder + '/game_logs'):
            os.mkdir(self.export_folder + '/game_logs')

        if not os.path.exists(self.export_folder + f'/game_logs/{STR_TODAY}'):
            os.mkdir(self.export_folder + f'/game_logs/{STR_TODAY}')

        logging.info('Saving odds data to export folders...')
        #save data we loaded
        self.odds_df.to_csv(self.export_folder + f'/player_props/{STR_TODAY}.csv', index=False)

        logging.info('Saving game logs to export folders...')
        for player_id in self.game_logs_df['Player_ID'].unique():
            self.game_logs_df[self.game_logs_df['Player_ID'] == player_id].to_csv(self.export_folder + f'/game_logs/{STR_TODAY}/{player_id}.csv', index=False)

    def compress_lines(self):
        return
    
    def run_model(self):

        self.load_data()

        if self.save:
            self.save_data()

        logging.info('Successfully loaded and saved data for {players} players and {props} props!'.format(players=len(self.game_logs_df['Player_ID'].unique()), props=len(self.odds_df)))