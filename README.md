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
backend/
├── main.py                # Application entry point
├── api/
│   └── endpoints/         # API routes (entry points)
├── models/                # Pydantic schemas (input/output validation)
├── services/              # Core logic (LLM, data processing, etc.)
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

### 1. Activate environment

```
conda activate env
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Start the server

```
python -m uvicorn backend.main:app --reload
```

### 4. Open in browser

* API root: http://127.0.0.1:8000/
* Swagger docs: http://127.0.0.1:8000/docs

---

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

* Add Streamlit frontend (`frontend/`)
* Add lightweight database (SQLite)
* Add Docker for reproducibility
* Add basic testing and CI

---

## Summary

This project is a **lightweight, flexible backend template** that will evolve into a collection of **data science and LLM-based applications**, each built using a consistent and clean architecture.

It is intentionally simple to allow rapid experimentation and iteration.
