# Lab 3: Testing with SonarQube and CI/CD Pipelines

## Lab Objectives

- Integrate SonarQube code quality analysis into CI/CD pipelines
- Implement CI/CD pipeline with GitLab CI
- Implement CI/CD pipeline with Google Cloud Build
- Automate testing, code analysis, and deployment for Python applications
- Configure Quality Gates to enforce code quality standards

## Prerequisites

- GitLab account (for GitLab CI/CD method)
- Google Cloud Platform account (for Cloud Build method)
- Access to a SonarQube server (URL and authentication token)
- Git installed locally
- Python 3.8+ installed
- Basic understanding of Python and CI/CD concepts

## Table of Contents

1. [SonarQube Configuration](#1-sonarqube-configuration)
2. [Method 1: CI/CD with GitLab](#2-method-1-cicd-with-gitlab)
3. [Method 2: CI/CD with Google Cloud Build](#3-method-2-cicd-with-google-cloud-build)
4. [Analyzing SonarQube Results](#4-analyzing-sonarqube-results)
5. [Best Practices](#5-best-practices)

---

## 1. SonarQube Configuration

### 1.1 Accessing SonarQube

- SonarQube server URL (e.g., `https://sonarqube.example.com`)
- Login credentials or authentication method

### 1.2 Creating a SonarQube Project

1. Log in to the SonarQube server
2. Click on **"Create Project"** > **"Manually"**
3. Enter project details:
   - **Project key**: `my-python-app` (must be unique)
   - **Display name**: `My Python Application`
4. Click **"Set Up"**
5. Choose **"With GitLab CI"** or **"Locally"** based on your method
6. Generate an authentication token:
   - Token name: `ci-pipeline-token`
   - **Important**: Copy and save the token securely (you'll need it later)

### 1.3 Project Configuration File

Create a `sonar-project.properties` file at the root of your project:

```properties
# Project identification
sonar.projectKey=my-python-app
sonar.projectName=My Python Application
sonar.projectVersion=1.0

# Source code location
sonar.sources=src
sonar.tests=tests

# Python specific settings
sonar.language=py
sonar.python.version=3.8,3.9,3.10,3.11

# Coverage report location
sonar.python.coverage.reportPaths=coverage.xml

# Exclude files from analysis
sonar.exclusions=**/*_test.py,**/tests/**,**/__pycache__/**,**/venv/**

# Encoding
sonar.sourceEncoding=UTF-8
```

---

## 2. Method 1: CI/CD with GitLab

### 2.1 GitLab Pipeline Architecture

The GitLab CI/CD pipeline consists of the following stages:

```
┌─────────┐   ┌──────────┐   ┌───────────┐   ┌──────────────┐   ┌─────────┐
│  Build  │──▶│   Test   │──▶│  SonarQube│──▶│ Quality Gate │──▶│ Deploy  │
└─────────┘   └──────────┘   └───────────┘   └──────────────┘   └─────────┘
```

**Stages:**
1. **Build**: Install dependencies and prepare environment
2. **Test**: Run unit tests with coverage
3. **Analyze**: SonarQube code quality analysis
4. **Quality Gate**: Verify quality standards are met
5. **Deploy**: Deploy to staging/production

### 2.2 GitLab CI Configuration

See the complete configuration in [gitlab/.gitlab-ci.yml](gitlab/.gitlab-ci.yml)

Key features:
- Python virtual environment setup
- Automated testing with pytest
- Code coverage with pytest-cov
- SonarQube integration
- Quality Gate validation
- Multi-environment deployment

### 2.3 Setting up GitLab Variables

Navigate to your GitLab project: **Settings** > **CI/CD** > **Variables**

Add the following variables:

| Variable Name | Value | Protected | Masked | Description |
|---------------|-------|-----------|--------|-------------|
| `SONAR_HOST_URL` | `https://your-sonar-server.com` | ✓ | ✗ | SonarQube server URL |
| `SONAR_TOKEN` | `your-sonarqube-token` | ✓ | ✓ | SonarQube authentication token |
| `GCP_PROJECT_ID` | `your-gcp-project` | ✓ | ✗ | Google Cloud project ID (if deploying to GCP) |
| `GCP_SERVICE_KEY` | `{json-key-content}` | ✓ | ✓ | GCP service account key |

### 2.4 Available GitLab Configurations

- [gitlab/.gitlab-ci.yml](gitlab/.gitlab-ci.yml) - Complete pipeline with all features
- [gitlab/.gitlab-ci-simple.yml](gitlab/.gitlab-ci-simple.yml) - Simplified pipeline for quick start
- [gitlab/.gitlab-ci-docker.yml](gitlab/.gitlab-ci-docker.yml) - Pipeline with Docker containerization

### 2.5 Running the GitLab Pipeline

1. Add the configuration to your project:
```bash
cp gitlab/.gitlab-ci.yml .gitlab-ci.yml
```

2. Commit and push to trigger the pipeline:
```bash
git add .gitlab-ci.yml sonar-project.properties
git commit -m "Add GitLab CI/CD with SonarQube integration"
git push origin main
```

3. Monitor the pipeline:
   - Go to **CI/CD** > **Pipelines** in GitLab
   - Click on the running pipeline to see detailed logs
   - View job outputs for each stage

4. Check SonarQube results:
   - After the analysis stage completes
   - Open your SonarQube server and navigate to your project

---

## 3. Method 2: CI/CD with Google Cloud Build

### 3.1 Cloud Build Pipeline Architecture

```
┌───────┐   ┌──────┐   ┌──────────┐   ┌─────────┐   ┌────────┐   ┌────────┐
│Install│──▶│ Lint │──▶│   Test   │──▶│ SonarQube│──▶│Quality │──▶│ Deploy │
│ Deps  │   │      │   │+ Coverage│   │ Analysis │   │ Gate   │   │        │
└───────┘   └──────┘   └──────────┘   └─────────┘   └────────┘   └────────┘
```

### 3.2 Cloud Build Configuration

See the complete configuration in [cloud-build/cloudbuild.yaml](cloud-build/cloudbuild.yaml)

### 3.3 Google Cloud Platform Setup

#### 3.3.1 Enable Required APIs

```bash
# Authenticate with GCP
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

#### 3.3.2 Configure Secrets

Store your SonarQube token securely using Secret Manager:

```bash
# Create the secret
echo -n "YOUR_SONAR_TOKEN" | gcloud secrets create sonar-token \
    --data-file=- \
    --replication-policy="automatic"

# Grant Cloud Build access to the secret
PROJECT_NUMBER=$(gcloud projects describe YOUR_PROJECT_ID --format="value(projectNumber)")

gcloud secrets add-iam-policy-binding sonar-token \
    --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

# Verify the secret was created
gcloud secrets describe sonar-token
```

#### 3.3.3 Grant Additional Permissions

```bash
# Allow Cloud Build to deploy to Cloud Run
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
    --role="roles/run.admin"

# Allow Cloud Build to act as a service account
gcloud iam service-accounts add-iam-policy-binding \
    ${PROJECT_NUMBER}-compute@developer.gserviceaccount.com \
    --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"
```

### 3.4 Available Cloud Build Configurations

- [cloud-build/cloudbuild.yaml](cloud-build/cloudbuild.yaml) - Complete pipeline
- [cloud-build/cloudbuild-simple.yaml](cloud-build/cloudbuild-simple.yaml) - Simplified version
- [cloud-build/cloudbuild-triggers.yaml](cloud-build/cloudbuild-triggers.yaml) - Trigger configurations

### 3.5 Running Cloud Build

#### Manual Execution

```bash
# Navigate to your project directory
cd /path/to/your/project

# Submit the build
gcloud builds submit \
    --config=cloudbuild.yaml \
    --substitutions=_SERVICE_NAME=my-python-app,_SONAR_HOST_URL=https://your-sonar-server.com

# Stream the logs
gcloud builds log --stream
```

#### Automated with Triggers

```bash
# Create a trigger for the main branch
gcloud builds triggers create github \
    --name="main-branch-trigger" \
    --repo-name=YOUR_REPO \
    --repo-owner=YOUR_GITHUB_USERNAME \
    --branch-pattern="^main$" \
    --build-config=cloudbuild.yaml \
    --substitutions=_SERVICE_NAME=my-python-app,_SONAR_HOST_URL=https://your-sonar-server.com

# List all triggers
gcloud builds triggers list

# Run a trigger manually
gcloud builds triggers run main-branch-trigger --branch=main
```

### 3.6 Viewing Build Results

```bash
# List recent builds
gcloud builds list --limit=10

# Get detailed information about a build
gcloud builds describe BUILD_ID

# View logs for a specific build
gcloud builds log BUILD_ID

# Check deployed services on Cloud Run
gcloud run services list
```

---

## 4. Analyzing SonarQube Results

### 4.1 Understanding the Dashboard

After a successful analysis, your SonarQube dashboard shows:

#### Main Metrics:
- **Bugs**: Potential runtime errors
- **Vulnerabilities**: Security issues
- **Code Smells**: Maintainability problems
- **Coverage**: Percentage of code covered by tests
- **Duplications**: Percentage of duplicated code
- **Security Hotspots**: Code requiring security review

#### Rating System:
- **A**: Excellent (0 issues or <5% technical debt)
- **B**: Good
- **C**: Moderate
- **D**: Poor
- **E**: Very poor

### 4.2 Quality Gates

Quality Gates define minimum quality standards. Default criteria:

```yaml
Coverage:              > 80%
Duplicated Lines:      < 3%
Maintainability Rating: A
Reliability Rating:     A
Security Rating:        A
New Bugs:              = 0
New Vulnerabilities:   = 0
```

#### Creating Custom Quality Gates

1. Navigate to **Quality Gates** in SonarQube
2. Click **Create**
3. Add conditions:
   - Coverage on New Code > 80%
   - Duplicated Lines on New Code < 3%
   - Maintainability Rating = A
4. Set as default or assign to specific projects

### 4.3 Reviewing Issues

1. **Navigate to Issues**: Click on the issue count in your project
2. **Filter by type**: Bugs, Vulnerabilities, Code Smells
3. **Filter by severity**: Blocker, Critical, Major, Minor, Info
4. **Review details**: Each issue shows:
   - Description of the problem
   - Why it's an issue
   - How to fix it
   - Code location

### 4.4 Local Analysis

Run SonarQube analysis locally before pushing:



---

## 5. Best Practices

### 5.1 Code Organization

```
my-python-app/
├── src/                    # Application source code
│   ├── __init__.py
│   ├── main.py
│   └── utils/
├── tests/                  # Test files
│   ├── __init__.py
│   ├── test_main.py
│   └── test_utils.py
├── .gitlab-ci.yml         # GitLab CI configuration
├── cloudbuild.yaml        # Cloud Build configuration
├── sonar-project.properties
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── Dockerfile
└── README.md
```

### 5.2 Security Best Practices

1. **Never commit secrets**:
   ```bash
   # Add to .gitignore
   .env
   *.key
   *.pem
   credentials.json
   ```

2. **Use secret management**:
   - GitLab: CI/CD Variables (masked)
   - GCP: Secret Manager
   - Never hardcode tokens or passwords

3. **Limit permissions**:
   - Use minimal required permissions for service accounts
   - Enable Protected Variables for sensitive data
   - Use Protected Branches for production deployments

### 5.3 Testing Strategy

```python
# Example: tests/test_main.py
import pytest
from src.main import calculate_sum

def test_calculate_sum():
    assert calculate_sum(2, 3) == 5
    assert calculate_sum(-1, 1) == 0
    assert calculate_sum(0, 0) == 0

def test_calculate_sum_invalid_input():
    with pytest.raises(TypeError):
        calculate_sum("a", "b")
```

Coverage requirements:
- Aim for >80% code coverage
- Focus on critical business logic
- Include edge cases and error handling
- Use parametrized tests for multiple scenarios

### 5.4 Quality Gate Strategy

**For Development Branches**:
```yaml
New Code Coverage:     > 80%
New Duplications:      < 3%
New Issues:            < 5 minor issues
```

**For Production Branches**:
```yaml
Overall Coverage:      > 80%
New Bugs:              = 0
New Vulnerabilities:   = 0
Blocker Issues:        = 0
Critical Issues:       = 0
```

### 5.5 Pipeline Optimization

1. **Use caching**:
   ```yaml
   # GitLab
   cache:
     key: ${CI_COMMIT_REF_SLUG}
     paths:
       - .venv/
       - .pip-cache/
   ```

2. **Parallel execution**:
   ```yaml
   test:
     parallel:
       matrix:
         - PYTHON_VERSION: ["3.8", "3.9", "3.10", "3.11"]
   ```

3. **Conditional jobs**:
   ```yaml
   deploy-production:
     only:
       - main
     when: manual
   ```

### 5.6 Monitoring and Notifications

Configure notifications for:
- Pipeline failures
- Quality Gate failures
- Security vulnerabilities
- Coverage drops

Example Slack notification:
```yaml
notify:
  script:
    - |
      curl -X POST -H 'Content-type: application/json' \
        --data '{"text":"Build failed for '"${CI_PROJECT_NAME}"'"}' \
        ${SLACK_WEBHOOK_URL}
  when: on_failure
```

---

## Practical Exercises

### Exercise 1: Basic Setup (GitLab)

**Objective**: Set up a basic CI/CD pipeline with SonarQube

**Tasks**:
1. Clone the sample Python application
2. Configure SonarQube project
3. Add `.gitlab-ci.yml` to your repository
4. Configure CI/CD variables in GitLab
5. Push code and verify pipeline execution
6. Review SonarQube analysis results

**Expected outcome**: Green pipeline with successful SonarQube analysis

### Exercise 2: Basic Setup (Cloud Build)

**Objective**: Set up Cloud Build pipeline with SonarQube

**Tasks**:
1. Set up GCP project and enable APIs
2. Configure Secret Manager with SonarQube token
3. Add `cloudbuild.yaml` to repository
4. Submit manual build
5. Create automated trigger
6. Review build logs and SonarQube results

**Expected outcome**: Successful build and deployment to Cloud Run

### Exercise 3: Custom Quality Gate

**Objective**: Create and enforce custom quality standards

**Tasks**:
1. Create a custom Quality Gate in SonarQube:
   - Coverage > 85%
   - Duplications < 5%
   - No new bugs
   - Maintainability Rating = A
2. Assign it to your project
3. Modify your code to fail the Quality Gate
4. Observe pipeline failure
5. Fix issues to pass the Quality Gate

**Expected outcome**: Pipeline fails with poor code, passes after improvements

### Exercise 4: Multi-Environment Deployment

**Objective**: Implement staging and production environments

**Tasks**:
1. Create separate Quality Gates for staging and production
2. Configure deployment to staging on `develop` branch
3. Configure manual deployment to production on `main` branch
4. Test the workflow:
   - Push to develop → auto-deploy to staging
   - Merge to main → manual approval for production
5. Verify different environment configurations

**Expected outcome**: Proper environment separation with controlled deployments

### Exercise 5: Security Scanning

**Objective**: Add security vulnerability scanning

**Tasks**:
1. Enable Security Hotspots in SonarQube
2. Add SAST (Static Application Security Testing) scan
3. Configure pipeline to fail on critical vulnerabilities
4. Introduce a known vulnerability (e.g., hardcoded password)
5. Observe security scan detection
6. Fix the vulnerability

**Expected outcome**: Security issues detected and resolved

---

## Troubleshooting

### Issue: SonarQube Analysis Failed

**Symptoms**: Pipeline fails at SonarQube analysis stage

**Solutions**:
```bash
# Check token validity
curl -u YOUR_TOKEN: https://your-sonar-server.com/api/authentication/validate

# Verify project key exists
curl -u YOUR_TOKEN: https://your-sonar-server.com/api/projects/search?projects=my-python-app

# Check coverage file exists
ls -la coverage.xml

# Validate sonar-project.properties
cat sonar-project.properties
```

### Issue: Quality Gate Timeout

**Symptoms**: Quality Gate check times out

**Solutions**:
1. Increase timeout in pipeline configuration
2. Check SonarQube server performance
3. Verify webhook configuration in SonarQube

```yaml
# GitLab
sonarqube-check:
  timeout: 10 minutes

# Cloud Build
timeout: '600s'
```

### Issue: Coverage Report Not Found

**Symptoms**: SonarQube shows 0% coverage

**Solutions**:
```bash
# Ensure pytest-cov is installed
pip install pytest-cov

# Generate coverage in XML format
pytest --cov=src --cov-report=xml

# Verify file exists
ls -la coverage.xml

# Check sonar-project.properties
grep "coverage.reportPaths" sonar-project.properties
```

### Issue: GitLab Runner Not Available

**Symptoms**: Pipeline stuck in "pending" state

**Solutions**:
```bash
# Check runner status
gitlab-runner list

# Verify runner tags match
gitlab-runner verify

# Restart runner
gitlab-runner restart
```

### Issue: Cloud Build Permission Denied

**Symptoms**: Build fails with permission errors

**Solutions**:
```bash
# Check service account permissions
gcloud projects get-iam-policy YOUR_PROJECT_ID

# Grant required roles
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
    --role="roles/cloudbuild.builds.builder"

# Verify Secret Manager access
gcloud secrets get-iam-policy sonar-token
```

---

## Additional Resources

### Documentation
- [SonarQube Documentation](https://docs.sonarqube.org/latest/)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [Google Cloud Build Documentation](https://cloud.google.com/build/docs)
- [Python Testing with pytest](https://docs.pytest.org/)

### Lab Files
- [Sample Python Application](sample-app/) - Demo application
- [GitLab CI Configuration](gitlab/) - GitLab CI files
- [Cloud Build Configuration](cloud-build/) - Cloud Build files
- [SonarQube Configuration](sonarqube-config/) - SonarQube settings

### Tools
- [SonarLint](https://www.sonarlint.org/) - IDE plugin for real-time analysis
- [pytest](https://pytest.org/) - Python testing framework
- [coverage.py](https://coverage.readthedocs.io/) - Code coverage measurement
- [gcloud CLI](https://cloud.google.com/sdk/gcloud) - Google Cloud command-line tool

---

## Summary

In this lab, you learned how to:

✓ Configure SonarQube for Python projects
✓ Implement CI/CD pipelines with GitLab CI
✓ Implement CI/CD pipelines with Google Cloud Build
✓ Integrate code quality analysis in pipelines
✓ Configure and enforce Quality Gates
✓ Automate testing, analysis, and deployment
✓ Apply security and quality best practices

Continue practicing with different projects and explore advanced features of each tool!

---

## Next Steps

1. **Explore advanced SonarQube features**:
   - Custom rules
   - Issue workflow
   - Project portfolios

2. **Optimize pipelines**:
   - Parallel execution
   - Caching strategies
   - Conditional deployments

3. **Implement additional checks**:
   - Security scanning (Trivy, Bandit)
   - License compliance
   - Dependency vulnerabilities

4. **Monitor and improve**:
   - Track metrics over time
   - Set up dashboards
   - Continuous improvement of code quality
