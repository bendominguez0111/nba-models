from config import KELLY_CRITERION_SETTING

def single_position_kelly(odds, probability):
    """Calculate the optimal bet size using the Kelly Criterion.

    Args:
        odds (float): The odds of the bet.
        probability (float): The probability of the bet.

    Returns:
        float: The optimal bet size.
    """
    return (odds * probability - (1 - probability)) / odds * KELLY_CRITERION_SETTING