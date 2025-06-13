*Ongoing project!*

**Recipe recommendation machine using SpaCy**

Implementation of a recipe recommendation machine, I will take the following steps

1. Scrap the web for recipes (I used Beautifulsoup and Selenium to scrappe recipes of www.ottolenghi.com)
Information saved: recipe name, link and ingredients. I might later add this information from a Kaggle dataset that contains recipes from other websites (I used a subset to train the model in the next step)

2. Perform NLP to only keep "main" ingredients.
My definition of main ingredients is fresh produce, meat and some staples, such as pasta/rice, canned food (eg. olives, anchovies etc). Spices and oil were not considered main ingredients.
To do this, I trained a NER (Named Entity Recognition) SpaCy pipeline.

3. (Ongoing) Recommend recipes based on available ingredients, as provided by the user
I am exploring options to find the best recommendations, including SpaCy pretrained models using word vectors
