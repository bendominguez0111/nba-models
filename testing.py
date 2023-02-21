from model.models.threes import ThreesModel

threes_model = ThreesModel()
threes_model.run_threes_model(
    player_name="Dillon Brooks",
    opponent="PHI",
    n_simulated_games=10_000
)