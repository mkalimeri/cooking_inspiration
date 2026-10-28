# ADR 001 — Introduce a local analytical data layer

**Status:** Proposed  
**Date:** 2026-10-28

## Context

The Recipe Recommender project scrapes Ottolenghi recipes, extracts ingredients using a spaCy NER model, and recommends recipes through a Streamlit application.

Currently, raw recipes are persisted as category-level JSON files. Processed recipes contain only the ingredients identified by NER as relevant to recommendations.

This architecture supports the original application but limits the reuse of the full recipe dataset for other analytical purposes.

## Findings from the repository audit

An inspection of four raw JSON files identified:

| Metric | Result |
|---|---:|
| Total raw records | 3,144 |
| Distinct recipe URLs | 366 |
| Distinct recipe-category relationships | 470 |
| Redundant records within categories | 2,674 |
| URLs with conflicting names | 0 |
| URLs with conflicting ingredient lists | 0 |

The scraper appears to collect repeated recipe cards when paginating, and it skips an entire category if the output file already exists. This prevents refreshes and may miss newly published recipes.

Category information is encoded in filenames rather than in individual recipe records.

## Decision

Introduce a local analytical layer using DuckDB, with a SQL-first implementation.

Python will handle file discovery, database connection and execution. SQL will handle deduplication and analytical modeling.

The initial model will contain:

- `recipes`: One row per unique recipe URL.
- `categories`: One row per source category.
- `recipe_categories`: One row per unique recipe-category association.
- `recipe_ingredients`: One row per original ingredient occurrence, preserving ingredient text and position.

The existing raw JSON files remain the source inputs. NER processing and the Streamlit application's data contract will remain unchanged during the first milestone.

## Rationale

- Preserve complete recipe information independently of recommendation-specific processing.
- Support SQL-based analysis of recipes, ingredients and categories.
- Avoid duplication through explicit table grains and relationships.
- Provide a foundation for future storage and application integration.
- Keep the initial implementation small and locally reproducible.

## Alternatives considered

- Python-first transformations: viable, but SQL-first better supports the project's Analytics Engineering learning objectives.
- AWS S3 + DuckDB: a potential second phase once the local model is established.
- Managed analytical database: deferred because its additional infrastructure is not currently justified.

## First implementation milestone

Build a reproducible local DuckDB database from the existing JSON files.

Acceptance criteria:

- 366 distinct recipes.
- 470 distinct recipe-category relationships.
- No duplicate URLs in `recipes`.
- No orphaned recipe-category or recipe-ingredient relationships.
- Original ingredient text and ordering preserved.
- At least one useful analytical SQL query.
- Automated tests for important data-quality invariants.

## Deferred decisions

- Ingredient normalization and the definition of staples.
- NER integration with the analytical layer.
- Streamlit integration.
- Improved pagination, refresh logic and scraping reliability.
- AWS S3 storage and possible Parquet datasets.

## Validation

The counts and consistency findings reflect the current dataset. They must be revalidated if the source files change.