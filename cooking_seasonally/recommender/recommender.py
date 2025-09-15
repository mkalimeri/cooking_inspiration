import sys
from typing import List
sys.path.append("./")

from pathlib import Path
import numpy as np
import pandas as pd

import spacy
import streamlit as st

from cooking_seasonally.helpers.utils import BASE_DIR, data_path, Recipe

def jaccard_similarity(list_1: List, list_2: List) -> float:
    '''
    Returns the Jaccard similarity of two lists
    '''
    return len(set(list_1).intersection(set(list_2))) / len(set(list_1).union(set(list_2)))

def vector_similarity(str_1: str, str_2: str) -> float:
    """
    Returns the vector similarity betweet two strings
    """
    nlp = spacy.load("en_core_web_lg")
    return nlp(str_1).similarity(nlp(str_2))

def return_relevant_recipes(recipes_df: pd.DataFrame, available_ingredients: List) -> pd.DataFrame:
    recipes_df["jaccard_similarities"] = recipes_df.ingredients.map(lambda x: jaccard_similarity(x, available_ingredients))
    recipes_df = recipes_df.sort_values('jaccard_similarities', ascending=False)

    return(recipes_df)

def return_random_recipe(recipes_df: pd.DataFrame):
    recipe = recipes_df.iloc[np.random.choice(recipes_df.shape[0])]
    url = recipe['url']
    st.write(f"How about [{recipe['name']}](%s)" % url)

