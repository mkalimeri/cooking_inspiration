import json

from pathlib import Path, PosixPath
from typing import List

from cooking_seasonally.helpers.recipe import Recipe

# Base directory
BASE_DIR = Path().resolve()

def get_recipes():
    jsn_dir_path = Path(BASE_DIR) / "data/interim/"
    recipe_files = get_json_files(jsn_dir_path)
    all_recipes_list = get_recipes_from_json(recipe_files[0])
    return all_recipes_list

def get_json_files(path: str) -> List[PosixPath]:
    # Get all links to json files in given directory
    return list(Path(path).glob("*.json"))


def get_recipes_from_json(jsn_link: str) -> List[Recipe]:
    # Open json file containing recipes and return a list of Recipe instances
    with open(jsn_link, "rb") as f:
        recipes_list = json.load(f, object_hook=Recipe.decode_recipe)
    return recipes_list
