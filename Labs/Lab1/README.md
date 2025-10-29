# Workshop #1: SonarQube Setup & First Analysis

## Project Description

This is a sample data pipeline project intentionally designed with various code quality issues for educational purposes. The project demonstrates common problems that SonarQube can detect:

- Security vulnerabilities (hardcoded credentials, SQL injection, unsafe deserialization)
- Code smells (duplicated code, complex functions, unused variables)
- Bugs (resource leaks, exception handling issues)
- Low test coverage (only 2 test files covering ~15% of the code)

## GET project with git from github

```bash
python3 -m venv create sonar
source sonar/bin/activate
pip install pysonar
git clone https://github.com/utopios/sonar-training
cd sonar-training/Labs/Lab1
```

## Project Structure

```
labs/
├── data_pipeline.py          # Main data processing module (NOT TESTED)
├── data_validator.py         # Data validation utilities (PARTIALLY TESTED)
├── database_manager.py       # Database operations (NOT TESTED)
├── file_processor.py         # File handling utilities (NOT TESTED)
├── test_data_pipeline.py     # Minimal tests for data_pipeline
├── test_data_validator.py    # Minimal tests for data_validator
├── sonar-project.properties  # SonarQube configuration
└── requirements.txt          # Python dependencies
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd labs
pip install -r requirements.txt
```

### 2. Run Tests (to see low coverage)

```bash
pytest --cov=. --cov-report=xml --cov-report=term
```

### 3. Start SonarQube

```bash
docker pull sonarqube:community

docker run -d --name sonarqube \
  -p 9000:9000 \
  -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true \
  sonarqube:community
```

### 4. Access SonarQube

- URL: http://localhost:9000
- Default credentials: admin/admin
- Change the password on first login

### 5. Run SonarQube Analysis

```bash
# Install SonarScanner (macOS)
brew install sonar-scanner

# Or download manually
# wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-macosx.zip
# unzip sonar-scanner-cli-5.0.1.3006-macosx.zip
# export PATH=$PATH:$(pwd)/sonar-scanner-5.0.1.3006-macosx/bin

# Generate token in SonarQube UI: My Account > Security > Generate Token

# Run analysis
sonar-scanner \
  -Dsonar.projectKey=my-data-pipeline \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=YOUR_TOKEN_HERE
```

## Workshop Tasks

1. Run the SonarQube analysis
2. Navigate the SonarQube dashboard
3. Identify at least 10 different issues
4. Classify them by type (Security, Bug, Code Smell)
5. Prioritize which issues to fix first
6. Document your findings

## Learning Objectives

By completing this workshop, you will:
- Understand how to set up and configure SonarQube
- Learn to interpret SonarQube's issue classifications
- Identify security vulnerabilities in Python code
- Recognize common code smells and anti-patterns
- Understand the importance of test coverage
- Practice prioritizing technical debt
