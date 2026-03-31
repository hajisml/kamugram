# Stage 1: Build
FROM python:3.11-slim AS builder

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Install dependencies separately to leverage caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Stage 2: Runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the pre-built environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Add virtualenv to PATH
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="."

# Copy project source code
COPY src /app/src
COPY README.md /app/README.md

# Ensure log and data directories are writable
RUN mkdir -p /app/data && chmod 777 /app/data

# Entry point
CMD ["python", "src/main.py"]
