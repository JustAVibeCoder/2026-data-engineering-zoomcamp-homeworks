# 🚕 Homework 1 - NYC Taxi Data Ingestion Pipeline

**A containerized data ingestion project using Docker, PostgreSQL, and Python**

> Part of the Data Engineering Zoomcamp - Module 1 Homework

![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)

---

## Table of Contents

- [Solution](#solution)
  - [Homework Answers](#homework-answers)
- [Project Description](#project-description)
  - [Project Overview](#project-overview)
  - [Technology Stack](#-technology-stack)
  - [Main Components](#-main-components)

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

## 🏗️ Project Description

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
