# Cooking Seasonally

A recipe recommendation prototype with a tested, SQL-first DuckDB analytical
layer. The analytical layer builds a local database from recipe JSON files and
is currently separate from the legacy Streamlit recommendations.

## Recommendation prototype

The original prototype collects recipes from Ottolenghi, extracts ingredients
and uses a custom spaCy named entity recognition model to identify main
ingredients. A local Streamlit application recommends recipes based on
user-provided ingredients using Jaccard similarity.

The analytical layer is a separate extension of that project and does not
currently feed the Streamlit recommendations.

## Analytical data model

The build creates five tables:

| Table | Grain |
|---|---|
| `staging_raw_recipes` | One row per recipe record in the source JSON files; repeated records are retained. |
| `recipes` | One row per unique recipe URL (`recipe_id`); conflicting names for the same URL are treated as a data-quality issue. |
| `categories` | One row per distinct source category. |
| `recipe_categories` | One row per unique recipe URL and category pair. |
| `recipe_ingredients` | One row per nonblank ingredient occurrence, identified by recipe URL and original position. |

The SQL transforms preserve recipe-category relationships and ingredient
occurrences while trimming whitespace and omitting blank ingredients.

## Setup and use

Prerequisites: Python 3.12.1 or later and [uv](https://docs.astral.sh/uv/).
From the repository root, install the locked dependencies:

```sh
uv sync --locked
```

Build `data/recipes.duckdb` using the included sample data:

```sh
uv run --locked python scripts/build_analytical_db.py
```

Run the analytical-model tests:

```sh
uv run --locked python -m pytest tests/test_analytical_models.py -v
```

## Data

`sample_data/` contains fictional recipe data for testing duplicate records,
multi-category relationships, repeated ingredients, and whitespace-only
ingredient entries. Its filenames follow the existing
`ottolenghi_recipes_*.json` convention for compatibility with the builder;
the sample does not contain scraped Ottolenghi recipes.

The original scraped JSON files are excluded from Git. To build locally from
those files, place them in `data/raw/` and run:

```sh
uv run --locked python scripts/build_analytical_db.py --data-dir data/raw
```

## Project structure

- `scripts/` — Python entry point for building the local database
- `sql/` — SQL staging and analytical-table definitions
- `sample_data/` — fictional JSON fixtures
- `tests/test_analytical_models.py` — analytical-model integrity and regression tests using the bundled sample data
- `cooking_seasonally/` — legacy scraper, NLP processing, and Streamlit application
- `docs/architecture/` — architecture decisions, including [ADR 001: local analytical data layer](docs/architecture/001-analytical-data-layer.md)

The existing scraper, NLP processing, and Streamlit application are legacy
components and have not been revalidated as part of the analytical-layer work.
