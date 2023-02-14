from app.odds_api import convert_totals_to_df, convert_player_props_to_df, get_all_events

print(
    convert_player_props_to_df(save=True)
)