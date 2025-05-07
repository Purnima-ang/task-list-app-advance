# Stage 1: Builder - Install dependencies
FROM python:3.9-slim-buster as builder

WORKDIR /app

# Install pipenv or venv and system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install dependencies in a local user directory
RUN pip install --upgrade pip \
 && pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime - Smaller final image
FROM python:3.9-slim-buster

WORKDIR /app

# Install system dependencies needed at runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    netcat \
 && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

# Copy installed Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Optional: Healthcheck to ensure Gunicorn starts correctly
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:5000/health || exit 1

# Expose app port
EXPOSE 5000

# Use Gunicorn for production WSGI server
CMD ["gunicorn", "app:create_app()", "--bind", "0.0.0.0:5000", "--workers=4", "--threads=2"]


