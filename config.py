import os

from dotenv import load_dotenv

load_dotenv()

#Authentication with Odds API
ODDS_API_KEY = os.getenv('ODDS_API_KEY')

# The Odds API endpoints
ODDS_API_BASE_URL = "https://api.the-odds-api.com"
## event odds
EVENT_ODDS_ENDPOINT = ODDS_API_BASE_URL + \
    "/v4/sports/{sport}/events/{event_id}/odds?apiKey={api_key}&regions={regions}&markets={markets}&dateFormat={date_format}&oddsFormat={odds_format}"

RETRIEVE_ODDS_ENDPOINT = ODDS_API_BASE_URL + \
    "/v4/sports/{sport}/odds/?apiKey={api_key}&regions={regions}&markets={markets}"

class OddsAPIMarkets:
    h2h = 'h2h'
    totals = 'totals'
    spreads = 'spreads'
    outrights = 'outrights'
    
    #nba-specific player-prop markets
    player_points = 'player_points'
    player_rebounds = 'player_rebounds'
    player_assists = 'player_assists'
    player_steals = 'player_steals'
    player_blocks = 'player_blocks'
    player_threes = 'player_threes'
    player_double_double = 'player_double_double'
    player_turnovers = 'player_turnovers'

    all_player_props = [
        player_points, 
        player_rebounds,
        player_assists,
        player_steals,
        player_blocks,
        player_threes,
        player_double_double,
        player_turnovers
    ]

class OddsAPIRegions:
    us = 'us'
    uk = 'uk'
    eu = 'eu'
    au = 'au'

class OddsAPISports:
    nba = 'basketball_nba'

class OddsAPISettings:
    markets = OddsAPIMarkets
    regions = OddsAPIRegions
    sports = OddsAPISports

# file stuff
base_dir = os.path.dirname(os.path.abspath(__file__))
export_folder = os.path.join(base_dir, 'exports')

# betting model settings
KELLY_CRITERION_SETTING = 0.5