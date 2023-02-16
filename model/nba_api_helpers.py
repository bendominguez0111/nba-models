from nba_api.stats.static import players
from difflib import SequenceMatcher
from nba_api.stats.endpoints import playergamelog
import numpy as np

def find_player_id(player_name):

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

def get_player_game_log(player_id: str, season: str):
    
    if not type(player_id) == str:
        raise TypeError('player_id must be a string')

    game_log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
    game_log_df = game_log.get_data_frames()[0]

    return game_log_df