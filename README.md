# Cloud-Native Task Service (FastAPI + PostgreSQL + CI/CD)

![CI/CD Pipeline](https://github.com/simongzvz/cloud-native-api/actions/workflows/ci.yml/badge.svg)

Containerisierte REST-API für Aufgabenverwaltung mit automatisierter Test-, Build- und Deployment-Pipeline.

## Live-Endpunkte
- **Swagger UI:** `https://api.simongzvz.duckdns.org/docs`
- **Healthcheck:** `https://api.simongzvz.duckdns.org/health`
- **Tasks API:** `GET /tasks`, `POST /tasks`

## Architektur & Stack
- **Backend:** Python 3.12, FastAPI, Uvicorn, Pydantic
- **Datenbank:** PostgreSQL 16 (persistentes Volume, Healthcheck-gesteuerter Start)
- **Container Security:** Multi-Stage `Dockerfile` (`python:3.12-slim`), Ausführung als unprivilegierter `appuser` (Non-Root)
- **CI/CD:** GitHub Actions (`ruff` Linting & `pytest` → Multi-Stage Docker Build & Push zu `ghcr.io` → automatisiertes SSH-Deployment via Docker Compose)
- **Ingress & TLS:** Caddy Reverse Proxy mit automatischen Let's-Encrypt-Zertifikaten
