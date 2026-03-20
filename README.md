
---

# AI-Powered Quiz API

## Overview
Backend for a quiz system built using:
* Django 6 + Django REST Framework
* PostgreSQL
* JWT Authentication (SimpleJWT)
* Docker

**Features:**
* JWT-based authentication
* Role-based access (User/Admin)
* Quiz and attempt system (in progress)
* Dockerized setup

---

## Setup

### Prerequisites
* Docker
* Docker Compose

### Run Project
```bash
git clone <repo-url>
cd django-docker-app
```

### Create .env
```bash
POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypass
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### Start services
```bash
docker compose up --build
```

### Run migrations
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

## API Endpoints

### Health Check
`GET /health/`

**Response:**
```json
{
  "status": "ok"
}
```

### Auth
#### Register
`POST /api/auth/register/`

**Body:**
```json
{
  "username": "user1",
  "password": "pass123"
}
```

#### Login
`POST /api/auth/login/`

**Body:**
```json
{
  "username": "user1",
  "password": "pass123"
}
```

**Response:**
```json
{
  "access": "<token>",
  "refresh": "<token>",
  "user": {
    "id": 1,
    "username": "user1",
    "role": "USER"
  }
}
```

#### Refresh
`POST /api/auth/refresh/`

**Body:**
```json
{
  "refresh": "<refresh_token>"
}
```

### Quiz
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| POST | `/api/quizzes/create/` | Create quiz (Admin) |
| GET | `/api/quizzes/` | List quizzes |
| GET | `/api/quizzes/{id}/` | Get quiz details |
| POST | `/api/quizzes/{id}/generate` | AI-generated questions for created quiz | 
### Attempt
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| POST | `/api/attempts/` | Start a new attempt |
| POST | `/api/attempts/{id}/answer/` | Submit or update an answer |
| POST | `/api/attempts/{id}/submit/` | Finalize and submit attempt |

### History
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/api/history/` | View authenticated user's history |

---

## Authorization & Roles

**Default:** Authentication required for all endpoints.

**Public Endpoints:**
* `/api/auth/register/`
* `/api/auth/login/`

**Roles:**
* **USER:** Can take quizzes and view personal history.
* **ADMIN:** Can create/manage quizzes and view all data.

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

---
