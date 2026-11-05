
import argparse
from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "recipes.duckdb"
SQL_DIR = PROJECT_ROOT / "sql"
SAMPLE_DATA_DIR = PROJECT_ROOT / "sample_data"

SQL_FILES = [
    "01_staging_raw_recipes.sql",
    "02_recipes.sql",
    "03_categories.sql",
    "04_recipe_categories.sql",
    "05_recipe_ingredients.sql",
]


def build_database(
    db_path: Path = DB_PATH,
    data_dir: Path = SAMPLE_DATA_DIR,
) -> None:
    """Build analytical tables from recipe JSON files."""

    db_path = Path(db_path)
    data_dir = Path(data_dir)

    source_pattern = str(
        data_dir / "ottolenghi_recipes_*.json"
    )

    db_path.parent.mkdir(parents=True, exist_ok=True)

    with duckdb.connect(str(db_path)) as con:
        for filename in SQL_FILES:
            sql = (SQL_DIR / filename).read_text(encoding="utf-8")

            if filename == "01_staging_raw_recipes.sql":
                con.execute(
                    sql,
                    {"source_pattern": source_pattern},
                )
            else:
                con.execute(sql)

            print(f"Executed: {filename}")

        recipe_count = con.execute(
            "SELECT COUNT(*) FROM recipes"
        ).fetchone()[0]  # ty: ignore[not-subscriptable]

        print(f"Recipes: {recipe_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=SAMPLE_DATA_DIR,
        help="Directory containing raw recipe JSON files",
    )

    args = parser.parse_args()
    build_database(data_dir=args.data_dir)
