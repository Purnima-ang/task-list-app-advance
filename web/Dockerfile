# Stage 1: Builder
FROM python:3.9-slim-buster as builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*


# Add a non-root user with home
RUN adduser --disabled-password --gecos '' --home /home/appuser appuser \
  && chown -R appuser /app /home/appuser

# Create a directory for logs
RUN mkdir -p /app/logs \
  && chown -R appuser /app/logs

# Copy installed packages and app
COPY --from=builder /usr/local /usr/local
COPY . .

USER appuser

# Healthcheck setup (already included in your Dockerfile)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:5000/health || exit 1

EXPOSE 5000

# CMD to run the Flask app using gunicorn
CMD ["gunicorn", "app:create_app()", "--bind", "0.0.0.0:5000", "--workers=4", "--threads=2"]

