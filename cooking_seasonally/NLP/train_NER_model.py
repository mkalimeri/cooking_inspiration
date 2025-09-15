import sys
sys.path.append("./")

from pathlib import Path

import spacy
from spacy.cli.init_config import fill_config
from spacy.cli.train import train


if __name__ == "__main__":
    BASE_DIR = Path().resolve()

    model_path = Path(BASE_DIR) / 'models/NER'
    data_path = Path(BASE_DIR) / 'data/processed/NER'

    print(BASE_DIR)

    # fill_config(model_path / 'config_word2vec.cfg', model_path / 'base_config_word2vec.cfg') 
    train(config_path=model_path / 'config_word2vec.cfg', output_path=model_path, overrides={'paths.train': str(data_path)+'/train_large_ottolenghi.spacy', 'paths.dev': str(data_path)+'/eval.spacy'})

