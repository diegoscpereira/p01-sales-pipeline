# 🏪 Sales Pipeline - Jornada de Dados - Python - P01

A daily sales ETL pipeline for a café/bakery, built in Python as a hands-on data engineering exercise. It reads raw daily CSV files, validates each record, quarantines bad data, aggregates sales by category, and writes the results to Parquet and CSV.

## Overview

The pipeline follows a classic Extract → Transform → Load flow, organized loosely around the medallion architecture (bronze → silver → gold):

1. **Extract (bronze)** — read all daily CSVs from the raw folder and union them into a single record set, tagging each row with its source date.
2. **Validate & Transform (silver)** — validate every record against a Pydantic model, quarantine the ones that fail, then group the valid records by category.
3. **Load (gold)** — calculate total sales per category and write the results to `.parquet` and `.csv`.

Bad rows never crash the run. They are isolated, logged, and appended to a quarantine file for later review, while the rest of the pipeline completes normally.

## Features

- **Pydantic validation** — each record is checked against a typed `Sales` model with field constraints (non-empty strings, non-negative quantities, positive prices). Invalid rows are caught individually.
- **Quarantine** — failed records are appended to a single timestamped quarantine CSV so no data is silently dropped.
- **Structured logging** — Loguru logs every stage to both the console and a rotating log file, including per-row validation failures with their reasons.
- **Decorator-based observability** — a `@log_stage` decorator wraps each stage to automatically log start, finish, duration, and any exceptions.
- **Type hints throughout** — every function is fully annotated.

## Project structure

```
sales_pipeline/
├── data/
│   └── raw/                  # daily input CSVs (sales_YYYY-MM-DD.csv)
├── output/
│   ├── totals.parquet        # aggregated category totals
│   ├── totals.csv            # same, human-readable
│   └── quarantine/
│       └── quarantine.csv    # rejected records, appended across runs
├── logs/
│   └── pipeline.log          # rotating log file
├── src/
│   ├── extract.py            # read + union daily files
│   ├── validate.py           # Pydantic model, validation, quarantine
│   ├── transform.py          # group by category, calculate totals
│   ├── load.py               # write Parquet + CSV
│   ├── decorators.py         # @log_stage
│   └── pipeline.py           # orchestration + logging config (entry point)
├── pyproject.toml
├── uv.lock
└── README.md
```

## Tech stack

- **Python 3.12**
- **uv** — dependency and environment management
- **pandas** + **pyarrow** — DataFrame handling and Parquet output
- **pydantic** — record validation
- **loguru** — logging
- **ruff** — linting and formatting
- **mypy** — static type checking

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for environment management.

```bash
# Clone the repo
git clone [<your-repo-url>](https://github.com/dscp1/jornada_de_dados_python_projeto01.git)
cd sales_pipeline

# Create the environment and install dependencies
uv sync
```

## Usage

Run the full pipeline from the project root:

```bash
uv run python src/pipeline.py
```

This reads every CSV in `data/raw/`, validates and transforms the records, and writes:

- `output/totals.parquet` and `output/totals.csv` — total sales per category
- `output/quarantine/quarantine.csv` — any records that failed validation

Logs are printed to the console and written to `logs/pipeline.log`.

## Input format

Each daily file is named `sales_YYYY-MM-DD.csv` with the following columns:

| Column | Type | Description |
|---|---|---|
| `Produto` | string | Product name |
| `Categoria` | string | Product category |
| `Quantidade` | integer | Units sold |
| `Venda` | float | Unit price |

## Validation rules

A record is considered valid only if it satisfies the `Sales` model:

- `Produto` — non-empty string
- `Categoria` — non-empty string
- `Quantidade` — integer, ≥ 0
- `Venda` — float, > 0
- `Date` — non-empty string (derived from the filename)

Records failing any rule are written to the quarantine file with a timestamp, and the reason is logged.

## Development

```bash
# Lint and auto-fix
uv run ruff check . --fix

# Format
uv run ruff format .

# Type check
uv run mypy src/
```

## Roadmap (v2)

- Detailed fact table output (all individual records with dates)
- Per-day, per-category summary using pandas `groupby`
- More robust filename date parsing
- Unit tests with pytest
