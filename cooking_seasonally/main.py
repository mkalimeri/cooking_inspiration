from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

from helpers.utils import data_path
from recommender.recommender import return_relevant_recipes, return_random_recipe

BASE_DIR = Path().resolve()

st.title("What are you cooking today?")

processed_json_path = data_path(BASE_DIR, "processed", "ottolenghi_processed_recipes.json")
recipes_df = pd.read_json(processed_json_path)

surprise = st.button('Surprise me!')
if surprise:
    return_random_recipe(recipes_df)

available_ingredients = st.text_input('What ingredients would you like to use? \n')
available_ingredients = available_ingredients.split(', ')

recipes_df = return_relevant_recipes(recipes_df, available_ingredients)
recipes_df = recipes_df.reset_index(drop=True)

url = recipes_df.iloc[0]['url']
st.write(f"How about [{recipes_df.iloc[0]['name']}](%s)" % url)
st.write(recipes_df.iloc[0])

st.write(f"Other options are")
for r in np.arange(1,6):
    url = recipes_df.iloc[r]['url']
    st.write(f"[{recipes_df.iloc[r]['name']}](%s)" % url)

