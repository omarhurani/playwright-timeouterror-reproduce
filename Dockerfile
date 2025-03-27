FROM mcr.microsoft.com/playwright/python:v1.51.0-noble AS base

WORKDIR /app

# Install Poetry
RUN pip install poetry==2.1.1

# Copy poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Configure poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-interaction --no-ansi

# Copy the rest of the code
COPY . .

# Set environment variables
ENV PORT=8080

# Command to run server
# Use "poetry run serve" to run the server or "poetry run playwright-tool" for CLI
CMD ["poetry", "run", "serve"]