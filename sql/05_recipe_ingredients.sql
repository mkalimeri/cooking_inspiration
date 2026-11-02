
CREATE OR REPLACE TABLE recipe_ingredients AS

WITH unique_recipes AS (
    SELECT DISTINCT
        url,
        ingredients
    FROM staging_raw_recipes
),

expanded AS (
    SELECT
        url AS recipe_id,
        position AS ingredient_position,
        ingredient
    FROM unique_recipes,
         UNNEST(ingredients)
             WITH ORDINALITY AS t(ingredient, position)
)

SELECT
    recipe_id,
    ingredient_position,
    TRIM(ingredient, CHR(32) || CHR(9) || CHR(10) || CHR(13)) as ingredient_text
FROM expanded
    WHERE TRIM(ingredient, CHR(32) || CHR(9) || CHR(10) || CHR(13)) <> ''
;
