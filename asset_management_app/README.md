# AI-Powered Asset Management Web Application

This project is a full-stack web application designed for financial advisors, providing tools for portfolio analysis, asset recommendations, and client data management, powered by a basic AI engine.

## Overview

The application consists of two main parts:
- **Backend**: A Python FastAPI application providing API endpoints.
- **Frontend**: A TypeScript, React, Next.js application for the user interface.

## Project Structure

- `/backend`: Contains the FastAPI application, database models, CRUD operations, and the AI recommendation engine.
- `/frontend`: Contains the Next.js application, React components, pages, and services for interacting with the backend.

## Getting Started

Please refer to the README files within the `backend` and `frontend` directories for specific setup and running instructions for each part of the application.

- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)

## Core Features (Conceptual)

- Client Management: Add, view, update, and delete client information.
- Portfolio Management: Track assets within client portfolios, view overall portfolio value.
- AI Asset Recommendations: Receive intelligent asset suggestions based on client risk profiles and market trends.
- Data Visualizations (Dashboard): (Planned/Conceptual for this version) Visual overview of key metrics.

## Running with Docker (Recommended)

This application can be built and run using Docker and Docker Compose, which simplifies setup and ensures a consistent environment.

### Prerequisites

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: Usually included with Docker Desktop. If not, [Install Docker Compose](https://docs.docker.com/compose/install/)

### Build and Run

1.  **Navigate to the project root directory**:
    Open your terminal and change to the `asset_management_app` directory (where the `docker-compose.yml` file is located).
    ```bash
    cd path/to/asset_management_app
    ```

2.  **Build the Docker images and start the services**:
    ```bash
    docker-compose build
    docker-compose up -d # -d runs in detached mode (in the background)
    ```
    - `docker-compose build`: This command builds the Docker images for both the `backend` and `frontend` services as defined in their respective `Dockerfile`s.
    - `docker-compose up`: This command starts the services. The `-d` flag is optional and runs the containers in the background. If you omit `-d`, logs will be streamed to your terminal.

3.  **Accessing the Application**:
    Once the services are up and running:
    -   **Frontend Application**: Open your web browser and go to [http://localhost:3000](http://localhost:3000)
    -   **Backend API (Swagger UI)**: Open your web browser and go to [http://localhost:8000/docs](http://localhost:8000/docs)
    -   **Backend API (ReDoc)**: Open your web browser and go to [http://localhost:8000/redoc](http://localhost:8000/redoc)

    The frontend service is configured to communicate with the backend service using Docker Compose\'s internal networking (`http://backend:8000`).

### Stopping the Application

-   If running in detached mode (`-d`) or in another terminal:
    ```bash
    docker-compose down
    ```
-   If running in the foreground (logs streaming), press `Ctrl+C` in the terminal, then run:
    ```bash
    docker-compose down
    ```
    The `docker-compose down` command stops and removes the containers. Add `-v` if you want to remove named volumes (e.g., for the database if you configured one).

### Troubleshooting Docker

-   **Port Conflicts**: If `localhost:3000` or `localhost:8000` are already in use by other applications, you might need to stop those applications or change the port mappings in the `docker-compose.yml` file (e.g., `"3001:3000"`).
-   **Build Failures**: Check the output of `docker-compose build` for any errors. Ensure you have a stable internet connection for downloading base images and dependencies.
-   **Outdated Images**: If you make changes to the source code or Dockerfiles, you should rebuild the images using `docker-compose build` before running `docker-compose up` again. You can also use `docker-compose up --build`.
