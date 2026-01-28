# Module 1 - Homework: Docker & Data Ingestion

This project demonstrates containerized data ingestion into PostgreSQL using Docker and Docker Compose.

## Project Overview

The project uses Docker containers to:

1. Run a PostgreSQL database
2. Manage the database with pgAdmin
3. Ingest NYC taxi data into PostgreSQL
4. Provide a Jupyter notebook environment for data analysis

## Main Files & Directories

### `docker-compose.yaml`

Defines and orchestrates all Docker services for the project:

- **pgdatabase**: PostgreSQL 17 database service with ny_taxi database
- **pgadmin**: Web UI for database management (port 8080)
- **data_ingest**: Custom service that runs the data ingestion script
- **jupyter**: JupyterLab environment for data exploration (port 8888)

All services are configured to depend on PostgreSQL being healthy before starting.

### `Dockerfile`

Builds the custom `data-ingest:v0.1` Docker image:

- Uses Python 3.13-slim as base image
- Installs required build dependencies (build-essential, libpq-dev) for psycopg2
- Uses UV package manager for fast, deterministic package installation
- Sets up working directory and copies project files

### `ingest_data.py`

Python script that ingests data into PostgreSQL:

- Downloads taxi zone lookup data from GitHub
- Connects to PostgreSQL using SQLAlchemy
- Loads CSV data into the database in chunks
- Accepts command-line parameters for database credentials and table names
- Used by the `data_ingest` service in docker-compose

### `pyproject.toml`

Project configuration file defining:

- Project metadata (name: module-1-homework, version: 0.1.0)
- Python version requirement (>=3.12)
- Dependencies:
  - `click`: Command-line interface creation
  - `pandas`: Data manipulation and CSV reading
  - `psycopg2`: PostgreSQL database adapter
  - `pyarrow`: Apache Arrow for efficient data operations
  - `sqlalchemy`: SQL toolkit and ORM for database operations

### `taxi_zone_lookup.csv`

Static CSV file containing taxi zone reference data (used as local fallback).

## Getting Started

### Prerequisites

- Docker and Docker Compose installed

### Run the Project

1. Build the Docker image:

```bash
docker build -t data-ingest:v0.1 .
```

2. Start all services:

```bash
docker compose up
```

3. Access services:
   - **PostgreSQL**: localhost:5433 (user: root, password: root)
   - **pgAdmin**: http://localhost:8080 (email: pgadmin@pgadmin.com, password: pgadmin)
   - **JupyterLab**: http://localhost:8888

4. Stop services:

```bash
docker compose down
```

## Data Ingestion Details

The `data_ingest` service automatically:

1. Waits for PostgreSQL to be healthy
2. Downloads taxi zone lookup data
3. Loads data into tables:
   - `yellow_taxi_trips`: Main taxi trip data
   - `taxi_zones`: Zone reference data
4. Uses chunked reading (100,000 rows/chunk) for memory efficiency

## Dependencies

Key Python packages used:

- **SQLAlchemy**: Database ORM and connection management
- **psycopg2**: PostgreSQL adapter for Python
- **pandas**: Data loading and transformation
- **Click**: CLI argument parsing
