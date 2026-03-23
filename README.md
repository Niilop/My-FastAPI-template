# My FastAPI Template

## Overview

This repository is a **minimal FastAPI-based backend template** designed for building and showcasing my **data science and LLM proof-of-concept (POC) projects**.

The goal is to keep the structure **simple, modular, and extendable**, without unnecessary production-level complexity (e.g., heavy databases, authentication systems, or CI/CD pipelines).

---

## What this project currently does

* Runs a **FastAPI server** using Uvicorn
* Exposes a basic API with:

  * Root endpoint (`/`) → confirms the API is running
  * Health check (`/health`) → simple service status check
  * Example endpoint (`/example/`) → demonstrates full request flow
* Demonstrates a clean architecture:

  * **Routes** (API layer)
  * **Pydantic models** (validation layer)
  * **Services** (business logic layer)

---

## Architecture

The project follows a simple and scalable structure:

```
Template/
├─ backend/
│  ├─ main.py
│  └─ ...
├─ frontend/
│  ├─ app.py
│  └─ ...
├─ docker-compose.yml
└─ README.md
```

### Request Flow

```
Client (browser / requests / frontend)
        ↓
FastAPI Route
        ↓
Pydantic Model (validation)
        ↓
Service Layer (logic)
        ↓
Response (JSON)
```

---

## How to run the project

### Method 1: Using Docker 

This is the easiest way to run the project. It handles all dependencies and sets up both the frontend and backend simultaneously. It also includes volume mounts, so any changes you make to the code will automatically reload in the containers!

### 1. Build and start the containers
`docker compose up --build`
### 2. Open in browser

* Front end: http://localhost:8501/
* API root: http://localhost:8000/
* Swagger docs: http://localhost:8000/docs
* 
### 3. Stop the containers
`docker compose down`


## Testing the API

You can test endpoints using:

* FastAPI Swagger UI (`/docs`)
* Python (`requests`)
* VS Code REST Client (`.http` files)

---

## Purpose and Plan

This repository serves as a **foundation for personal projects**

---

## Future Extensions (Optional)

* Add lightweight database (SQLite)
* Develop Docker
* Update Streamlit frontend
* Add basic testing and CI

---

## Summary

This project is a **lightweight, backend and minimal frontend template** that will later on evolve into a collection of **data science and LLM-based applications**.

It is intentionally simple to allow rapid experimentation and iteration.
