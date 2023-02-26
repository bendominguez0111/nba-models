from model.models.threes import ThreesModel

ThreesModel.run_model(
    player_name="Jamal Murray",
    opponent="LAC",
    bootstrap_samples=100_000,
    n_simulated_games=10_000,
    plot=True
)