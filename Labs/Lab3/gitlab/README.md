# GitLab CI/CD Configuration for Python with SonarQube

This directory contains GitLab CI/CD pipeline configurations for Python applications with SonarQube integration.

## Available Configurations

### 1. `.gitlab-ci.yml` - Complete Pipeline

**Features:**
- Python virtual environment setup
- Code linting (flake8, pylint, bandit)
- Unit testing with pytest
- Code coverage reporting
- SonarQube analysis
- Quality Gate validation
- Security scanning (safety)
- Docker image building
- Multi-environment deployment (staging/production)
- Notifications

**Use when:** You need a production-ready pipeline with all quality checks

**Usage:**
```bash
cp gitlab/.gitlab-ci.yml .gitlab-ci.yml
```

### 2. `.gitlab-ci-simple.yml` - Simplified Pipeline

**Features:**
- Basic dependency installation
- Unit tests with coverage
- SonarQube analysis
- Simple deployment

**Use when:** You're getting started or need a minimal setup

**Usage:**
```bash
cp gitlab/.gitlab-ci-simple.yml .gitlab-ci.yml
```

### 3. `.gitlab-ci-docker.yml` - Docker-focused Pipeline

**Features:**
- Application build and test
- SonarQube analysis
- Docker image creation
- Container security scanning (Trivy)
- Cloud Run deployment
- Image registry management

**Use when:** Your application runs in containers

**Usage:**
```bash
cp gitlab/.gitlab-ci-docker.yml .gitlab-ci.yml
```

## Required GitLab Variables

Configure these variables in **Settings > CI/CD > Variables**:

### Core Variables

| Variable | Example | Protected | Masked | Description |
|----------|---------|-----------|--------|-------------|
| `SONAR_HOST_URL` | `https://sonarqube.example.com` | ✓ | ✗ | SonarQube server URL |
| `SONAR_TOKEN` | `squ_abc123...` | ✓ | ✓ | SonarQube authentication token |

### Deployment Variables (if using deployment stages)

| Variable | Example | Protected | Masked | Description |
|----------|---------|-----------|--------|-------------|
| `GCP_PROJECT_ID` | `my-gcp-project` | ✓ | ✗ | Google Cloud project ID |
| `GCP_SERVICE_KEY` | `{base64-encoded-json}` | ✓ | ✓ | GCP service account key (base64 encoded) |

### Docker Registry Variables (if using Docker)

These are usually pre-configured by GitLab:
- `CI_REGISTRY` - GitLab container registry URL
- `CI_REGISTRY_USER` - Registry username
- `CI_REGISTRY_PASSWORD` - Registry password
- `CI_REGISTRY_IMAGE` - Full image name

## Pipeline Stages Explanation

### Stage 1: Build
```yaml
build:
  stage: build
  script:
    - python -m venv .venv
    - source .venv/bin/activate
    - pip install -r requirements.txt
```

**Purpose:** Install dependencies and prepare the environment
**Outputs:** Virtual environment cached for subsequent stages

### Stage 2: Test
```yaml
test:
  stage: test
  script:
    - pytest --cov=src --cov-report=xml
```

**Purpose:** Run unit tests and generate coverage reports
**Outputs:** `coverage.xml`, `junit.xml`, test results

### Stage 3: Analyze
```yaml
sonarqube-analysis:
  stage: analyze
  script:
    - sonar-scanner ...
```

**Purpose:** Analyze code quality and security with SonarQube
**Outputs:** Analysis results sent to SonarQube server

### Stage 4: Quality Gate
```yaml
quality-gate:
  stage: quality-gate
  script:
    - curl SonarQube API to check status
```

**Purpose:** Verify that code meets quality standards
**Outputs:** Pipeline success/failure based on Quality Gate

### Stage 5: Deploy
```yaml
deploy:
  stage: deploy
  script:
    - gcloud run deploy ...
```

**Purpose:** Deploy application to target environment
**Outputs:** Running application in cloud environment

## Pipeline Flow

```
┌─────────┐
│ Trigger │ (Push or MR)
└────┬────┘
     │
     ▼
┌─────────┐
│  Build  │ Install dependencies
└────┬────┘
     │
     ├──────────────┬─────────────┐
     ▼              ▼             ▼
┌─────────┐   ┌─────────┐   ┌─────────┐
│  Test   │   │  Lint   │   │Security │ (Parallel)
└────┬────┘   └────┬────┘   └────┬────┘
     │             │             │
     └──────┬──────┴─────────────┘
            ▼
     ┌─────────────┐
     │  SonarQube  │ Code analysis
     └──────┬──────┘
            ▼
     ┌─────────────┐
     │Quality Gate │ Check standards
     └──────┬──────┘
            │
            ├─────────────┐
            ▼             ▼
     ┌──────────┐   ┌──────────┐
     │  Docker  │   │  Deploy  │
     │  Build   │   │          │
     └──────────┘   └──────────┘
```

## Customization Examples

