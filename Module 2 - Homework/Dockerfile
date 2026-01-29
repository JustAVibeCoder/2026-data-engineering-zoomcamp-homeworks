# Defining the base image
FROM python:3.13.11-slim

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Setting main working directory in the container 
WORKDIR /code 

# Add virtual environment to PATH so we can use installed packages
ENV PATH="/app/.venv/bin:$PATH"

# Install build dependencies for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copying environment files
COPY pyproject.toml uv.lock .python-version ./


# Install packages from the uv config files
RUN uv sync --locked

# Running terminal commands to install required packages
# RUN pip install pandas pyarrow

# Copying local script to the container
COPY ingest_data.py .

# Setting entrypoint to be our script (it will execute when the we run the image)
ENTRYPOINT [ "uv", "run", "ingest_data.py" ]