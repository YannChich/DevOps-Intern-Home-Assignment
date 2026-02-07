# DevOps Intern – Home Assignment (F5)

This repository contains my solution for the DevOps Intern home assignment.
The objective of this project is to demonstrate fundamental DevOps skills, including containerization, automated testing, Docker Compose orchestration, and CI automation using GitHub Actions.

---

## Project Overview

The project is composed of the following components:

- A custom **Nginx Docker image** running two HTTP servers in a single container
- A **Python-based test container** responsible for validating the expected behavior
- A **Docker Compose** configuration to orchestrate and network the services
- A **GitHub Actions CI pipeline** that builds, tests, and publishes artifacts based on test results

---

## Architecture

The system consists of two containers running on the same Docker network:

- **Nginx container**
  - Exposes two HTTP endpoints on different ports
- **Test container**
  - Sends HTTP requests to the Nginx container
  - Determines success or failure based on response validation

The CI pipeline relies on the test container exit code as the single source of truth.

---

## Nginx Configuration

The Nginx container is based on **Ubuntu**, as required by the assignment, and contains two server blocks:

### Server on port 8080
- Returns an HTTP **200 OK**
- Responds with a custom HTML page

### Server on port 8081
- Always returns an HTTP **500 Internal Server Error**

Screenshots demonstrating both behaviors are available in the `screenshots/` directory.

---

## Automated Tests

Automated tests are executed from a separate Docker image using Python.

The test script:
- Waits for the Nginx service to become available
- Sends HTTP requests to both servers
- Validates:
  - Status code and response content for port 8080
  - Status code for port 8081
- Exits with:
  - `0` if all tests pass
  - `1` if any test fails

This exit code is used directly by the CI pipeline.

---

## Docker Compose

Docker Compose is used to:

- Build both Docker images locally
- Run the Nginx and test containers on the same network
- Allow inter-container communication using service names

To run the project locally:

```bash
docker compose up --build
```

---

## CI Pipeline

The CI pipeline is implemented using GitHub Actions and is defined in `.github/workflows/ci.yml`.

On each push or pull request to the `main` branch, the pipeline:

1. Checks out the repository
2. Builds the Docker images
3. Runs the services using Docker Compose
4. Uses the test container exit code to determine the result
5. Publishes an artifact:
   - `succeeded` if tests pass
   - `fail` if tests fail

---

## Project Structure

```
.
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf
├── tests/
│   ├── Dockerfile
│   └── test_app.py
├── Resource/screenshots/
│   ├── nginx-8080.png
│   └── nginx-8081.png
├── .github/
│   └── workflows/
│       └── ci.yml
├── docker-compose.yml
└── README.md
```

---

## Design Decisions and Assumptions

- Ubuntu was selected as the Nginx base image to comply with the assignment requirements
- The test image uses a lightweight Alpine-based Python image to minimize size
- No external Python dependencies are used
- Docker Compose service names are used for inter-container communication
- Tests are deterministic and designed to be easy to understand

---

## How to Run Locally

### Requirements
- Docker
- Docker Compose (v2)

### Steps
```bash
git clone <your-repository-url>
cd devops-intern-home-assignment
docker compose up --build
```

---

## Assignment Status

- Implemented Nginx Docker image with two server blocks
- Implemented automated HTTP tests
- Implemented Docker Compose orchestration
- Implemented GitHub Actions CI pipeline with conditional artifacts
