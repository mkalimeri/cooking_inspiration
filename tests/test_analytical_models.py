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

def test_recipe_ingredient_composite_keys_are_unique(db):
    duplicate_count = db.execute("""
        SELECT COUNT(*)
        FROM (
            SELECT recipe_id, ingredient_position
            FROM recipe_ingredients
            GROUP BY recipe_id, ingredient_position
            HAVING COUNT(*) > 1
        )
    """).fetchone()[0]  # ty: ignore[not-subscriptable]

    assert duplicate_count == 0

def test_recipe_ingredient_no_blank_ingredients(db):
    invalid_count = db.execute("""
        SELECT COUNT(*)
        FROM recipe_ingredients
        WHERE ingredient_text IS NULL
        OR TRIM(
            ingredient_text,
            CHR(32) || CHR(9) || CHR(10) || CHR(13)
        ) = ''
    """).fetchone()[0]

    assert invalid_count == 0

def test_all_current_recipes_have_ingredients(db):
    missing_recipes = db.execute("""
        SELECT COUNT(*)
        FROM recipes as r
        LEFT JOIN recipe_ingredients as ri
        ON r.recipe_id = ri.recipe_id
        WHERE ri.recipe_id IS NULL
    """).fetchone()[0]

    assert missing_recipes == 0

def test_recipe_ingredients_reference_existing_recipes(db):
    missing_recipes = db.execute("""
        SELECT COUNT(*)
        FROM recipe_ingredients as ri
        LEFT JOIN recipes as r
        ON ri.recipe_id = r.recipe_id
        WHERE r.recipe_id IS NULL
    """).fetchone()[0]

    assert missing_recipes == 0


def test_all_source_ingredients_are_preserved(db):
    missing_count = db.execute("""
        WITH unique_recipes AS (
            SELECT DISTINCT
                url,
                ingredients
            FROM staging_raw_recipes
        ),
        expected_ingredients AS (
            SELECT
                url AS recipe_id,
                position AS ingredient_position,
                TRIM(
                    ingredient,
                    CHR(32) || CHR(9) || CHR(10) || CHR(13)
                ) AS ingredient_text
            FROM unique_recipes,
                 UNNEST(ingredients)
                     WITH ORDINALITY AS t(ingredient, position)
            WHERE TRIM(
                ingredient,
                CHR(32) || CHR(9) || CHR(10) || CHR(13)
            ) <> ''
        )
        SELECT COUNT(*)
        FROM (
            SELECT
                recipe_id,
                ingredient_position,
                ingredient_text
            FROM expected_ingredients

            EXCEPT

            SELECT
                recipe_id,
                ingredient_position,
                ingredient_text
            FROM recipe_ingredients
        )
    """).fetchone()[0]

    assert missing_count == 0

def test_no_outside_ingredients_added(db):
    missing_count = db.execute("""
        WITH unique_recipes AS (
            SELECT DISTINCT
                url,
                ingredients
            FROM staging_raw_recipes
        ),
        expected_ingredients AS (
            SELECT
                url AS recipe_id,
                position AS ingredient_position,
                TRIM(
                    ingredient,
                    CHR(32) || CHR(9) || CHR(10) || CHR(13)
                ) AS ingredient_text
            FROM unique_recipes,
                 UNNEST(ingredients)
                     WITH ORDINALITY AS t(ingredient, position)
            WHERE TRIM(
                ingredient,
                CHR(32) || CHR(9) || CHR(10) || CHR(13)
            ) <> ''
        )
        SELECT COUNT(*)
        FROM (
            SELECT
                recipe_id,
                ingredient_position,
                ingredient_text
            FROM recipe_ingredients

            EXCEPT

            SELECT
                recipe_id,
                ingredient_position,
                ingredient_text
            FROM expected_ingredients
        )
    """).fetchone()[0]

    assert missing_count == 0

def test_recipe_ingredients_with_duplicates_and_blanks():
    # 1. Create a fresh temporary database
    with duckdb.connect(":memory:") as con:

        # 2. Create staging and insert synthetic records
        con.execute("""
            CREATE TABLE staging_raw_recipes (
                url VARCHAR,
                ingredients VARCHAR[]
            )
        """)

        recipe = (
            "recipe-A",
            [" ", " olive oil ", "\n", "olive oil", "chickpeas"]
        )

        con.execute(
            "INSERT INTO staging_raw_recipes VALUES (?, ?)",
            recipe
        )
        con.execute(
            "INSERT INTO staging_raw_recipes VALUES (?, ?)",
            recipe
        )

        # 3. Execute the actual transformation SQL
        sql = Path("sql/05_recipe_ingredients.sql").read_text()
        con.execute(sql)

        # 4. Retrieve actual results
        actual = con.execute("""
            SELECT ingredient_position, ingredient_text
            FROM recipe_ingredients
            WHERE recipe_id = 'recipe-A'
            ORDER BY ingredient_position
        """).fetchall()

        # 5. Define expected results
        expected = [
            (2, "olive oil"),
            (4, "olive oil"),
            (5, "chickpeas"),
        ]

        assert actual == expected
