*POC version!*

**Recipe recommendation machine using SpaCy for Named Entity Recognition (NER)**

Implementation of a recipe recommendation machine

1. Scrapped the web for recipes (I used Beautifulsoup and Selenium to scrappe recipes of www.ottolenghi.com)
Information saved: recipe name, link and ingredients. I might later enrich the recipe database with more recipes

2. Named Entity Recognition (NER) to only keep "main" ingredients.
My definition of main ingredients is fresh produce, meat and some staples, such as pasta/rice. Spices, herbs, oil, canned goods were not considered main ingredients.
To do this, I trained a NER (Named Entity Recognition) SpaCy pipeline. Data used for training included ingredients of recipes from www.epicurious.com and www.ottolenghi.com. The evaluation set only contained recipe ingredients from wwww.ottolenghi.com

3. Recommend recipes based on available ingredients, as provided by the user
I explored options to find the best recommendations, including SpaCy pretrained models using word vectors and Jaccard Similarity. I decided Jaccard similarity is more appropriate for my purpose, as I am interested in specific, and not similar, ingredients to the ones available to the user.

4. Developed a simple page for the recommendr using Streamlit.

5. Deployed the app (still Proof Of Concept!)
   See

**What is next?** 

1. Jaccard similarity only counts ***exact*** matches! So, eg. tomato and tomatoes do not count as the same items, which is not desirab;le in this case
   - Solutions: Stemming of words before matched, clustering of similar words
2. Take possible typos into account
3. Enrich recipe database
4. UI needs polishing
5. Add feature: Suggest weekly menu with provided staples
6. Currently, the recipes are saved in json files, consider using a database
