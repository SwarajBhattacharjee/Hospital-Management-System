# DevOps & Automation Lab Capstone Project (ENSP461)
## Viva Preparation, Project Brief & Demonstration Guide

> **Student Name:** Swaraj Bhattacharjee  
> **Roll Number:** 2301730011  
> **Course:** DevOps & Automation Lab (ENSP461) &bull; Semester VII  
> **Project:** PulseCare Hospital Management System (HMS)  
> **Repository:** `https://github.com/SwarajBhattacharjee/Hospital-Management-System.git`

---

## 1. Executive Brief: What We Built & How We Built It

### What Was Built
An automated, containerized, cloud-native **Hospital Management System** with:
1. **Core Web Application:** Role-Based Access Control (Admin, Doctor, Receptionist), Patient CRUD with medical validation, Doctor registry, Appointment scheduling with double-booking prevention, and Administrative Staff management.
2. **RESTful JSON API:** Programmatic endpoints (`/api/patients`, `/api/doctors`, `/api/appointments`) and a public container health check endpoint (`/health`).
3. **Automated Test Suite:** 21 automated unit and integration tests executing under `pytest`.
4. **Hardened Docker Container:** Python 3.12-slim base image, non-root user execution, single-worker multi-threaded Gunicorn WSGI server, and healthcheck probes.
5. **Continuous Integration (CI):** Declarative `Jenkinsfile` automating Checkout &rarr; Environment & Dependencies &rarr; Automated Testing &rarr; Docker Image Packaging.
6. **Git Flow Architecture:** Clean, auditable branch flow (`main` &larr; `develop` &larr; `feature/*`) preserving full commit and merge history.

### How We Built It
- **Application Factory Pattern:** Encapsulated in `app/__init__.py` with `create_app()`, allowing dynamic configuration overrides for tests (in-memory SQLite) vs production (persistent SQLite).
- **Relational Integrity:** Implemented via Flask-SQLAlchemy with timezone-aware timestamps and referential checks blocking deletions of patients or doctors with scheduled appointments.
- **Defensive Concurrency:** Configured Gunicorn with `--workers 1 --threads 4` to prevent SQLite file-level lock deadlocks and eliminate table creation race conditions on startup.
- **Least-Privilege Security (DevSecOps):** Created a dedicated non-root user (`appuser`, UID 1001) in Docker, removed unnecessary world-writable (`chmod 777`) directory permissions, and enforced CSRF protection across all web forms.
- **Volume Persistence:** Bound the container's `/app/instance` directory to a named Docker volume (`hms_db_data`), guaranteeing data survives container recreation.

---

## 2. Step-by-Step Demonstration Script for Your Professor

Follow these exact steps during your practical evaluation:

### Step 1: Show Git Branching Strategy & Clean History (2 minutes)
Open terminal in your project directory and run:
```bash
git branch -a
git log --oneline --graph -8
```
*What to say:*  
> *"Sir/Ma'am, we followed the industry-standard Git Flow model. The `main` branch holds production releases, `develop` serves as our integration branch, and all functional work is isolated in dedicated feature branches (`feature/app-core`, `feature/docker`). We preserve a non-fast-forward merge history so every milestone is traceable."*

---

### Step 2: Demonstrate Automated Testing (2 minutes)
Run the automated test suite in the virtual environment:
```powershell
.\venv\Scripts\pytest -v
```
*What to show:*  
- All **21 tests passing** in ~7–8 seconds.
- Test coverage across `test_auth.py` (session logins, 403 barriers for unauthorized roles), `test_patients.py` (data validation, double-booking rejection), and `test_api.py` (JSON payloads, status codes 200, 201, 400, 401, 403, 404).

*What to say:*  
> *"Our test suite validates business logic and security boundaries before any code can be containerized. For example, we explicitly test that a doctor cannot be double-booked for the same time slot, and that a receptionist receives a 403 Forbidden error if they attempt to access staff management."*

---

