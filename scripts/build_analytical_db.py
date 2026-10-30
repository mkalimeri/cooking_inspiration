from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "recipes.duckdb"
SQL_DIR = PROJECT_ROOT / "sql"

SQL_FILES = [
    "01_staging_raw_recipes.sql",
    "02_recipes.sql",
    "03_categories.sql",
    "04_recipe_categories.sql",
]


def build_database(db_path: Path = DB_PATH) -> None:
    """Create the analytical tables by executing SQL files in order."""
    with duckdb.connect(str(db_path)) as con:
        for filename in SQL_FILES:
            sql = (SQL_DIR / filename).read_text(encoding="utf-8")
            con.execute(sql)
            print(f"Executed: {filename}")

        recipe_count = con.execute(
            "SELECT COUNT(*) FROM recipes"
        ).fetchone()[0]  # ty: ignore[not-subscriptable]

        print(f"Recipes: {recipe_count}")


if __name__ == "__main__":
    build_database()