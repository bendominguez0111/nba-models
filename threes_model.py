from model.models.threes import run_threes_model
import numpy as np

fmgs = run_threes_model(
    player_name = "Jayson Tatum",
    opponent = "IND",
    n_simulated_games = 100_000
)

fmgs = np.array(fmgs)

print(
    'Probability of Jayson Tatum making over 4.5 threes against the Pacers: ',
    str(round(sum(fmgs > 4.5) / len(fmgs) * 100, 4)) + "%"
)

print(
    'Probability of Jayson Tatum making over 3.5 threes against the Pacers: ',
    str(round(sum(fmgs > 3.5) / len(fmgs) *100, 4)) + "%"
)

print(
    'Probability of Jayson Tatum making over 2.5 threes against the Pacers: ',
    str(round(sum(fmgs > 2.5) / len(fmgs) * 100, 4)) + "%"
)

print(
    'Probability of Jayson Tatum making over 1.5 threes against the Pacers: ',
    str(round(sum(fmgs > 1.5) / len(fmgs) * 100, 2)) + "%"
)