### Step 3: Demonstrate Docker Containerization & Health Probes (3 minutes)
Build and launch the container via Docker Compose:
```bash
docker compose up --build -d
docker ps
```
*What to show:*  
- Point out the status column showing `Up ... (healthy)`.
- Inspect the logs to prove only ONE worker booted:
```bash
docker logs hms-application
```
- Query the liveness health probe endpoint directly:
```bash
curl.exe http://localhost:5000/health
```
*(Returns: `{"status":"healthy"}` with HTTP 200)*

*What to say:*  
> *"The application is packaged inside a lightweight Python 3.12-slim container. We defined a container-native `HEALTHCHECK` probe targeting `/health`. Notice in the logs that Gunicorn boots exactly one worker process with 4 threads, which prevents SQLite database lock issues."*

---

### Step 4: Live Web Application Walkthrough (3 minutes)
Open browser at `http://localhost:5000`:
1. **Login as Admin (`admin` / `admin123`):**
   - Show the Dashboard metric cards (Patients, Doctors, Appointments, Staff).
   - Register a new patient and show validation handling (e.g. try invalid phone or age).
   - Schedule an appointment.
2. **Login as Doctor (`doctor` / `doctor123`):**
   - Show that patient editing is disabled (view-only).
   - Go to Appointments and update status to **Completed** using the dropdown.
3. **Login as Receptionist (`receptionist` / `receptionist123`):**
   - Attempt to visit `http://localhost:5000/staff`.
   - Point out the custom **403 Forbidden** error page demonstrating Role-Based Access Control.

---

### Step 5: Prove Database Volume Persistence Across Restarts (2 minutes)
1. Add a patient named `"Viva Demo Patient"`.
2. In terminal, stop and destroy the running container:
```bash
docker compose down
```
3. Restart the container without rebuilding:
```bash
docker compose up -d
```
4. Refresh the browser and show the professor that `"Viva Demo Patient"` **still exists**.

*What to say:*  
> *"Even though container instances are ephemeral and throwaway by design, we mounted a named volume `hms_db_data` to `/app/instance`. When the container was destroyed and recreated, our SQLite database remained completely intact."*

---

### Step 6: Walk Through `Dockerfile` & `Jenkinsfile` (2 minutes)
Open `Dockerfile` and `Jenkinsfile` in VS Code / IDE:
- Highlight the non-root user `appuser` (security).
- Explain the 4 stages in `Jenkinsfile`: `Checkout` &rarr; `Install Dependencies` &rarr; `Run Tests` &rarr; `Build Docker Image`.

---

## 3. Top Expected Viva Questions & Model Answers

### Q1: Why did you configure Gunicorn with `--workers 1 --threads 4` instead of multiple workers?
**Answer:**  
*"SQLite is an embedded, file-based database that locks the database file during write transactions. If we run multiple worker processes, concurrent write operations or simultaneous application startup DDL calls (`db.create_all()`) can result in `sqlite3.OperationalError: database is locked`. By using 1 worker process with 4 threads, all requests share the same process memory space and database connection queue, while the threads handle concurrent web requests efficiently without locking conflicts."*

---

### Q2: Why is the container running under a non-root user (`appuser`)?
**Answer:**  
*"By default, Docker containers run as `root` (UID 0), which poses a critical security risk (container breakout / privilege escalation). In accordance with DevSecOps best practices, our Dockerfile creates a dedicated system user `appuser` (UID 1001) and switches to it using `USER appuser`. If an attacker exploits an application vulnerability, they only gain restricted, unprivileged access inside the container."*

---

### Q3: What is the difference between a container's writable layer and a Docker named volume?
**Answer:**  
*"A container's writable layer is tightly coupled to the container's lifecycle; when the container is deleted (`docker rm`), all data written to that layer is permanently lost. A Docker named volume is stored on the host filesystem independently of the container lifecycle. In our `docker-compose.yml`, we mapped `hms_db_data:/app/instance`, so our SQLite database persists across container updates, restarts, and redeployments."*

---

