# Backend - AI Asset Management API

This directory contains the Python FastAPI backend for the AI Asset Management application.

## Features

- **Client Management**: CRUD operations for client data.
- **Asset Management**: CRUD operations for financial assets.
- **Portfolio Management**: Endpoints to manage client portfolios and their constituent assets.
- **AI Recommendation Engine**: Basic rule-based AI to suggest assets based on risk profile and market trends.

## Technology Stack

- Python 3.x
- FastAPI: Modern, fast (high-performance) web framework for building APIs.
- Uvicorn: ASGI server for running FastAPI.
- Pydantic: Data validation and settings management using Python type annotations.
- SQLAlchemy: SQL toolkit and Object Relational Mapper (ORM) for database interaction.
- SQLite: Default database used for simplicity.

## Setup and Running

1.  **Navigate to this directory**:
    ```bash
    cd path/to/asset_management_app/backend
    ```

2.  **Create and activate a virtual environment** (recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    This file (`requirements.txt`) should have been generated during the initial setup and includes FastAPI, Uvicorn, SQLAlchemy, Pydantic, etc.

4.  **Database Initialization**:
    The application is configured to use an SQLite database (`./asset_management.db`). The necessary tables are automatically created when the FastAPI application starts, as defined in `database.py` and called from `main.py`.

5.  **Run the FastAPI application**:
    ```bash
    uvicorn main:app --reload --port 8000
    ```
    - `--reload`: Enables auto-reloading when code changes (useful for development).
    - `--port 8000`: Runs the server on port 8000.

6.  **Access the API**:
    - The API will be available at `http://localhost:8000`.
    - Interactive API documentation (Swagger UI) can be accessed at `http://localhost:8000/docs`.
    - Alternative API documentation (ReDoc) can be accessed at `http://localhost:8000/redoc`.

## Project Structure

- `main.py`: FastAPI application instance, API endpoints.
- `models.py`: Pydantic models for request/response data validation and SQLAlchemy ORM model definitions (though DB models are in `database.py`).
- `crud.py`: Functions for Create, Read, Update, Delete database operations.
- `database.py`: SQLAlchemy database setup, engine, session management, and database table models (`DbClient`, `DbAsset`, `DbPortfolio`).
- `ai_engine.py`: Placeholder logic for AI-based asset recommendations.
- `requirements.txt`: List of Python dependencies.
- `asset_management.db`: SQLite database file (created on first run).
