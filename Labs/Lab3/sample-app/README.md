# Python Sample Application

A simple Flask REST API for demonstrating CI/CD pipelines with SonarQube integration.

## Features

- RESTful API with Flask
- Calculator operations (add, subtract, multiply, divide)
- Health check endpoint
- Comprehensive unit tests
- Code coverage reporting
- Dockerized application
- Production-ready with Gunicorn

## Project Structure

```
sample-app/
├── src/
│   ├── __init__.py
│   ├── main.py           # Flask application
│   ├── calculator.py     # Calculator logic
│   └── utils.py          # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_main.py      # API endpoint tests
│   ├── test_calculator.py # Calculator tests
│   └── test_utils.py     # Utility function tests
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
├── sonar-project.properties
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd sample-app
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Running the Application

### Locally

```bash
# Development mode
python src/main.py

# Production mode with Gunicorn
gunicorn --bind 0.0.0.0:8080 --workers 2 src.main:app
```

The application will be available at `http://localhost:8080`

### With Docker

```bash
# Build the image
docker build -t python-sample-app .

# Run the container
docker run -p 8080:8080 python-sample-app

# Run with environment variables
docker run -p 8080:8080 \
  -e ENVIRONMENT=production \
  -e PORT=8080 \
  python-sample-app
```

## API Endpoints

### Health Check
```bash
GET /health

Response:
{
  "status": "healthy",
  "service": "python-sample-app",
  "version": "1.0.0",
  "environment": "development"
}
```

### Home
```bash
GET /

Response:
{
  "message": "Welcome to Python Sample API",
  "endpoints": {
    "health": "/health",
    "add": "/add",
    "subtract": "/subtract",
    "multiply": "/multiply",
    "divide": "/divide"
  }
}
```

### Addition
```bash
POST /add
Content-Type: application/json

{
  "a": 5,
  "b": 3
}

Response:
{
  "operation": "addition",
  "a": 5,
  "b": 3,
  "result": 8.0
}
```

### Subtraction
```bash
POST /subtract
Content-Type: application/json

{
  "a": 10,
  "b": 3
}

Response:
{
  "operation": "subtraction",
  "a": 10,
  "b": 3,
  "result": 7.0
}
```

### Multiplication
```bash
POST /multiply
Content-Type: application/json

{
  "a": 4,
  "b": 5
}

Response:
{
  "operation": "multiplication",
  "a": 4,
  "b": 5,
  "result": 20.0
}
```

### Division
```bash
POST /divide
Content-Type: application/json

{
  "a": 10,
  "b": 2
}

Response:
{
  "operation": "division",
  "a": 10,
  "b": 2,
  "result": 5.0
}
```

## Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_calculator.py

# Run specific test
pytest tests/test_calculator.py::TestAddition::test_add_positive_numbers
```

### Code Coverage

```bash
# Run tests with coverage
pytest --cov=src --cov-report=html --cov-report=term

# View HTML coverage report
open htmlcov/index.html  # On Mac
# or
xdg-open htmlcov/index.html  # On Linux
# or
start htmlcov/index.html  # On Windows
```

### Linting

```bash
# Flake8 (style guide enforcement)
flake8 src/ --max-line-length=120

# Pylint (code quality)
pylint src/

# Black (code formatting)
black src/ tests/

# isort (import sorting)
isort src/ tests/
```

### Security Scanning

```bash
# Bandit (security issues)
bandit -r src/

# Safety (dependency vulnerabilities)
safety check
```


## CI/CD Integration

This application is designed to work with:

- **GitLab CI**: See `.gitlab-ci.yml` in the parent directory
- **Google Cloud Build**: See `cloudbuild.yaml` in the parent directory

Both pipelines include:
- Automated testing
- Code coverage reporting
- SonarQube analysis
- Quality Gate validation
- Docker image building
- Deployment to Cloud Run

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8080` | Port number for the application |
| `ENVIRONMENT` | `production` | Environment name (development/staging/production) |
| `VERSION` | `1.0.0` | Application version |


