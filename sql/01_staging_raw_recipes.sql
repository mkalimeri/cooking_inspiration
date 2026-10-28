
CREATE OR REPLACE TABLE staging_raw_recipes AS
SELECT
    filename AS source_filename,
    regexp_extract(
        filename,
        'ottolenghi_recipes_([^/]+)[.]json$',
        1
    ) AS category,
    name,
    url,
    ingredients
FROM read_json_auto(
    'data/raw/ottolenghi_recipes_*.json',
    format = 'array',
    filename = true
);
