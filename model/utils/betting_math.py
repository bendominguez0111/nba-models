import pandas as pd

def calc_implied_probability(money_line) -> float:

    """Converts a money line to an implied probability.
    :param money_line: The money line to convert
    :param round_n: The number of decimal places to round to
    :return: The implied probability
    """

    if money_line < 0:
        return money_line / (money_line - 100)
    else:
        return 1 - (money_line / (money_line + 100))
    
def calc_suggested_kelly(row:pd.Series) -> float:

    """Calculate the suggested kelly bet size."""

    if row['edge'] > 0:
        b = (1 / row['implied_odds']) - 1
        if row['name'] == 'Over':
            return (b*row['p(over)'] - row['p(under)']) / b
        elif row['name'] == 'Under':
            return (b*row['p(under)'] - row['p(over)']) / b
    else:
        return 0
    
def calc_edge_for_over_under(row:pd.Series) -> float:

    """Calculate the edge for an over/under bet."""
    
    if row['name'] == 'Over':
        return row['p(over)'] - row['implied_odds']
    else:
        return row['p(under)'] - row['implied_odds']
    
def calc_expected_value(row:pd.Series) -> float:

    """Calculate the expected value of a bet."""

    if row['name'] == 'Over':
        return row['p(over)'] / row['implied_odds'] - 1
    elif row['name'] == 'Under':
        return row['p(under)'] / row['implied_odds'] - 1
    
    return