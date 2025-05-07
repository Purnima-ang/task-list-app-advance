# 📝 Task List App with Flask, PostgreSQL, and Redis

This project is a multi-service Task List web application built with **Flask**, **PostgreSQL**, and **Redis**, containerized using **Docker Compose**, and deployed via a **CI/CD pipeline using GitHub Actions**. It includes advanced Docker practices like multi-stage builds, environment management, persistent volumes, and secure deployment.

---

## 🚀 Features

- ✅ Create and view tasks via a web UI
- 🐘 PostgreSQL for persistent storage
- 🔄 Redis for caching
- 🐳 Dockerized multi-service architecture
- 🔐 Environment-specific configuration (`.env.dev`, `.env.prod`)
- 📦 Multi-stage builds for optimized images
- 🚢 CI/CD pipeline with GitHub Actions + Docker Hub
- 📊 Advanced logging with Fluentd
- 📈 Monitoring with Prometheus (ready to connect with Grafana)

---

## 🗂 Project Structure

```bash
task-list-app/
├── web/                  # Flask app
│   ├── app.py
│   ├── tests
│       └── test_app.py
│       └── conftest.py
│   ├── .dockerignore
│   ├── requirements.txt
│   ├── Dockerfile
│   └── templates/
│       └── index.html
├── fluentd/
│   └── fluent.conf
├── prometheus/
│   └── prometheus.yml
├── db/                   # PostgreSQL
│   ├── Dockerfile
│   └── init.sql
├── cache/                # Redis
│   └── Dockerfile
├── docker-compose.yml
├── .env.dev              # Development env vars
├── .env.prod             # Production env vars
├── .github/workflows/
│   └── ci.yml            # GitHub Actions pipeline
└── README.md

🛠️ Getting Started
✅ Prerequisites
Docker 20.10+

Docker Compose 1.27+

(For CI/CD) GitHub account and Docker Hub account

🚀 Run in Development
docker compose --env-file .env.dev up --build -d

App will be available at:
➡️ http://localhost:5000

🚀 Run in Production
docker compose --env-file .env.prod up --build -d

⚙️ Environment Configuration
Use .env.dev and .env.prod to manage per-environment variables:

# .env.dev
REDIS_HOST=cache
REDIS_PORT=6379
DB_HOST=db
DB_NAME=tasksdb
DB_USER=postgres
DB_PASSWORD=postgres

Then in docker-compose.yml, these are injected via:

environment:
  REDIS_HOST: ${REDIS_HOST}
  ...

📦 Docker Setup
Each service has its own Dockerfile

Flask app uses a multi-stage build for optimized image size

PostgreSQL data is persisted via a Docker volume (db_data)

Healthcheck added to web, db, and cache services

Non-root user runs Flask app for better security

Default Docker bridge network enables service communication

🛡️ Security & Best Practices
Multi-stage builds reduce image size

Containers avoid running as root (Flask app uses appuser)

Healthchecks ensure services are ready before others depend on them

Secrets (DOCKER_USERNAME, DOCKER_PASSWORD) stored securely in GitHub

.env.* files excluded from version control

🐙 Docker Hub Deployment
🏷️ Tag Your Image
docker tag task-list-app-web purnimang/task_app:web

🔐 Log in to Docker Hub
docker logout
docker login
💡 Note: If using 2FA, use a Docker Access Token.

🚀 Push Image to Docker Hub
docker push purnimang/task_app:web
You can now pull the image via:

docker pull purnimang/task_app:web
Or run it:

docker run -p 5000:5000 purnimang/task_app:web

🔄 CI/CD Pipeline (GitHub Actions)
A full pipeline is included in .github/workflows/ci.yml:

💡 Steps:
Checkout Code

Log in to Docker Hub

Build & Tag Images

Push to Docker Hub

(Optional) Deploy via SSH or similar

🧪 Set Secrets in GitHub
Go to your repo → Settings → Secrets → Actions → Add:

DOCKER_USERNAME

DOCKER_PASSWORD

📊 Logging & Monitoring (Bonus)
📊 Logging with Fluentd

📊Prometheus + Grafana
Prometheus scrapes metrics

Grafana dashboards visualize service health

Instructions for this setup can be added if required.

🧪 Testing
TBD: Add Python unit tests in /web/tests and extend the CI pipeline to run them via:

- name: Run tests
  run: pytest

🌐 Deployment Preview
Live: http://localhost:5000

Or deploy via Docker Hub:

docker pull purnimang/task_app:web
docker run -p 5000:5000 purnimang/task_app:web