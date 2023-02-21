import logging
import sys

from config import DEBUG, EXPORT_FOLDER, ODDS_API_KEY
from model import Model

#logging settings
root = logging.getLogger()
root.setLevel(logging.DEBUG if DEBUG else logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

model = Model(export_folder=EXPORT_FOLDER, odds_api_key=ODDS_API_KEY)

model.run_model()