### Change Python Version

```yaml
variables:
  PYTHON_VERSION: "3.10"  # Change to 3.8, 3.9, 3.11, etc.

build:
  image: python:${PYTHON_VERSION}
```

### Add Custom Test Commands

```yaml
test:
  script:
    - source .venv/bin/activate
    - pytest tests/unit/
    - pytest tests/integration/
    - python -m doctest src/**/*.py
```

### Modify Coverage Requirements

```yaml
test:
  script:
    - pytest --cov=src --cov-fail-under=80  # Fail if coverage < 80%
```

### Deploy to Different Environments

```yaml
deploy-dev:
  environment:
    name: development
  only:
    - develop

deploy-qa:
  environment:
    name: qa
  only:
    - release/*

deploy-prod:
  environment:
    name: production
  only:
    - main
  when: manual  # Require manual approval
```

### Add Slack Notifications

```yaml
notify-slack:
  stage: .post
  script:
    - |
      curl -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"Pipeline ${CI_PIPELINE_STATUS} for ${CI_PROJECT_NAME}\"}" \
        ${SLACK_WEBHOOK_URL}
  when: always
```

### Run Tests in Parallel

```yaml
test:
  parallel:
    matrix:
      - PYTHON_VERSION: ["3.8", "3.9", "3.10", "3.11"]
  image: python:${PYTHON_VERSION}
```

## Troubleshooting

### Issue: Cache Not Working

**Problem:** Dependencies reinstalled every time

**Solution:**
```yaml
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .cache/pip
    - .venv/
  policy: pull-push  # or just 'pull' for read-only
```

### Issue: Tests Failing Locally But Passing in CI

**Problem:** Different environments

**Solution:**
```bash
# Run tests in Docker locally
docker run --rm -v $(pwd):/app python:3.11 sh -c "
  cd /app &&
  pip install -r requirements.txt &&
  pytest
"
```

### Issue: SonarQube Connection Failed

**Problem:** Cannot reach SonarQube server

**Solution:**
```bash
# Test connection
curl -u ${SONAR_TOKEN}: ${SONAR_HOST_URL}/api/system/status

# Check variables are set
echo ${SONAR_HOST_URL}  # Should not be empty
echo ${SONAR_TOKEN}     # Should not be empty
```

### Issue: Quality Gate Times Out

**Problem:** SonarQube analysis takes too long

**Solution:**
```yaml
quality-gate:
  script:
    - sleep 30  # Increase wait time
    - curl ...  # Check status
  timeout: 10 minutes  # Increase job timeout
```

### Issue: Docker Build Fails

**Problem:** Docker-in-Docker not working

**Solution:**
```yaml
docker-build:
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  variables:
    DOCKER_TLS_CERTDIR: "/certs"
  before_script:
    - docker info  # Verify Docker is available
```

### Issue: Permission Denied on GCP Deployment

**Problem:** Service account lacks permissions

**Solution:**
```bash
# Grant required roles
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:SA_EMAIL" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:SA_EMAIL" \
    --role="roles/iam.serviceAccountUser"
```

## Best Practices

### 1. Use Descriptive Job Names

```yaml
# Good
unit-tests-python-3.11:
  stage: test

# Bad
test:
  stage: test
```

### 2. Set Appropriate Timeouts

```yaml
test:
  timeout: 10 minutes  # Prevent hanging jobs

sonarqube:
  timeout: 15 minutes  # Analysis may take longer
```

### 3. Use Artifacts Wisely

```yaml
test:
  artifacts:
    paths:
      - coverage.xml
    expire_in: 1 week  # Auto-cleanup
    when: always       # Keep even if job fails
```

### 4. Fail Fast

```yaml
stages:
  - lint      # Fast checks first
  - test
  - analyze   # Slower checks later
```

### 5. Use Anchors for Reusability

```yaml
.python-base: &python-base
  image: python:3.11
  before_script:
    - source .venv/bin/activate

test:
  <<: *python-base
  script:
    - pytest

lint:
  <<: *python-base
  script:
    - flake8
```

### 6. Protect Sensitive Data

```yaml
# Never do this:
script:
  - echo "Token: ${SONAR_TOKEN}"  # BAD!

# Do this:
script:
  - '[[ -n "${SONAR_TOKEN}" ]] && echo "Token is set"'
```

### 7. Use Rules for Complex Conditions

```yaml
deploy:
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: manual
    - if: '$CI_COMMIT_BRANCH == "develop"'
      when: on_success
    - when: never
```

## Additional Resources

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [GitLab CI/CD Variables](https://docs.gitlab.com/ee/ci/variables/)
- [GitLab Runner Documentation](https://docs.gitlab.com/runner/)
- [SonarQube Integration](https://docs.sonarqube.org/latest/analysis/gitlab-integration/)

## Support

For issues or questions:
1. Check the [main Lab README](../README.md)
2. Review GitLab CI/CD logs
3. Verify all required variables are set
4. Test locally with Docker if possible
