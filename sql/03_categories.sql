-- grain: one row per category

create or replace table categories as
select distinct
    category as category_id
from staging_raw_recipes