# Module 1 - Homework: Docker & Data Ingestion

This project demonstrates containerized data ingestion into PostgreSQL using Docker and Docker Compose.

## Table of Contents

- [Solution](#solution)
  - [Getting Started](#getting-started)
  - [SQL Queries](#sql-queries)
- [Project Description](#project-description)
  - [Project Overview](#project-overview)
  - [Main Files & Directories](#main-files--directories)
  - [Data Ingestion Details](#data-ingestion-details)
  - [Dependencies](#dependencies)

## Solution

### Getting Started

#### Prerequisites

- Docker and Docker Compose installed

#### Run the Project

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

### SQL Queries

The following SQL queries were executed against the ingested data to analyze NYC taxi trips:

#### Question 1 - Pip Version

Command: `docker run -it --entrypoint=bash python:3.13` then `pip -V`
**Answer:** 25.3

#### Question 2 - pgAdmin Connection

Given the docker-compose.yaml, what hostname and port should pgAdmin use to connect to postgres?
**Answer:** `postgres:5432` (container name) or `db:5432` (service name) - both are correct

#### Question 3 - Trips ≤ 1 Mile in November 2025

Count trips in November 2025 with trip_distance ≤ 1 mile:

```sql
SELECT COUNT(*) AS count_trips FROM public.yellow_taxi_trips
WHERE lpep_pickup_datetime between '2025-11-01' and '2025-12-01'
AND trip_distance <= 1
```

**Answer:** 8007

#### Question 4 - Pickup Day with Longest Trip Distance

Find the pickup day with the longest trip distance (excluding trips > 100 miles):

```sql
SELECT DATE(lpep_pickup_datetime) AS Day FROM public.yellow_taxi_trips
WHERE trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1
```

**Answer:** 2025-11-14

#### Question 5 - Pickup Zone with Largest Total Amount on November 18

Find the pickup zone with the most trips on November 18, 2025:

```sql
SELECT tz."Zone" as pickup_zone, COUNT(*) count_trips FROM public.yellow_taxi_trips tt
JOIN public.taxi_zones tz
	ON tz."LocationID" = tt."PULocationID"
WHERE DATE(lpep_pickup_datetime) = '2025-11-18'
GROUP BY tz."Zone"
ORDER BY COUNT(*) DESC
LIMIT 1
```

**Answer:** East Harlem North

#### Question 6 - Largest Tip from East Harlem North

For passengers picked up in "East Harlem North" in November 2025, find the dropoff zone with the largest tip:

```sql
SELECT
    tzd."Zone" AS dropoff_zone,
    tt.tip_amount AS sum_tip
FROM public.yellow_taxi_trips tt
JOIN public.taxi_zones tzp
    ON tzp."LocationID" = tt."PULocationID"
JOIN public.taxi_zones tzd
    ON tzd."LocationID" = tt."DOLocationID"
WHERE EXTRACT(MONTH FROM tt.lpep_pickup_datetime) = 11
  AND EXTRACT(YEAR FROM tt.lpep_pickup_datetime) = 2025
  AND tzp."Zone" = 'East Harlem North'
ORDER BY sum_tip DESC
LIMIT 1
```

**Answer:** Yorkville West

#### Question 7 - Terraform Workflow

Which sequence describes the Terraform workflow for:

1. Downloading provider plugins and setting up backend
2. Generating proposed changes and auto-executing the plan
3. Removing all resources managed by Terraform

**Answer:** `terraform init`, `terraform apply -auto-approve`, `terraform destroy`

## Project Description

### Project Overview

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
