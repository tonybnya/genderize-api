# Multi-stage Dockerfile for Flask API
FROM python:3.12-slim AS builder

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv pip install --system --no-cache -r pyproject.toml

# Production stage
FROM python:3.12-slim AS production

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn
COPY --from=builder /usr/local/bin/flask /usr/local/bin/flask

# Copy application code
COPY app.py utils.py ./

# Expose port 8080 (Fly.io internal port)
EXPOSE 8080

# Run with Gunicorn (4 workers)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--timeout", "30", "--keep-alive", "2", "app:app"]
