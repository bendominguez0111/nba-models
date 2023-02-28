import logging
from difflib import SequenceMatcher
import time

import numpy as np
import pandas as pd
from nba_api.stats.endpoints import (commonplayerinfo, leaguegamefinder,
                                     playergamelog, shotchartdetail)
from nba_api.stats.static import players, teams
from sklearn.ensemble import RandomForestClassifier

def get_player_id(player_name) -> str or np.nan:

    """
    Finds the player id for a given player name
    :param player_name: The player name to find the id for
    :return: The player id
    """

    possible_matches = players.find_players_by_full_name(player_name)

    if len(possible_matches) == 1:
        return str(possible_matches[0]['id'])
    elif len(possible_matches) > 1:
        idx_closest_match = np.argmax([SequenceMatcher(None, player_name, match['full_name']).ratio() for match in possible_matches])
        return str(possible_matches[idx_closest_match]['id'])
    else:
        return np.nan
    
def get_player_team_id(player_id:str, res_wait: int = 0, timeout: int = 30) -> str:

    """
    Gets the team id for a given player id
    :param player_id: The player id to get the team id for
    :return: The team id
    """
    if res_wait > 0:
        time.sleep(res_wait)
    if not type(player_id) == str:
        raise TypeError('player_id must be a string')

    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id, timeout=timeout)
    team_id = player_info.get_data_frames()[0]['TEAM_ID'][0]

    return team_id

def get_player_game_log(player_id: str, season: str) -> pd.DataFrame:
    
    if not type(player_id) == str:
        raise TypeError('player_id must be a string')

    game_log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
    game_log_df = game_log.get_data_frames()[0]

    return game_log_df

def get_player_shot_loc_data(player_name: str, team_id: str = None, context_measure_simple: str = 'FGA') -> pd.DataFrame:

    """
    Gets the shot location data for a given player
    :param player_name: The name of the player to get the shot data for
    :param season: The season to get the shot data for
    :param team_id: The team id to get the shot data for
    :param context_measure_simple: Types of shots to get (eg. FGA, FG3A, etc.)
    :return: A pandas dataframe containing the shot data
    """
    player_id = players.find_players_by_full_name(player_name)[0]['id']
    team_id = get_player_team_id(str(player_id))
    shot_chart = shotchartdetail.ShotChartDetail(player_id=player_id, team_id=team_id, context_measure_simple=context_measure_simple)
    df = pd.concat(shot_chart.get_data_frames())

    return df

def get_league_shot_loc_data(context_measure_simple: str = 'FGA') -> pd.DataFrame:
    """
    Get league shot data
    :param season: The season to get the shot data for
    :param context_measure_simple: Types of shots to get (eg. FGA, FG3A, etc.)
    :return: A pandas dataframe containing the shot data
    """

    def find_team_abrv(team_name):
        try:
            abrv = teams.find_teams_by_full_name(team_name.strip())[0]['abbreviation']
            return abrv
        except IndexError:
            return np.nan
        
    def find_matchup(row):
        game_df = games_df[games_df['GAME_ID'] == str(row['GAME_ID'])]
        matchup = game_df['MATCHUP'].values[0]
        return matchup
    
    def find_defense(row):
        team_abrv = row['TEAM_ABRV']
        team_a = row['MATCHUP'].split()[0]
        team_b = row['MATCHUP'].split()[-1]
        if team_abrv != team_a:
            return team_a
        if team_abrv != team_b:
            return team_b
        
    games_df = pd.concat(leaguegamefinder.LeagueGameFinder().get_data_frames())
    
    league_shots = shotchartdetail.ShotChartDetail(
        player_id=0,
        team_id=0,
        season_type_all_star='Regular Season',
        context_measure_simple = context_measure_simple
    )

    league_df = pd.concat(league_shots.get_data_frames())
    league_df = league_df.loc[(league_df['GRID_TYPE'] == 'Shot Chart Detail'), ['GAME_ID', 'TEAM_NAME', 'TEAM_ID', 'LOC_X', 'LOC_Y', 'SHOT_MADE_FLAG']]
    league_df['TEAM_ABRV'] = league_df['TEAM_NAME'].apply(find_team_abrv)

    matchups_table = league_df[['TEAM_ID', 'GAME_ID']].groupby('GAME_ID').size().reset_index().drop(0, axis=1)
    matchups_table['MATCHUP'] = matchups_table.apply(find_matchup, axis=1)

    league_df = league_df.merge(matchups_table, on='GAME_ID')

    league_df['DEF'] = league_df.apply(find_defense, axis=1)

    return league_df[['DEF', 'GAME_ID', 'LOC_X', 'LOC_Y', 'SHOT_MADE_FLAG']]

def generate_3_point_classifier():

    league_shots = shotchartdetail.ShotChartDetail(
        player_id=0,
        team_id=0,
        season_type_all_star='Regular Season',
        context_measure_simple = 'FGA'
    )

    league_shots_df = league_shots.get_data_frames()[0]
    league_shots_df['three'] = league_shots_df['SHOT_ZONE_BASIC'].isin(['Left Corner 3', 'Above the Break 3', 'Right Corner 3','Backcourt']).astype(int)
    X, y = league_shots_df[['LOC_X', 'LOC_Y']].values, league_shots_df['three'].values
    clf = RandomForestClassifier()
    clf.fit(X, y)
    return clf