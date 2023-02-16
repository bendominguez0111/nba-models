from model import Model
from config import EXPORT_FOLDER, ODDS_API_KEY

model = Model(export_folder=EXPORT_FOLDER, odds_api_key=ODDS_API_KEY)

model.run_model()