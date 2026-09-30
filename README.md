# PulseCare Hospital Management System (HMS)

> **Course:** DevOps & Automation Lab (ENSP461)  
> **Program:** B.Tech CSE – Semester VII  
> **Student Name:** Swaraj Bhattacharjee  
> **Roll Number:** 2301730011  
> **Project Title:** Design and Implementation of an End-to-End DevOps Pipeline for Cloud-Native Application Deployment  
> **Technology Stack:** Python 3.12 &bull; Flask &bull; SQLite &bull; Bootstrap 5 &bull; Gunicorn &bull; Docker &bull; pytest

---

## 1. Project Overview

**PulseCare Hospital Management System** is a lightweight, academic web application and RESTful API created for the DevOps & Automation Lab Capstone Project. It is designed to demonstrate modern software engineering practices, test automation, containerization, and continuous delivery without unnecessary distributed systems complexity.

### Key Capabilities
- **Authentication & RBAC:** Role-Based Access Control using secure Werkzeug password hashing and session cookies for Admin, Doctor, and Receptionist roles.
- **Patient Management:** Full CRUD operations with input validation (regex phone check, blood group enum, age boundaries) and appointment history.
- **Doctor Roster:** Physician registry with clinical specializations and consulting schedules.
- **Appointment Scheduling:** Conflict detection preventing doctor double-booking for overlapping time slots.
- **Administrative Staff:** Staff records management restricted strictly to administrators.
- **RESTful API:** Session-authenticated JSON endpoints under `/api` for programmatic access.
- **Health Probes:** Container and database liveness endpoint at `/health`.

---

## 2. Capstone Phase Mapping

The table below reflects the official 11-phase lab syllabus from `docs/Capstone assignment.pdf`:

| Phase | Phase Name | Status | Deliverables / Notes |
| :--- | :--- | :--- | :--- |
| **Phase 1** | **Version Control (Git)** | **Done** | Git repository initialized, branch flow (`main`, `develop`, `feature/*`), merge history. |
| **Phase 2** | **Continuous Integration (Jenkins)** | **Prepared** | Declarative `Jenkinsfile` with Checkout, Dependency Install, Test Execution, and Docker Build. |
| **Phase 3** | **Docker** | **Implemented** | Python 3.12-slim `Dockerfile` (non-root `appuser`, single-worker Gunicorn), `docker-compose.yml` with persistent volume. |
| **Phase 4** | **Kubernetes** | *Future phase* | Deployment, Service, ConfigMap, Secret, PersistentVolume, scaling & rolling updates. |
| **Phase 5** | **Ansible** | *Future phase* | Playbooks for configuration management and deployment automation. |
| **Phase 6** | **Terraform** | *Future phase* | Infrastructure as Code using reproducible modules, variables, and outputs. |
| **Phase 7** | **Monitoring** | *Future phase* | Prometheus metrics and Grafana dashboards for container & application telemetry. |
| **Phase 8** | **Logging** | *Future phase* | Centralized logging configuration (ELK Stack or Fluentd). |
| **Phase 9** | **Security** | *Future phase* | SonarQube code scanning, image vulnerability auditing, RBAC hardening, Jenkins credentials. |
| **Phase 10**| **Deployment Strategy** | *Future phase* | Blue-Green or Canary deployment workflow. |
| **Phase 11**| **GitOps** | *Future phase* | Declarative GitOps deployment using ArgoCD or FluxCD. |

---

## 3. Academic Notice & Demo Credentials

> ⚠️ **WARNING: ACADEMIC DEMO PURPOSES ONLY**  
> The accounts below are pre-seeded solely for demonstration and evaluation. They must never be used in production environments.

| Username | Password | Role | Permissions |
| :--- | :--- | :--- | :--- |
| `admin` | `admin123` | **Admin** | Unrestricted access: full CRUD, staff management, deletions |
| `receptionist` | `receptionist123` | **Receptionist** | Manage patients and appointments; view doctors; no staff or delete access |
| `doctor` | `doctor123` | **Doctor** | View-only access; ability to mark appointments as Completed or Cancelled |

---

## 4. Local Execution & Testing Guide

### Prerequisites
- Python 3.12+
- Git

### Commands

1. **Activate Virtual Environment:**
   ```powershell
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   ```
   ```bash
   # Linux / macOS
   source venv/bin/activate
   ```

2. **Install Pinned Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize Database & Seed Demo Records:**
   ```bash
   python init_db.py
   ```

4. **Execute Automated Test Suite:**
   ```bash
   pytest -v
   ```

5. **Start Application Server:**
   ```bash
   python run.py
   ```
   Access the dashboard at `http://localhost:5000`.

---

## 5. Docker & Container Deployment

### Running with Docker Compose (Recommended)
```bash
# Build image and start container in detached mode
docker compose up --build -d

# Verify container status and health probe
docker ps

# Inspect container logs (verify single Gunicorn worker)
docker logs hms-application

# Stop container without removing the persistent volume
docker compose down
```

> **Note:** Never run `docker compose down -v` if you wish to keep SQLite database data intact, as `-v` removes named volumes.

---

## 6. Git Workflow & Conflict Resolution

### Branch Hierarchy
```
main (stable, production releases)
  └── develop (integration branch)
        ├── feature/app-core (Flask modules, DB models, test suite)
        ├── feature/docker (Dockerfile, docker-compose, volume persistence)
        └── feature/jenkins-readme (Jenkinsfile, assignment documentation)
```

### Demonstrating Merge Conflict Resolution for Evaluators
To fulfill the Phase 1 requirement of demonstrating conflict resolution:
```bash
# 1. Create a conflict simulation branch off develop
git checkout develop
git checkout -b feature/conflict-demo-a

# 2. Make an edit to a test file or doc
echo "# Note by Team A" >> conflict_test.txt
git add conflict_test.txt
git commit -m "docs: add note from branch A"

# 3. Create second branch off develop
git checkout develop
git checkout -b feature/conflict-demo-b
echo "# Note by Team B" >> conflict_test.txt
git add conflict_test.txt
git commit -m "docs: add note from branch B"

# 4. Attempt to merge branch A into branch B
git merge feature/conflict-demo-a
# Git outputs: CONFLICT (add/add): Merge conflict in conflict_test.txt

# 5. Inspect and resolve
# Open conflict_test.txt, remove <<<<<<< and >>>>>>> markers, save desired content
git add conflict_test.txt
git commit -m "fix(merge): resolve conflict between demo-a and demo-b"
```

---

## 7. REST API Reference

All programmatic endpoints require an active session cookie:

- `GET /health` - Health probe (200 OK / 503 Unhealthy)
- `GET /api/patients` - List all patients (200 OK)
- `POST /api/patients` - Create new patient (201 Created / 400 Bad Request)
- `GET /api/patients/<id>` - Retrieve specific patient with appointments (200 OK / 404 Not Found)
- `PUT /api/patients/<id>` - Update patient details (200 OK / 400 Bad Request)
- `DELETE /api/patients/<id>` - Delete patient, blocked if appointments exist (200 OK / 400 Conflict / 403 Forbidden)
- `GET /api/doctors` - List doctors and schedules (200 OK)
- `GET /api/appointments` - List scheduled consultations (200 OK)
