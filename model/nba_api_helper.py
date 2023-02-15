import numpy as np
from nba_api.stats.static import players
from difflib import SequenceMatcher

def find_player_id(player_name):

    """
    Finds the player id for a given player name
    :param player_name: The player name to find the id for
    :return: The player id
    """

    possible_matches = players.find_players_by_full_name(player_name)

    if len(possible_matches) == 1:
        return possible_matches[0]['id']
    else:
        idx_closest_match = np.argmax([SequenceMatcher(None, player_name, match['full_name']).ratio() for match in possible_matches])
        return possible_matches[idx_closest_match]['id']