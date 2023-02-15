"""

This module contains the endpoints & configuration for the Stats API

"""

class StatsAPISettings:
    host_header = "api-nba-v1.p.rapidapi.com"
    league_id = 12

class StatsAPIEndpoints:
    BASE_URL = "https://api-nba-v1.p.rapidapi.com"
    TEAMS_ENDPOINT = BASE_URL + "/teams"
    PLAYERS_ENDPOINT = BASE_URL + "/players"
    PLAYER_STATS_ENDPOINT = BASE_URL + "/players/statistics"