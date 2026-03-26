---

# My FastAPI Template

## Overview

This repository is a **modular FastAPI backend template** designed for building and showcasing **data science and LLM proof-of-concept (POC) projects** including:

* Authentication (JWT-based)
* Database integration (SQLAlchemy + Alembic)
* LLM integration (Google Gemini via LangChain)
* Rate limiting
* Clean architecture with service layers

The goal is to keep the system **structured and scalable**, while still lightweight enough for rapid experimentation.

---

## Features

### Core API

* FastAPI application with modular routing
* Automatic Swagger docs (`/docs`)
* Health (`/health`) and metrics (`/metrics`) endpoints

### Authentication

* User registration and login
* JWT-based authentication
* Password hashing with bcrypt
* Protected route example (`/auth/me`)

### Database

* SQLAlchemy ORM
* Alembic migrations
* PostgreSQL-ready (configurable via `.env`)
* Models:

  * Users
  * Data Catalogs
  * ML Models
  * Pipelines

### LLM Integration

* Google Gemini via LangChain
* Example: `/llm/summarize`
* Easily extendable for agents or workflows

### Rate Limiting

* Implemented using `slowapi`
* Example: summarization endpoint limited to `5 requests/minute`

### Machine Learning Support

* Placeholder ML pipeline structure
* Model loading and inference service
* Ready for training + deployment workflows

### Frontend (Minimal)

* Streamlit-based frontend scaffold
* Runs alongside backend via Docker

---

## Project Structure

# Project Structure

```
backend/
├── __pycache__
├── alembic
│   ├── __pycache__
│   ├── versions
│   │   ├── __pycache__
│   │   ├── __init__.py
│   │   └── 001_initial.py
│   ├── __init__.py
│   ├── env.py
│   └── script.py.mako
├── api
│   └── endpoints
│       ├── __pycache__
│       ├── agent.py
│       ├── auth.py
│       ├── example.py
│       └── llm.py
├── core
│   ├── __pycache__
│   ├── config.py
│   ├── database.py
│   ├── logging.py
│   └── rate_limit.py
├── ml_models
│   └── model.pkl
├── models
│   ├── __pycache__
│   ├── database.py
│   └── schemas.py
├── pipelines
│   └── training.py
├── services
│   ├── __pycache__
│   ├── auth_service.py
│   ├── example_service.py
│   ├── llm_service.py
│   └── ml_service.py
├── __init__.py
├── alembic.ini
├── Dockerfile
├── main.py
├── requirements.txt
└── test.http
```


---

## Architecture

### Request Flow

```
Client (Frontend / API call)
        ↓
FastAPI Route (api/endpoints)
        ↓
Pydantic Schemas (validation)
        ↓
Service Layer (business logic)
        ↓
Database / LLM / ML Model
        ↓
Response (JSON)
```

---

## How to Run the Project

### Docker


### 1. Environment Setup

Copy the template and fill in your local secrets (Gemini API Key, DB Passwords):

Bash

```
cp .env.example .env
```

### 2. Launch the Infrastructure

Use Docker to spin up the PostgreSQL database and the backend services:

Bash

```
docker-compose up --build
```

### 3. Initialize the Database

Once the containers are running, apply the migrations to build your tables:

Bash

```
pip install -r requirements.txt
cd backend
alembic upgrade head
```

---

## 🛠 Database Migrations (Alembic)

We use Alembic to manage database changes. **Never** use `Base.metadata.create_all()` in the code.

### To Create a New Migration

If you change a model in `models/database.py` (e.g., adding a column):

1. **Generate the script:**
    
    Bash
    
    ```
    alembic revision --autogenerate -m "description of change"
    ```
    
2. **Review the script:** Check the new file in `alembic/versions/`.
    
3. **Apply the change:**
    
    Bash
    
    ```
    alembic upgrade head
    ```
    

---

## 🧪 Testing the API

You can run the automated test script to verify Registration, Login, and JWT Token logic:

Bash
```
python scripts/test_auth.py
```


---

## API Endpoints

### Authentication

* `POST /auth/register` → Register user
* `POST /auth/login` → Get JWT token
* `GET /auth/me` → Get current user

### Example

* `POST /example/` → Demo endpoint

### LLM

* `POST /llm/summarize` → Text summarization

### System

* `GET /` → Root
* `GET /health` → Health check
* `GET /metrics` → Basic metrics

---

## Testing

You can test the API using:

* Swagger UI → `/docs`
* VS Code REST Client (`backend/test.http`)
* Python `requests`

---

## Purpose

This repository serves as a **foundation for building**:

* LLM-powered apps
* Data pipelines
* ML model APIs
* Experimental backend systems

It is intentionally **modular and extensible**, so new features can be added without restructuring the project.

---

## Future Improvements

* Role-based authentication
* Background jobs (Celery / workers)
* Better metrics & observability
* CI/CD pipeline
* Deployment configs (cloud-ready)
* More advanced LLM agents

---

## Summary

This is a **production-inspired FastAPI template** tailored for **data science and LLM experimentation**.

It balances:

* Simplicity (easy to extend)
* Structure (clean architecture)
* Capability (auth, DB, LLM, ML ready)

---

If you want, I can also:

* trim this into a “portfolio-friendly” version (short + impressive)
* or add diagrams (architecture / infra) for GitHub README visuals

This template bridges the gap between a **simple script** and a **production-ready microservice**. It is intentionally modular, allowing you to swap out the LLM provider or ML model while keeping the core infrastructure intact.

