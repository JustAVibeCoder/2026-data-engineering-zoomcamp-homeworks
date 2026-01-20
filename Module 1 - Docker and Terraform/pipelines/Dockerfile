# Defining the base image
FROM python:3.13.11-slim

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Setting main working directory in the container 
WORKDIR /code 

# Add virtual environment to PATH so we can use installed packages
ENV PATH="/app/.venv/bin:$PATH"

# Copying environment files
COPY pyproject.toml uv.lock .python-version ./

# Install packages from the uv config files
RUN uv sync --locked

# Running terminal commands to install required packages
# RUN pip install pandas pyarrow

# Copying local script to the container
COPY ingest_data.py .

# Setting entrypoint to be our script (it will execute when the we run the image)
ENTRYPOINT [ "uv", "run", "python", "ingest_data.py" ]