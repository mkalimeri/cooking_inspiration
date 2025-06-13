import sys
sys.path.append("./")

from pathlib import Path

from spacy.cli.init_config import fill_config
from spacy.cli.train import train

from cooking_seasonally.helpers.utils import BASE_DIR


if __name__ == "__main__":
    model_path = Path(BASE_DIR) / 'models/NER'
    data_path = Path(BASE_DIR) / 'data/processed/NER'

    # fill_config(model_path / 'config.cfg', model_path / 'base_config.cfg') # batch = 64
    train(config_path=model_path / 'config.cfg', output_path=model_path, overrides={'paths.train': str(data_path)+'/train.spacy', 'paths.dev': str(data_path)+'/eval.spacy'})

