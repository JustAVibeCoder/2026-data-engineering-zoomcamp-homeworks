# 🚕 NYC Taxi Data Ingestion Pipeline

**A containerized data ingestion project using Docker, PostgreSQL, and Python**

> Part of the Data Engineering Zoomcamp - Module 1 Homework

![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)

---

## 📋 Overview

This project demonstrates a containerized data engineering practices by building a complete ETL pipeline for NYC taxi data. It showcases:

- **Docker & Docker Compose** for container orchestration
- **PostgreSQL** for data warehousing
- **Python** for data processing with pandas and SQLAlchemy
- **pgAdmin** for database management
- **JupyterLab** for interactive data exploration
- **Infrastructure as Code** patterns with Terraform

The pipeline automatically ingests NYC taxi trip data and zone information into PostgreSQL, with health checks and dependency management built in.

---

## 📑 Table of Contents

- [Quick Start](#-quick-start)
- [Solution](#solution)
- [Project Architecture](#-project-architecture)
  - [Project Overview](#project-overview)
  - [Technology Stack](#-technology-stack)
  - [Main Components](#-main-components)
- [Implementation Details](#-implementation-details)
  - [Data Ingestion](#data-ingestion-details)
  - [File Structure](#main-files--directories)
  - [Dependencies](#dependencies)

---

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- At least 2GB free disk space

### Build & Run

```bash
# 1. Build the Docker image
docker build -t data-ingest:v0.1 .

# 2. Start all services
docker compose up

# 3. Access the services
# PostgreSQL: localhost:5433 (root/root)
# pgAdmin: http://localhost:8080 (pgadmin@pgadmin.com/pgadmin)
# JupyterLab: http://localhost:8888

# 4. Stop services
docker compose down
```

### Service Endpoints

| Service    | URL                     | Credentials                                    |
| ---------- | ----------------------- | ---------------------------------------------- |
| PostgreSQL | `localhost:5433`        | User: `root` / Pass: `root`                    |
| pgAdmin    | `http://localhost:8080` | Email: `pgadmin@pgadmin.com` / Pass: `pgadmin` |
| JupyterLab | `http://localhost:8888` | No auth required                               |

---

## Solution

### Homework Answers

This section contains the solutions to the Data Engineering Zoomcamp Module 1 homework questions.

### Question 1 - Pip Version

**Task:** What's the version of pip in the python:3.13 image?

```bash
docker run -it --entrypoint=bash python:3.13
pip -V
```

**Answer:** `25.3`

---

### Question 2 - pgAdmin Connection

**Task:** Given the docker-compose.yaml, what hostname and port should pgAdmin use to connect to the postgres database?

**Answer:**

- **Container name:** `postgres:5432`
- **Service name:** `db:5432`

Both are correct as Docker creates internal DNS entries for both container names and service names.

---

### Question 3 - Trips ≤ 1 Mile in November 2025

**Task:** For trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01'), how many trips had a trip_distance of ≤ 1 mile?

```sql
SELECT COUNT(*) AS count_trips
FROM public.yellow_taxi_trips
WHERE lpep_pickup_datetime BETWEEN '2025-11-01' AND '2025-12-01'
  AND trip_distance <= 1;
```

**Answer:** `8,007 trips`

---

### Question 4 - Pickup Day with Longest Trip Distance

**Task:** Which was the pick up day with the longest trip distance? (Exclude trips > 100 miles)

```sql
SELECT DATE(lpep_pickup_datetime) AS pickup_day
FROM public.yellow_taxi_trips
WHERE trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1;
```

**Answer:** `2025-11-14`

---

### Question 5 - Pickup Zone with Most Trips on November 18

**Task:** Which pickup zone had the most trips on November 18th, 2025?

```sql
SELECT
    tz."Zone" AS pickup_zone,
    COUNT(*) AS trip_count
FROM public.yellow_taxi_trips tt
JOIN public.taxi_zones tz
    ON tz."LocationID" = tt."PULocationID"
WHERE DATE(tt.lpep_pickup_datetime) = '2025-11-18'
GROUP BY tz."Zone"
ORDER BY trip_count DESC
LIMIT 1;
```

**Answer:** `East Harlem North`

---

### Question 6 - Largest Tip from East Harlem North

**Task:** For passengers picked up in "East Harlem North" in November 2025, which dropoff zone had the largest single tip?

```sql
SELECT
    tzd."Zone" AS dropoff_zone,
    MAX(tt.tip_amount) AS largest_tip
FROM public.yellow_taxi_trips tt
JOIN public.taxi_zones tzp
    ON tzp."LocationID" = tt."PULocationID"
JOIN public.taxi_zones tzd
    ON tzd."LocationID" = tt."DOLocationID"
WHERE EXTRACT(MONTH FROM tt.lpep_pickup_datetime) = 11
  AND EXTRACT(YEAR FROM tt.lpep_pickup_datetime) = 2025
  AND tzp."Zone" = 'East Harlem North'
ORDER BY largest_tip DESC
LIMIT 1;
```

**Answer:** `Yorkville West`

---

### Question 7 - Terraform Workflow

**Task:** Describe the Terraform workflow for: (1) downloading provider plugins & setup, (2) generating changes & auto-execute, (3) removing resources

**Answer:**

```
terraform init → terraform apply -auto-approve → terraform destroy
```

---

## 🏗️ Project Architecture

### Project Overview

This data engineering project implements a production-ready pipeline with the following capabilities:

- ✅ **Automated Data Ingestion**: Downloads and ingests NYC taxi data from GitHub
- ✅ **Database Management**: Uses PostgreSQL for reliable data storage
- ✅ **Container Orchestration**: Docker Compose manages multiple services
- ✅ **Health Checks**: Ensures PostgreSQL is ready before processing
- ✅ **Interactive Analysis**: JupyterLab for data exploration
- ✅ **Web Interface**: pgAdmin for database administration
- ✅ **Scalable Design**: Chunked data loading for memory efficiency

### 🔧 Technology Stack

| Layer                  | Technology     | Purpose                    |
| ---------------------- | -------------- | -------------------------- |
| **Orchestration**      | Docker Compose | Service coordination       |
| **Database**           | PostgreSQL 17  | Data warehouse             |
| **Database UI**        | pgAdmin 4      | Administration interface   |
| **Data Processing**    | Python 3.13    | ETL logic                  |
| **Package Management** | UV             | Fast dependency resolution |
| **Data Analysis**      | JupyterLab     | Interactive notebooks      |
| **ORM**                | SQLAlchemy     | Database abstraction       |
| **Data Manipulation**  | Pandas         | CSV processing             |

### 🎯 Main Components

#### Service Architecture

```
┌─────────────────────────────────────┐
│     Docker Compose Network          │
├─────────────────────────────────────┤
│  pgdatabase (PostgreSQL 17)        │
│  ├── Database: ny_taxi             │
│  └── Tables: yellow_taxi_trips,    │
│            taxi_zones              │
├─────────────────────────────────────┤
│  pgadmin (Database UI)             │
│  ├── Port: 8080                    │
│  └── Access: localhost:8080        │
├─────────────────────────────────────┤
│  data_ingest (Custom Python)       │
│  ├── Downloads taxi data           │
│  └── Populates PostgreSQL          │
├─────────────────────────────────────┤
│  jupyter (JupyterLab)              │
│  ├── Port: 8888                    │
│  └── Data exploration              │
└─────────────────────────────────────┘
```

---

## 📋 Implementation Details

### Main Files & Directories

### 📁 File Structure & Purpose

#### **`docker-compose.yaml`** - Service Orchestration

Defines all microservices with networking, environment configuration, and health checks:

| Service       | Image                          | Purpose                | Port |
| ------------- | ------------------------------ | ---------------------- | ---- |
| `pgdatabase`  | `postgres:17-alpine`           | Primary data warehouse | 5433 |
| `pgadmin`     | `dpage/pgadmin4:latest`        | DB administration UI   | 8080 |
| `data_ingest` | `data-ingest:v0.1`             | Custom ETL service     | N/A  |
| `jupyter`     | `jupyter/datascience-notebook` | Interactive analysis   | 8888 |

**Key Features:**

- Health checks ensure PostgreSQL readiness
- Service dependencies prevent race conditions
- Persistent volumes for data durability

---

#### **`Dockerfile`** - Image Configuration

Builds the custom data ingestion container with production best practices:

```dockerfile
FROM python:3.13-slim
# Install system dependencies for building psycopg2
RUN apt-get install -y build-essential libpq-dev
# Use UV for fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
RUN uv sync --locked
```

**Optimizations:**

- Minimal base image (slim variant) → smaller footprint
- System dependencies installed before Python packages
- UV package manager → faster, deterministic builds

---

#### **`ingest_data.py`** - Data Processing Logic

Core Python ETL script that:

```python
# Connects to PostgreSQL with SQLAlchemy
# Downloads taxi zone lookup from GitHub
# Loads CSV data in 100K-row chunks for memory efficiency
# Supports CLI parameters for flexibility
```

**Capabilities:**

- Configurable connection parameters (host, user, password, port)
- Customizable table names
- Chunked processing for large datasets
- Error handling and logging

---

#### **`pyproject.toml`** - Project Configuration

Modern Python project manifest with:

```toml
[project]
requires-python = ">=3.12"
dependencies = [
    "pandas>=3.0.0",      # Data manipulation
    "sqlalchemy>=2.0.46",  # Database ORM
    "psycopg2>=2.9.11",   # PostgreSQL driver
    "pyarrow>=23.0.0",    # Efficient data format
    "click>=8.3.1",       # CLI framework
]
```

#### Core Libraries

| Package        | Version | Purpose                                             |
| -------------- | ------- | --------------------------------------------------- |
| **SQLAlchemy** | ≥2.0.46 | Database ORM, connection pooling, schema management |
| **psycopg2**   | ≥2.9.11 | PostgreSQL wire protocol driver                     |
| **pandas**     | ≥3.0.0  | CSV reading, data transformation, type inference    |
| **pyarrow**    | ≥23.0.0 | Apache Arrow for efficient data formats             |
| **click**      | ≥8.3.1  | CLI framework, argument parsing                     |

#### Development Tools

- **Docker** - Containerization and reproducibility
- **Docker Compose** - Multi-container orchestration
- **UV** - Fast, reliable Python package manager
- **JupyterLab** - Interactive data exploration
- **pgAdmin** - Web-based database management

---

## 🎓 Learning Outcomes

This project demonstrates:

✨ **Container Architecture**

- Multi-stage Docker builds
- Health checks and service dependencies
- Volume management for persistence

✨ **Data Engineering Patterns**

- ETL pipeline design
- Chunked data processing
- Connection pooling and resource management

✨ **Database Design**

- Relational schema design
- Foreign key relationships
- Efficient indexing strategies

✨ **Infrastructure as Code**

- Docker Compose declarative syntax
- Service configuration management
- Environment-specific settings

✨ **Data Analysis**

- Advanced SQL queries
- Date/time manipulation
- JOINs and aggregations
- Window functions

---

## 📊 Project Statistics

| Metric                 | Value                                    |
| ---------------------- | ---------------------------------------- |
| **Services**           | 4 (PostgreSQL, pgAdmin, ETL, JupyterLab) |
| **Tables**             | 2 (yellow_taxi_trips, taxi_zones)        |
| **Docker Images**      | 4 (custom + 3 public)                    |
| **Python Version**     | 3.13+                                    |
| **Database**           | PostgreSQL 17                            |
| **Total Dependencies** | 5 core packages + transitive deps        |

---

## 🔍 Next Steps & Enhancements

Potential improvements for production deployment:

- [ ] Add monitoring and logging (Prometheus, ELK Stack)
- [ ] Implement data quality checks (Great Expectations)
- [ ] Add CI/CD pipeline (GitHub Actions)
- [ ] Implement Kubernetes deployment manifests
- [ ] Add database backup/restore procedures
- [ ] Implement row-level security and encryption
- [ ] Add API layer (FastAPI, Flask)
- [ ] Create data lineage tracking
- [ ] Implement schema versioning

---

## 📚 Resources

- [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [NYC Taxi Data](https://github.com/DataTalksClub/nyc-tlc-data)

---

## 📝 License & Attribution

This is a homework project for the Data Engineering Zoomcamp, freely available to learners worldwide.

---

<div align="center">

**Built with ❤️ for data engineering education**

[⬆ Back to Top](#-nyc-taxi-data-ingestion-pipeline)

</div>
- Version constraints for reproducibility
- Compatible with modern Python packaging tools

---

#### **`taxi_zone_lookup.csv`** - Reference Data

Static lookup table containing:

- LocationID (zone identifier)
- Zone (neighborhood name)
- Service Zone classification
- Borough information

Used as fallback/reference for taxi trip data enrichment.

---

### Data Ingestion Details

#### ETL Pipeline Flow

```
GitHub (raw data)
    ↓
ingest_data.py
    ├─ Read CSV in chunks
    ├─ Transform data types
    ├─ Validate constraints
    └─ Insert into PostgreSQL
    ↓
PostgreSQL (persistent storage)
    ├─ yellow_taxi_trips table (main data)
    └─ taxi_zones table (reference data)
    ↓
JupyterLab / pgAdmin (analysis & exploration)
```

#### Processing Parameters

The `data_ingest` service uses these CLI options:

- `--pg-user`: PostgreSQL username (default: root)
- `--pg-pass`: PostgreSQL password (default: root)
- `--pg-host`: Database host (default: postgres)
- `--pg-port`: Database port (default: 5432)
- `--pg-db`: Database name (default: ny_taxi)
- `--data-table-name`: Trips table name (default: yellow_taxi_trips)
- `--zones-table-name`: Zones table name (default: taxi_zones)
- `--chunksize`: Rows per batch (default: 100,000)

#### Data Validation

The pipeline includes:
✅ **Schema validation** via SQLAlchemy ORM  
✅ **Type checking** during pandas read/write  
✅ **Constraint enforcement** at database level  
✅ **Health checks** before processing starts

---

### Dependencies

#### Core Libraries
