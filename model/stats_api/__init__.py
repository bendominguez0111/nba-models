import requests
import pandas as pd

from model.stats_api.config import StatsAPIEndpoints, StatsAPISettings


class StatsAPI:

    """
    This class is responsible for making requests to the API-NBA API
    https://rapidapi.com/api-sports/api/api-nba
    """

    def __init__(self, api_key, season='2022'):

        self.request_headers = {
            'X-RapidAPI-Host': StatsAPISettings.host_header,
            'X-RapidAPI-Key': api_key
        }

        self.season = season

    def get_teams(self) -> list:
        """
        Returns a list of all the teams in the NBA
        :return: A list of all the teams in the NBA
        """
        res = requests.get(StatsAPIEndpoints.TEAMS_ENDPOINT, headers=self.request_headers)
        teams = res.json()['response']

        return teams

    def search_team_id(self, search_query) -> int:

        """
        Returns the ID of the team
        :param search_query: The name of the team
        :return: The ID of the team
        """

        params = {'search': search_query}
        res = requests.get(StatsAPIEndpoints.TEAMS_ENDPOINT, headers=self.request_headers, params=params)
        res = res.json()['response']
        team_id = res[0]['id']

        return team_id

    def get_player(self, player_name:str="Tyler Herro", team_name:str="Miami Heat"):
        
        """
        Returns the player's information
        :param player_name: The name of the player
        :param team_name: The name of the team the player plays for
        :return: The player's information
        """

        if len(player_name.split()) > 1:
            search_query_player_name = player_name.split()[-1]
            print(search_query_player_name)

        params = {
            'team': self.search_team_id(team_name),
            'season': self.season,
            'search': search_query_player_name
        }

        res = requests.get(StatsAPIEndpoints.PLAYERS_ENDPOINT, headers=self.request_headers, params=params)
        player = res.json()['response'][0]
        
        return player

    def get_player_stats(self, player_name:str="Tyler Herro", team_name:str="Miami Heat") -> pd.DataFrame:

        """
        Returns a DataFrame of the player's stats for the season
        :param player_name: The name of the player
        :param team_name: The name of the team the player plays for
        :return: A DataFrame of the player's stats for the season
        """

        player_id = self.get_player(player_name, team_name)['id']

        params = {
            'id': player_id,
            'season': self.season
        }

        res = requests.get(StatsAPIEndpoints.PLAYER_STATS_ENDPOINT, params=params, headers=self.request_headers)
        games = res.json()['response']

        player_data = {
            'game_id': [],
            'player_id': [],
            'player_name': [],
            'points': [],
            'fgm': [],
            'fga': [],
            'ftm': [],
            'fta': [],
            'fgp': [],
            'ftp': [],
            'tpm': [],
            'tpa': [],
            'tpp': [],
            'offReb': [],
            'defReb': [],
            'totReb': [],
            'assists': [],
            'pFouls': [],
            'steals': [],
            'turnovers': [],
            'blocks': [],
            'plusMinus': []
        }

        for game in games:
            player_data['game_id'].append(game['game']['id'])
            player_data['player_id'].append(player_id)
            player_data['player_name'].append(player_name)
            player_data['points'].append(game['points'])
            player_data['fgm'].append(game['fgm'])
            player_data['fga'].append(game['fga'])
            player_data['ftm'].append(game['ftm'])
            player_data['fta'].append(game['fta'])
            player_data['fgp'].append(game['fgp'])
            player_data['ftp'].append(game['ftp'])
            player_data['tpm'].append(game['tpm'])
            player_data['tpa'].append(game['tpa'])
            player_data['tpp'].append(game['tpp'])
            player_data['offReb'].append(game['offReb'])
            player_data['defReb'].append(game['defReb'])
            player_data['totReb'].append(game['totReb'])
            player_data['assists'].append(game['assists'])
            player_data['pFouls'].append(game['pFouls'])
            player_data['steals'].append(game['steals'])
            player_data['turnovers'].append(game['turnovers'])
            player_data['blocks'].append(game['blocks'])
            player_data['plusMinus'].append(game['plusMinus'])

        return pd.DataFrame(player_data)