### Q4: Explain the purpose of the `/health` endpoint and the `HEALTHCHECK` directive in Docker.
**Answer:**  
*"The `/health` endpoint verifies that both the web server and the database connection are operational (executing `SELECT 1`). The Docker `HEALTHCHECK` directive periodically pings this endpoint (every 30 seconds). If the app crashes or the database becomes unreachable, Docker marks the container status as `unhealthy`, allowing container orchestrators like Kubernetes or Docker Compose to restart or replace the unhealthy instance."*

---

### Q5: Why did you use the Application Factory pattern (`create_app()`)?
**Answer:**  
*"The Application Factory pattern avoids global application state. It allows us to instantiate the Flask app with different configurations depending on the environment. In production and local development, it loads the real SQLite database from the `instance/` folder. During automated testing (`conftest.py`), it creates a clean, isolated in-memory database (`sqlite:///:memory:`) that resets between test runs without touching or corrupting production data."*

---

### Q6: How did you implement Role-Based Access Control (RBAC)?
**Answer:**  
*"We implemented custom Python decorators: `@login_required` and `@role_required(*allowed_roles)`. When a request arrives, the decorator checks the user's role stored in the secure session. If an unauthorized role attempts to access an endpoint (e.g. a receptionist accessing `/staff`), the server intercepts the request and issues an HTTP 403 Forbidden status—rendering a clean 403 HTML page for web users or returning a JSON error response for API callers."*

---

### Q7: Explain your CI pipeline stages in the `Jenkinsfile`.
**Answer:**  
*"Our pipeline is written declaratively in a `Jenkinsfile` and consists of 4 sequential quality gates:*
1. *`Checkout`: Pulls the committed revision from GitHub.*
2. *`Install Dependencies`: Sets up a clean virtual environment and installs dependencies from `requirements.txt`.*
3. *`Run Tests`: Executes all 21 pytest tests and generates an XML JUnit report. If any test fails, the pipeline aborts immediately.*
4. *`Build Docker Image`: Only if tests pass, it packages the container with the unique build tag (`hospital-management-system:${BUILD_NUMBER}`)."*

---

### Q8: Why did you use session authentication with CSRF tokens rather than JWTs?
**Answer:**  
*"For a server-rendered monolithic application, server-side session cookies marked `HttpOnly` and `SameSite` combined with CSRF tokens provide stronger default protection against Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF). JWTs stored in browser `localStorage` are vulnerable to token theft via XSS, and adding token revocation lists for JWTs introduces unnecessary complexity for a single-service architecture."*

---

### Q9: How do you prevent a doctor from being double-booked?
**Answer:**  
*"In our appointment booking route (`routes.py`), before inserting an appointment record into the database, we execute an SQLAlchemy query checking if an active appointment already exists for the selected doctor at the exact same date and time where status is not 'Cancelled'. If a match is found, the transaction is rejected and an alert is displayed to the user. We also have an automated test in `test_patients.py` verifying that duplicate bookings are blocked."*

---

### Q10: How does your `.gitignore` contribute to project security?
**Answer:**  
*"Our `.gitignore` excludes sensitive files (`.env`), the virtual environment (`venv/`), test cache directories (`.pytest_cache/`, `__pycache__/`), and local database files (`instance/*.db`). This prevents developers from accidentally committing credentials, local binaries, or test artifacts into the shared GitHub repository."*

---

## 4. Quick Command Reference Sheet

| Task | Command |
| :--- | :--- |
| **Activate venv** | `.\venv\Scripts\Activate.ps1` |
| **Run Tests** | `pytest -v` |
| **Seed Database** | `python init_db.py` |
| **Run Locally** | `python run.py` |
| **Build & Run Docker** | `docker compose up --build -d` |
| **Check Container Status** | `docker ps` |
| **View Container Logs** | `docker logs hms-application` |
| **Test Health Probe** | `curl.exe http://localhost:5000/health` |
| **Stop Docker (Keep Data)** | `docker compose down` |
| **Git Graph** | `git log --oneline --graph -8` |
