# Collection Logbook Automation

**Stack:** SQL (PostgreSQL) · Python · pandas

A light-weight tool that helps collection officers log customer interactions and automates their daily work queue.

## Folder Structure
```
collection_logbook/
├── sql/        # Schema, seed data, dashboard & report queries
├── python/     # Application logic (notes, dashboard, reports, export)
├── data/       # Sample CSVs for testing
└── outputs/    # Generated MIS exports
```

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env
psql -f sql/01_schema.sql
psql -f sql/02_seed_data.sql
python python/main.py
```
