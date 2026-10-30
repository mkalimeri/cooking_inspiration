-- grain: one row per url/category_id

create or replace table recipe_categories as 
select distinct 
    url as recipe_id,
    category as category_id
from staging_raw_recipes