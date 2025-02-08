# Use an official Python base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy only essential files to leverage Docker caching
COPY pyproject.toml poetry.lock ./

# Install Poetry (if using Poetry for dependency management)
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --only main

# Copy the entire application
COPY . .

# Expose the port that FastAPI runs on
EXPOSE 9000

# Run the FastAPI application
CMD ["uvicorn", "my_service.main:app", "--host", "0.0.0.0", "--port", "9000"]
