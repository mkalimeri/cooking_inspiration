import sys
sys.path.append("./")

import json
from pathlib import Path
from typing import List

import spacy
from spacy.cli import download
import spacy.language 
from spacy.tokens import Doc

from cooking_seasonally.helpers.recipe import Recipe
from cooking_seasonally.helpers.utils import get_recipes, data_path

BASE_DIR = Path().resolve().parent.parent

def get_main_ingerdients_per_recipe(model: spacy.language.Doc, recipe: Recipe) -> str:
# Use the trained NER model to extract the main ingredients of a recipe
    return [model(ingredient).ents[0].text for ingredient in recipe.ingredients if len(model(ingredient).ents) > 0]

def get_main_ingredients(recipe_list: List[Recipe]) -> List[Recipe]:
# Process the list of ingredients of each recipe and create a new list of Recipes, which contain only the main ingredients
    # Download the NER model
    model = spacy.load(Path(BASE_DIR) / 'models/NER/model-best')

    return [Recipe(
        name=recipe.name, 
        url=recipe.url, 
        ingredients=get_main_ingerdients_per_recipe(model, recipe)
        ) for recipe in recipe_list]


if __name__ == '__main__':

    # Get the recipe list
    all_recipes = get_recipes()

    try:
        nlp = spacy.load('en_core_web_lg')
    except:
        download("en_core_web_lg")
        nlp = spacy.load('en_core_web_lg')
    finally:
        # Create the new list of recipes, containing only the main ingredients
        processed_recipes_list = get_main_ingredients(all_recipes)

    # Save list with recipes containing main ingredients in json format
    # processed_json_path = Path(BASE_DIR) / data_path("processed", "ottolenghi_processed_recipes_2.json")
    processed_json_path = Path(BASE_DIR) / data_path("processed", "ottolenghi_processed_recipes.json")

    with open(processed_json_path, 'w') as f:
        json.dump(processed_recipes_list, f, default=Recipe.encode_recipe)