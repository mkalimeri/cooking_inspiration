import sys
sys.path.append("./")

import json

from pathlib import Path, PosixPath
from typing import List

from .recipe import Recipe

# Base directory

def data_path(BASE_DIR: Path, folder: str, file_name: str)->Path:
    return Path(BASE_DIR) / f"data/{folder}/{file_name}"


def get_json_files(path: str) -> List[PosixPath]:
    # Get all links to json files in given directory
    return list(Path(path).glob("*.json"))


def get_recipes(jsn_link: Path) -> List[Recipe]:
    # Open json file containing recipes and return a list of Recipe instances
    with open(jsn_link, "rb") as f:
        recipes_list = json.load(f, object_hook=Recipe.decode_recipe)
    return recipes_list
