# Google Cloud Build Configuration for Python with SonarQube

This directory contains Cloud Build pipeline configurations for Python applications with SonarQube integration.

## Available Configurations

### 1. `cloudbuild.yaml` - Complete Pipeline

**Features:**
- Dependency installation
- Code linting (flake8, pylint, bandit)
- Unit testing with coverage
- SonarQube analysis
- Quality Gate validation
- Docker image building and pushing
- Vulnerability scanning
- Staging deployment
- Production deployment (conditional)
- Health checks

**Use when:** You need a production-ready pipeline with all quality checks

**Usage:**
```bash
gcloud builds submit --config=cloudbuild.yaml \
  --substitutions=_SERVICE_NAME=my-app,_SONAR_HOST_URL=https://your-sonar.com
```

### 2. `cloudbuild-simple.yaml` - Simplified Pipeline

**Features:**
- Basic dependency installation
- Testing with coverage
- SonarQube analysis
- Docker build and push
- Cloud Run deployment

**Use when:** You're getting started or need a minimal setup

**Usage:**
```bash
gcloud builds submit --config=cloudbuild-simple.yaml \
  --substitutions=_SERVICE_NAME=my-app,_SONAR_HOST_URL=https://your-sonar.com
```

### 3. `cloudbuild-triggers.yaml` - Trigger Configurations

Contains examples and scripts for creating automated build triggers.

## Prerequisites

### 1. Enable Required APIs

```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### 2. Create SonarQube Token Secret

```bash
# Create the secret
echo -n "YOUR_SONAR_TOKEN" | gcloud secrets create sonar-token \
    --data-file=- \
    --replication-policy="automatic"

# Get your project number
PROJECT_NUMBER=$(gcloud projects describe YOUR_PROJECT_ID --format="value(projectNumber)")

# Grant Cloud Build access to the secret
gcloud secrets add-iam-policy-binding sonar-token \
    --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

### 3. Grant Required Permissions

```bash
# Allow Cloud Build to deploy to Cloud Run
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
    --role="roles/run.admin"

# Allow Cloud Build to act as service account
gcloud iam service-accounts add-iam-policy-binding \
    ${PROJECT_NUMBER}-compute@developer.gserviceaccount.com \
    --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"

# Allow Cloud Build to push images
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
    --role="roles/storage.admin"
```

## Running Builds

### Manual Build Submission

```bash
# Basic build
gcloud builds submit --config=cloudbuild.yaml

# With custom substitutions
gcloud builds submit \
    --config=cloudbuild.yaml \
    --substitutions=_SERVICE_NAME=my-python-app,_REGION=us-central1,_SONAR_HOST_URL=https://sonarqube.example.com

# Deploy to production
gcloud builds submit \
    --config=cloudbuild.yaml \
    --substitutions=_SERVICE_NAME=my-app,_DEPLOY_PRODUCTION=true

# From a specific directory
gcloud builds submit \
    --config=cloudbuild.yaml \
    /path/to/source/code
```

### Viewing Build Status

```bash
# List recent builds
gcloud builds list --limit=10

# Get build details
gcloud builds describe BUILD_ID

# Stream build logs
gcloud builds log BUILD_ID --stream

# View logs for a specific step
gcloud builds log BUILD_ID --stream | grep "STEP_ID"
```

## Creating Automated Triggers

### Trigger on Push to Main Branch

```bash
gcloud builds triggers create github \
    --name="main-branch-build" \
    --repo-name=YOUR_REPO \
    --repo-owner=YOUR_GITHUB_ORG \
    --branch-pattern="^main$" \
    --build-config=cloudbuild.yaml \
    --substitutions=_SERVICE_NAME=python-app,_SONAR_HOST_URL=https://your-sonar.com
```

### Trigger on Pull Request

```bash
gcloud builds triggers create github \
    --name="pull-request-check" \
    --repo-name=YOUR_REPO \
    --repo-owner=YOUR_GITHUB_ORG \
    --pull-request-pattern="^main$" \
    --build-config=cloudbuild.yaml \
    --comment-control=COMMENTS_ENABLED \
    --substitutions=_SERVICE_NAME=python-app-pr
```

### Trigger on Tag (Release)

```bash
gcloud builds triggers create github \
    --name="release-build" \
    --repo-name=YOUR_REPO \
    --repo-owner=YOUR_GITHUB_ORG \
    --tag-pattern="^v[0-9]+\.[0-9]+\.[0-9]+$" \
    --build-config=cloudbuild.yaml \
    --substitutions=_SERVICE_NAME=python-app,_DEPLOY_PRODUCTION=true
```

### Manage Triggers

