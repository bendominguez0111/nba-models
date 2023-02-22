from model.models.threes import ThreesModel

ThreesModel.run_model(
    player_name="Jordan Poole",
    opponent="LAL",
    bootstrap_samples=100_000,
    n_simulated_games=10_000,
    plot=True
)