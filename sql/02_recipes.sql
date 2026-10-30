CREATE OR REPLACE TABLE recipes AS
SELECT
    url AS recipe_id,
    name,
    url
FROM staging_raw_recipes
GROUP BY url, name;