```bash
# List all triggers
gcloud builds triggers list

# Describe a trigger
gcloud builds triggers describe TRIGGER_ID

# Run a trigger manually
gcloud builds triggers run TRIGGER_NAME --branch=main

# Delete a trigger
gcloud builds triggers delete TRIGGER_ID
```

## Pipeline Stages

### Complete Pipeline Flow

```
┌───────────┐
│  Install  │  Install Python dependencies
└─────┬─────┘
      │
      ├──────────────┬────────────┐
      ▼              ▼            ▼
┌──────────┐   ┌──────────┐  ┌──────────┐
│   Lint   │   │   Test   │  │ Security │
└─────┬────┘   └─────┬────┘  └────┬─────┘
      │              │            │
      └──────┬───────┴────────────┘
             ▼
      ┌─────────────┐
      │  SonarQube  │  Code analysis
      └──────┬──────┘
             ▼
      ┌─────────────┐
      │Quality Gate │  Validate standards
      └──────┬──────┘
             ▼
      ┌─────────────┐
      │Docker Build │  Create container image
      └──────┬──────┘
             ▼
      ┌─────────────┐
      │    Push     │  Push to GCR
      └──────┬──────┘
             ▼
      ┌─────────────┐
      │Vuln. Scan   │  Security scanning
      └──────┬──────┘
             │
             ├─────────────────┐
             ▼                 ▼
      ┌────────────┐    ┌────────────┐
      │  Staging   │    │ Production │
      │   Deploy   │    │   Deploy   │
      └────────────┘    └────────────┘
```

### Step-by-Step Explanation

#### Step 1-2: Install & Lint
```yaml
- name: 'python:3.11-slim'
  entrypoint: 'bash'
  args:
    - '-c'
    - |
      pip install -r requirements.txt
      flake8 src/
```
**Duration:** ~1-2 minutes
**Purpose:** Install dependencies and check code style

#### Step 3: Test
```yaml
- name: 'python:3.11-slim'
  args:
    - '-c'
    - 'pytest --cov=src --cov-report=xml'
```
**Duration:** ~2-5 minutes
**Purpose:** Run tests and generate coverage reports

#### Step 4-5: SonarQube Analysis
```yaml
- name: 'sonarsource/sonar-scanner-cli'
  args:
    - '-c'
    - 'sonar-scanner ...'
```
**Duration:** ~2-3 minutes
**Purpose:** Analyze code quality, bugs, and security issues

#### Step 6: Quality Gate
```yaml
- name: 'gcr.io/cloud-builders/curl'
  args:
    - '-c'
    - 'curl SonarQube API...'
```
**Duration:** ~30 seconds
**Purpose:** Verify code meets quality standards

#### Step 7-8: Docker Build & Push
```yaml
- name: 'gcr.io/cloud-builders/docker'
  args: ['build', '-t', '...', '.']
```
**Duration:** ~3-5 minutes
**Purpose:** Create and push container image

#### Step 9: Vulnerability Scan
```yaml
- name: 'gcr.io/cloud-builders/gcloud'
  args: ['container', 'images', 'describe', '...']
```
**Duration:** ~1 minute
**Purpose:** Scan image for known vulnerabilities

#### Step 10-11: Deploy & Test
```yaml
- name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
  args: ['run', 'deploy', '...']
```
**Duration:** ~2-3 minutes
**Purpose:** Deploy to Cloud Run and verify

## Customization Examples

### Change Python Version

```yaml
substitutions:
  _PYTHON_VERSION: '3.10'

steps:
  - name: 'python:${_PYTHON_VERSION}'
    ...
```

### Add Environment-Specific Configs

```yaml
# Development
substitutions:
  _ENVIRONMENT: 'development'
  _MEMORY: '512Mi'
  _MAX_INSTANCES: '5'

# Production
substitutions:
  _ENVIRONMENT: 'production'
  _MEMORY: '2Gi'
  _MAX_INSTANCES: '100'
```

### Run Tests in Parallel

```yaml
- name: 'python:3.11'
  id: 'unit-tests'
  args: ['pytest', 'tests/unit/']
  waitFor: ['install']

- name: 'python:3.11'
  id: 'integration-tests'
  args: ['pytest', 'tests/integration/']
  waitFor: ['install']

- name: 'sonarsource/sonar-scanner-cli'
  id: 'sonar'
  waitFor: ['unit-tests', 'integration-tests']
```

### Add Database Migrations

```yaml
- name: 'python:3.11'
  id: 'migrate'
  entrypoint: 'bash'
  args:
    - '-c'
    - |
      pip install -r requirements.txt
      python manage.py migrate
  waitFor: ['quality-gate']
```

### Conditional Production Deployment

```yaml
- name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
  entrypoint: 'bash'
  args:
    - '-c'
    - |
      if [ "$BRANCH_NAME" = "main" ] && [ "$_MANUAL_APPROVAL" = "true" ]; then
        gcloud run deploy production-app ...
      else
        echo "Skipping production deployment"
      fi
```

