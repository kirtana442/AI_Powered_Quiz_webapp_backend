# AI-Powered Quiz API

## Overview
Backend for a quiz system built using:
* **Django 6** + **Django REST Framework**
* **PostgreSQL**
* **JWT Authentication** (SimpleJWT)
* **Docker**

**Features:**
* JWT-based authentication
* Role-based access control (User/Admin)
* Quiz and attempt system
* Dockerized setup

**Test the APIs online:** [https://aipoweredquizwebappbackend-production.up.railway.app/api/docs/](https://aipoweredquizwebappbackend-production.up.railway.app/api/docs/)

> This is the official site for testing the APIs directly — no local setup required.

---

## Setup

### Prerequisites
* Docker
* Docker Compose

### Run Project Locally
```bash
git clone https://github.com/kirtana442/AI_Powered_Quiz_webapp_backend.git
cd AI_Powered_Quiz_webapp_backend
```

### Create .env
Create a `.env` file in the root directory:
```bash
POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypass
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### Start Services
```bash
docker compose up --build
```

### Run Migrations
```bash
docker compose run --rm web python manage.py migrate
```

---

## Authentication

JWT-based authentication is required for most endpoints.

**Header format:**
```http
Authorization: Bearer <access_token>
```

---

## Test Admin User

For testing purposes, a **demo admin** account is pre-created on the deployed system.

* **Username:** `testadmin`
* **Password:** `admin123`
* **Role:** `ADMIN`

> ⚠️ This account is for testing/demo purposes only. Do not use it in production.

**Usage:**
1. Log in via `/api/auth/login/` with the credentials above.
2. Copy the returned `access` token.
3. Include the token in the `Authorization` header to test **all admin-only endpoints**.

---

## API Endpoints

### Health Check
`GET /health/`

### Auth
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Get access & refresh tokens |
| POST | `/api/auth/refresh/` | Refresh expired access token |

### Quiz
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| POST | `/api/quizzes/create/` | Create quiz (Admin) |
| GET | `/api/quizzes/` | List all quizzes |
| GET | `/api/quizzes/{id}/` | Get quiz details |
| POST | `/api/quizzes/{id}/generate/` | AI-generated questions |

### Attempt
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| POST | `/api/attempts/` | Start a new attempt |
| POST | `/api/attempts/{id}/answer/` | Submit or update an answer |
| POST | `/api/attempts/{id}/submit/` | Finalize and submit attempt |

### History
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/api/history/` | View auth user's history |

---

## Authorization & Roles

**Default:** Authentication required for all endpoints except where noted.

**Public Endpoints:**
* `/api/auth/register/`
* `/api/auth/login/`

**Roles:**
* **USER:** Can take quizzes and view personal history.
* **ADMIN:** Can create/manage quizzes and view all system data.

---

## Core Logic

### Attempt Flow
`START` → `ANSWER` → `SUBMIT` → `SCORE`

### Answer Update (Django ORM)
```python
Response.objects.update_or_create(
    attempt=attempt,
    question=question,
    defaults={
        "selected_option": option,
        "is_correct": option.is_correct
    }
)
```

### Scoring Logic
```python
total_score = sum(
    r.question.points for r in attempt.responses.all() if r.is_correct
)
```

---
## Docker Services
* **web:** Django application running on port `8000`.
* **db:** PostgreSQL database instance.
```
