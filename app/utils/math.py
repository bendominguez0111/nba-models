
def implied_probability(american_odds):
    """Calculate the implied probability of a bet.

    Args:
        american_odds (float): The American odds of the bet.

    Returns:
        float: The implied probability of the bet.
    """
    if american_odds > 0:
        return american_odds / (american_odds + 100)
    else:
        return 100 / (abs(american_odds) + 100)

