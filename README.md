*POC version!*

**Recipe recommendation machine using SpaCy for Named Entity Recognition (NER)**

Implementation of a recipe recommendation machine: the user gets recipe recommendations from the website www.ottolenghi.com based on main ingredients entered (eg. beef, zucchini). 

1. Scrapped the web for recipes (I used Beautifulsoup and Selenium to scrappe recipes of www.ottolenghi.com)
Information saved: recipe name, link and ingredients. I might later enrich the recipe database with more recipes

2. Named Entity Recognition (NER) to only keep "main" ingredients.
My definition of main ingredients is fresh produce, meat and some staples, such as pasta/rice. Spices, herbs, oil, canned goods were not considered main ingredients.
To do this, I trained a NER (Named Entity Recognition) SpaCy pipeline. Data used for training included ingredients of recipes from www.epicurious.com (Kaggle dataset  and www.ottolenghi.com. The evaluation set only contained recipe ingredients from wwww.ottolenghi.com

3. Recommend recipes based on available ingredients, as provided by the user
I explored options to find the best recommendations, including SpaCy pretrained models using word vectors and Jaccard Similarity. I decided Jaccard similarity is more appropriate for my purpose, as I am interested in specific, and not similar, ingredients to the ones available to the user.

4. Developed a simple page for the recommendr using Streamlit (on localhost).

<img width="858" height="603" alt="Screenshot 2025-09-16 at 14 55 36" src="https://github.com/user-attachments/assets/c6a55e08-e792-4131-aa45-26104f0cb14e" />

**What is next?** 

1. Deploy the POC verion (ongoing)
2. UI needs polishing
3. Jaccard similarity only counts ***exact*** matches! So, eg. tomato and tomatoes do not count as the same items, which is not desirab;le in this case
   - Solutions: Stemming of words before matched, clustering of similar words
4. Take possible typos into account
5. Enrich recipe database
6. Add feature: Suggest weekly menu with provided staples
7. Currently, the recipes are saved in json files, consider using a database
