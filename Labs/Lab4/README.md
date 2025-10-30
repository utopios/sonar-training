# SonarQube Pytho Project

A complete, well-structured Python application with comprehensive test coverage designed for SonarQube analysis demonstration.

## Project Overview

This project demonstrates a production-ready Python application structure with:
- Clean architecture with separate models, services, and utilities
- Comprehensive unit tests with pytest
- High test coverage (80%+ target)
- Proper documentation and type hints
- SonarQube integration with coverage reports

## Project Structure

```
sonarqube-python-project/
├── src/
│   ├── __init__.py
│   └── app/
│       ├── __init__.py
│       ├── models/              # Data models
│       │   ├── __init__.py
│       │   ├── user.py          # User entity with validation
│       │   └── product.py       # Product entity with business logic
│       ├── services/            # Business logic layer
│       │   ├── __init__.py
│       │   ├── user_service.py  # User management service
│       │   └── product_service.py # Product/inventory service
│       └── utils/               # Utility functions
│           ├── __init__.py
│           ├── validators.py    # Input validation utilities
│           └── formatters.py    # Data formatting utilities
├── tests/
│   ├── __init__.py
│   ├── unit/                    # Unit tests
│   │   ├── __init__.py
│   │   ├── test_user_model.py
│   │   ├── test_product_model.py
│   │   ├── test_user_service.py
│   │   └── test_validators.py
│   └── integration/             # Integration tests (optional)
│       └── __init__.py
├── docs/                        # Documentation directory
├── pytest.ini                   # Pytest configuration
├── setup.py                     # Package setup
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
├── sonar-project.properties     # SonarQube configuration
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Features

### Models
- **User Model**: User management with validation (username, email, role)
- **Product Model**: Product/inventory management with stock control

### Services
- **UserService**: Complete CRUD operations for users
- **ProductService**: Product management with inventory operations

### Utilities
- **Validators**: Email, username, password strength, phone, URL validation
- **Formatters**: Currency, date, percentage, file size formatting

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- SonarQube Server or SonarCloud account
- SonarScanner CLI tool

## Installation

### 1. Clone or Navigate to the Project

```bash
cd /Users/ihababadi/Desktop/sonarqube-python-project
```

### 2. Create a Virtual Environment (Recommended)

### 3. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Or install with development dependencies
pip install -r requirements-dev.txt
```

### 4. Install the Package in Development Mode

```bash
pip install -e .
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage Report

```bash
pytest --cov=src --cov-report=xml --cov-report=html --cov-report=term
```

### Run Specific Test Files

```bash
# Run only user model tests
pytest tests/unit/test_user_model.py

# Run only service tests
pytest tests/unit/test_user_service.py -v
```

### View Coverage Report

After running tests with coverage, you can view the HTML report:

```bash
open htmlcov/index.html    # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html   # Windows
```

## SonarQube Analysis

#### 1. Start SonarQube Server

#### 2. Create a Project Token

1. Log in to SonarQube
2. Go to **My Account** → **Security** → **Generate Tokens**
3. Enter a token name (e.g., "python-demo-project")
4. Click **Generate**
5. **Copy and save the token** (you won't see it again)

#### 3. Run Tests with Coverage

```bash
# Generate coverage report in XML format (required by SonarQube)
pytest --cov=src --cov-report=xml --cov-branch
```

This creates a `coverage.xml` file in the project root.

#### 4. Run SonarScanner

#### 5. View Results

Open sonarqube and navigate to your project to see:
- Code coverage metrics
- Code quality issues
- Security vulnerabilities
- Code smells
- Duplications
- Technical debt

## SonarQube Metrics Explained

### Quality Gate Metrics

1. **Coverage**: Percentage of code covered by tests
   - Target: ≥80%
   - This project: ~90%+

2. **Duplications**: Percentage of duplicated code
   - Target: ≤3%

3. **Maintainability Rating**: Based on technical debt
   - A: ≤5% technical debt ratio
   - B: 6-10%
   - C: 11-20%
   - D: 21-50%
   - E: >50%

4. **Reliability Rating**: Based on bugs
   - A: 0 bugs
   - B: 1 minor bug
   - C: 1 major bug
   - D: 1 critical bug
   - E: 1 blocker bug

5. **Security Rating**: Based on vulnerabilities
   - Similar scale to Reliability

### Issue Severity

- **Blocker**: Must be fixed immediately
- **Critical**: Should be fixed quickly
- **Major**: Should be fixed
- **Minor**: Could be fixed
- **Info**: Informational

## TODO Tasks

### GitLab CI/CD Integration
- [ ] Create `.gitlab-ci.yml` configuration file
- [ ] Configure CI/CD pipeline stages (build, test, analysis)
- [ ] Set up Python environment in CI pipeline (Python 3.8+)
- [ ] Add automated testing job with pytest
- [ ] Integrate SonarQube scanner in CI pipeline
- [ ] Configure SonarQube authentication with GitLab CI variables
- [ ] Add coverage report generation in CI pipeline
- [ ] Set up artifact storage for test and coverage reports
- [ ] Configure pipeline to run on merge requests
- [ ] Add quality gate check as pipeline requirement
- [ ] Set up caching for pip dependencies to speed up builds
- [ ] Configure deployment stages (optional)

### Test Coverage Improvement
- [ ] Increase overall test coverage to 95%+
- [ ] Add unit tests for `formatters.py` utility functions
- [ ] Add unit tests for `product_service.py` remaining methods
- [ ] Create integration tests for user-product workflows
- [ ] Add edge case tests for validation functions
- [ ] Add tests for error handling and exception cases
- [ ] Implement parametrized tests for validators
- [ ] Add boundary value tests for product stock operations
- [ ] Create performance/load tests (optional)
- [ ] Add mutation testing to verify test quality
- [ ] Document test scenarios and test data