## Troubleshooting

### Issue: Secret Not Found

**Error:** `ERROR: (gcloud.secrets.versions.access) NOT_FOUND`

**Solution:**
```bash
# Verify secret exists
gcloud secrets list

# Check IAM permissions
gcloud secrets get-iam-policy sonar-token

# Grant access if needed
PROJECT_NUMBER=$(gcloud projects describe PROJECT_ID --format="value(projectNumber)")
gcloud secrets add-iam-policy-binding sonar-token \
    --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

### Issue: Build Timeout

**Error:** `ERROR: build step X exceeded timeout`

**Solution:**
```yaml
# Increase timeout for specific step
- name: 'python:3.11'
  timeout: '600s'  # 10 minutes
  ...

# Or increase overall build timeout
timeout: '3600s'  # 1 hour
```

### Issue: Docker Push Permission Denied

**Error:** `denied: Permission "artifactregistry.repositories.uploadArtifacts" denied`

**Solution:**
```bash
# Grant storage admin role
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
    --role="roles/storage.admin"
```

### Issue: Cloud Run Deployment Fails

**Error:** `ERROR: (gcloud.run.deploy) PERMISSION_DENIED`

**Solution:**
```bash
# Grant Cloud Run admin role
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
    --role="roles/run.admin"

# Grant service account user role
gcloud iam service-accounts add-iam-policy-binding \
    ${PROJECT_NUMBER}-compute@developer.gserviceaccount.com \
    --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"
```

### Issue: SonarQube Connection Failed

**Error:** Analysis fails with connection timeout

**Solution:**
```bash
# Test connectivity from Cloud Build
gcloud builds submit --config=- <<EOF
steps:
  - name: 'gcr.io/cloud-builders/curl'
    args: ['https://your-sonar-server.com/api/system/status']
EOF

# Check if SonarQube server is accessible from Google Cloud
# If using VPN/firewall, ensure Cloud Build IPs are whitelisted
```

### Issue: Quality Gate Fails

**Error:** Build fails at quality-gate step

**Solution:**
1. Check SonarQube dashboard for specific issues
2. Review quality gate conditions
3. Fix code issues or adjust quality gate
4. For testing, make it non-blocking:

```yaml
- name: 'gcr.io/cloud-builders/curl'
  id: 'quality-gate'
  args: ['...']
  allowFailure: true  # Don't fail build
```

## Best Practices

### 1. Use Substitutions for Configuration

```yaml
substitutions:
  _SERVICE_NAME: 'my-app'
  _REGION: 'europe-west1'
  _SONAR_HOST_URL: 'https://sonar.example.com'
```

### 2. Optimize Build Time

```yaml
# Use slim images
- name: 'python:3.11-slim'  # Not python:3.11

# Cache pip packages
- name: 'python:3.11-slim'
  env:
    - 'PIP_CACHE_DIR=/workspace/.pip-cache'
  volumes:
    - name: 'pip-cache'
      path: '/workspace/.pip-cache'
```

### 3. Separate Development and Production

```yaml
# Use different configs
# cloudbuild-dev.yaml
# cloudbuild-prod.yaml

# Or use substitutions
substitutions:
  _ENV: 'production'
```

### 4. Monitor Build Metrics

```bash
# View build history
gcloud builds list --format="table(id,status,startTime,duration,substitutions)"

# Get average build time
gcloud builds list --limit=10 --format="value(duration)"
```

### 5. Use Tags for Organization

```yaml
tags:
  - 'python'
  - 'sonarqube'
  - 'production'
  - '${_SERVICE_NAME}'
```

### 6. Store Artifacts

```yaml
artifacts:
  objects:
    location: 'gs://${PROJECT_ID}_cloudbuild/artifacts/${BUILD_ID}'
    paths:
      - 'coverage.xml'
      - 'test-results/**'
```

## Additional Resources

- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [Cloud Build Pricing](https://cloud.google.com/build/pricing)
- [Cloud Build Triggers](https://cloud.google.com/build/docs/automating-builds/create-manage-triggers)
- [SonarQube Scanner](https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)

## Cost Optimization

### Free Tier
- First 120 build-minutes per day: Free
- N1_HIGHCPU_8: ~3 minutes of free builds per day

### Optimization Tips
```yaml
# Use smaller machine types for simple builds
options:
  machineType: 'N1_HIGHCPU_8'  # or E2_HIGHCPU_8

# Reduce build time
- Optimize Docker images
- Cache dependencies
- Run steps in parallel
```

## Support

For issues or questions:
1. Check [main Lab README](../README.md)
2. Review Cloud Build logs
3. Verify all permissions are correctly set
4. Test individual steps locally with Docker
