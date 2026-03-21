# AI-Powered Quiz Backend API

This project provides a backend system for an AI-powered quiz platform. It supports user authentication, dynamic quiz generation via AI, stateful quiz attempts with resume functionality, and basic analytics.

---

## Technical Stack

* **Framework:** Django 6 and Django REST Framework (DRF)
* **Database:** PostgreSQL
* **Authentication:** JWT (SimpleJWT)
* **AI Integration:** Google Gemini API
* **Containerization:** Docker and Docker Compose
* **Deployment:** Railway
* **Documentation:** Swagger / OpenAPI

---

## Database Schema and Model Relationships

The system utilizes a normalized schema with the following entities:

* **User:** Extends the default user model to include role-based access (User vs. Admin).
* **Quiz:** Stores metadata including topic, difficulty, and question count.
* **Question:** Linked to a Quiz; stores MCQ content and correct answers.
* **Attempt:** Tracks a user's progress through a quiz. It manages state (started, in-progress, completed) to allow for session resumption.
* **Response:** Captures a user's selection for a specific question within an attempt.

Relationships are enforced via foreign keys with unique constraints (e.g., one response per question per attempt) and indexed for efficient querying of history and analytics.

---

## API Endpoints

### Authentication
JWT-based authentication is required for most endpoints.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Obtain access and refresh tokens |
| POST | `/api/auth/refresh/` | Refresh expired access token |

### Quiz & AI Generation
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/api/quizzes/` | List all available quizzes |
| POST | `/api/quizzes/create/` | Create a quiz shell (Admin only) |
| POST | `/api/quizzes/{id}/generate/` | Trigger AI to populate quiz with questions |

### Quiz Interaction
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| POST | `/api/attempts/` | Start a new quiz attempt |
| POST | `/api/attempts/{id}/answer/` | Submit or update an answer |
| POST | `/api/attempts/{id}/submit/` | Finalize attempt and calculate score |
| GET | `/api/history/` | View authenticated user's attempt history |

---

## AI Integration

The system uses the Gemini API to generate structured Multiple Choice Questions (MCQs).

* **Implementation:** AI logic is encapsulated in a utility layer separate from views. Prompts are constructed using validated inputs (topic, difficulty) to ensure predictable outputs.
* **Reliability:** A retry mechanism is implemented to handle transient API failures or malformed JSON responses.
* **Parsing:** AI-generated data is parsed and validated before being committed to the database as structured `Question` and `Option` objects.

---

## Design Decisions and Trade-offs

* **Stateful Attempt Architecture:** The choice to track attempts independently allows for a "resume" feature. This adds complexity to the database but significantly improves user experience.
* **Server-Side Integrity:** Answer correctness is calculated on the server at the moment of submission to prevent client-side score tampering.
* **JWT over Sessions:** Chosen to maintain a stateless API, facilitating easier scaling and potential integration with multiple front-end clients.

---

## Challenges and Solutions

* **Duplicate Submissions:** To prevent users from submitting multiple answers for the same question in one attempt, the backend uses `update_or_create` logic combined with database-level unique constraints.
* **AI Rate Limiting:** Managed via structured error handling and a back-off retry mechanism in the utility layer.
* **Schema Normalization:** Balancing the need for complex analytics (admin view) with fast reads for users taking quizzes led to the implementation of indexed foreign keys on the `Response` and `Attempt` models.

---

## Local Setup

### 1. Prerequisites
* Docker and Docker Compose

### 2. Clone and Configure
```bash
git clone https://github.com/kirtana442/AI_Powered_Quiz_webapp_backend.git
cd AI_Powered_Quiz_webapp_backend
docker-compose build
```

Create a `.env` file in the root:
```text
POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypass
POSTGRES_HOST=db
POSTGRES_PORT=5432
GEMINI_API_KEY=your_api_key
SECRET_KEY=django_secret_key
```

### 3. Run Application
```bash
docker-compose build
docker-compose run --rm web python manage.py migrate
docker-compose up
```
The API will be available at `http://localhost:8000`. Documentation is accessible at `/api/docs/`.

---

**Test the APIs online:** [https://aipoweredquizwebappbackend-production.up.railway.app/api/docs/](https://aipoweredquizwebappbackend-production.up.railway.app/api/docs/)

> This is the official site for testing the APIs directly — no local setup required.

---

## Testing Approach

* **Manual Verification:** Verified end-to-end flows (Auth -> Quiz Creation -> AI Generation -> Attempt -> Scoring) using the Swagger UI.
* **Role Validation:** Ensured Admin-only endpoints (analytics, quiz creation) are restricted via DRF permission classes.
* **Integrity Checks:** Database constraints were tested by attempting to inject duplicate responses and malformed attempt states.
