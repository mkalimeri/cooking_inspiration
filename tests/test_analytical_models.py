from pathlib import Path

import duckdb
import pytest

from scripts.build_analytical_db import build_database


@pytest.fixture(scope="module")
def db(tmp_path_factory):
    """Build a fresh analytical database for this test module."""
    temp_dir = tmp_path_factory.mktemp("analytical_db")
    db_path = temp_dir / "test_recipes.duckdb"

    build_database(db_path)

    with duckdb.connect(str(db_path), read_only=True) as con:
        yield con

def test_recipe_ids_are_unique(db):
    duplicate_count = db.execute("""
        SELECT COUNT(*)
        FROM (
            SELECT recipe_id
            FROM recipes
            GROUP BY recipe_id
            HAVING COUNT(*) > 1
        )
    """).fetchone()[0]  # ty: ignore[not-subscriptable]

    assert duplicate_count == 0

def test_recipe_id_not_null(db):
    null_count = db.execute("""
        select 
            count(*)
        from recipes
        where recipe_id is null
    """).fetchone()[0]  # ty: ignore[not-subscriptable]

    assert null_count == 0

def test_all_source_recipes_are_preserved(db):
    missing_count = db.execute("""
        SELECT COUNT(*)
        FROM (
            SELECT DISTINCT url
            FROM staging_raw_recipes

            EXCEPT

            SELECT recipe_id
            FROM recipes
        )
    """).fetchone()[0]

    assert missing_count == 0

def test_recipe_category_pairs_are_unique(db):
    result = db.execute("""
        SELECT
            COUNT(*) AS total_rows,
            COUNT(DISTINCT (recipe_id, category_id)) AS distinct_pairs
        FROM recipe_categories
    """).fetchone()

    assert result is not None
    total_rows, distinct_pairs = result

    assert total_rows == distinct_pairs
    assert total_rows == 470

def test_recipe_categories_reference_existing_recipes(db):
    result = db.execute("""
        select 
            count(*)
        from recipe_categories as rc
        left join recipes as r
            on rc.recipe_id = r.recipe_id
        where r.recipe_id is null
    """).fetchone()[0]

    assert result == 0

def test_recipe_categories_reference_existing_categories(db):
    result = db.execute("""
        select 
            count(*)
        from recipe_categories as rc
        left join categories as c
            on rc.category_id = c.category_id
        where c.category_id is null
    """).fetchone()[0]

    assert result == 0

def test_all_relationships_exist_in_bridge(db):
    result = db.execute("""
        select count(*) from (
            select 
                url as recipe_id,
                category as category_id
            from staging_raw_recipes

            except

            select
                recipe_id,
                category_id
            from recipe_categories
        )
    """).fetchone()[0]

    assert result == 0