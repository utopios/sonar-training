# SonarQube Configuration

This directory contains SonarQube configuration files and examples for Lab 3.

## Contents

- `quality-gates-example.json` - Example Quality Gate configuration
- This README with setup instructions

## Creating a SonarQube Project

### Via Web Interface

1. Log in to your SonarQube server
2. Click **"Create Project"** > **"Manually"**
3. Enter:
   - **Project key**: `python-sample-app` (or your project name)
   - **Display name**: `Python Sample Application`
4. Click **"Set Up"**
5. Choose integration method:
   - **"With GitLab CI"** if using GitLab
   - **"With other CI tools"** if using Cloud Build
   - **"Locally"** for local analysis

### Generate Authentication Token

1. Go to **My Account** > **Security**
2. Enter token name: `ci-pipeline-token`
3. Click **"Generate"**
4. **Copy the token immediately** (you won't be able to see it again)
5. Store it securely in your CI/CD secrets

## Quality Gates

### Default Quality Gate

SonarQube comes with a built-in "Sonar way" quality gate:

| Metric | Operator | Error Threshold |
|--------|----------|----------------|
| Coverage on New Code | is less than | 80% |
| Duplicated Lines on New Code | is greater than | 3% |
| Maintainability Rating on New Code | is worse than | A |
| Reliability Rating on New Code | is worse than | A |
| Security Rating on New Code | is worse than | A |
| Security Hotspots Reviewed on New Code | is less than | 100% |

### Creating Custom Quality Gate

#### Via Web Interface

1. Navigate to **Quality Gates** in SonarQube
2. Click **"Create"**
3. Name it: `Lab 3 Python Quality Gate`
4. Add conditions:

**Condition 1: Code Coverage**
- Metric: `Coverage on New Code`
- Operator: `is less than`
- Value: `80`

**Condition 2: Duplications**
- Metric: `Duplicated Lines (%) on New Code`
- Operator: `is greater than`
- Value: `3`

**Condition 3: Maintainability**
- Metric: `Maintainability Rating on New Code`
- Operator: `is worse than`
- Value: `A`

**Condition 4: Reliability**
- Metric: `Reliability Rating on New Code`
- Operator: `is worse than`
- Value: `A`

**Condition 5: Security**
- Metric: `Security Rating on New Code`
- Operator: `is worse than`
- Value: `A`

**Condition 6: Security Hotspots**
- Metric: `Security Hotspots Reviewed on New Code`
- Operator: `is less than`
- Value: `100`

5. Click **"Save"**

#### Via API

```bash
# Create quality gate
curl -X POST "http://your-sonarqube-server/api/qualitygates/create" \
  -u admin:admin \
  -d "name=Lab 3 Python Quality Gate"

# Get the gate ID from response (e.g., id=5)
GATE_ID=5

# Add conditions
curl -X POST "http://your-sonarqube-server/api/qualitygates/create_condition" \
  -u admin:admin \
  -d "gateId=${GATE_ID}&metric=new_coverage&op=LT&error=80"

curl -X POST "http://your-sonarqube-server/api/qualitygates/create_condition" \
  -u admin:admin \
  -d "gateId=${GATE_ID}&metric=new_duplicated_lines_density&op=GT&error=3"

# Add more conditions as needed...
```

### Assigning Quality Gate to Project

#### Via Web Interface

1. Go to **Project Settings** > **Quality Gate**
2. Select your custom quality gate
3. Click **"Save"**

#### Via API

```bash
curl -X POST "http://your-sonarqube-server/api/qualitygates/select" \
  -u admin:admin \
  -d "gateId=${GATE_ID}&projectKey=python-sample-app"
```

## Quality Gate Metrics Explained

### Coverage Metrics

- **Coverage**: Percentage of code covered by tests
- **Line Coverage**: Percentage of lines executed by tests
- **Branch Coverage**: Percentage of branches executed by tests

**Best Practice**: Aim for >80% coverage

### Duplication Metrics

- **Duplicated Lines (%)**: Percentage of duplicated lines of code
- **Duplicated Blocks**: Number of duplicated blocks

**Best Practice**: Keep below 3%

### Maintainability Rating

Based on Technical Debt Ratio:
- **A**: ≤5%
- **B**: 6-10%
- **C**: 11-20%
- **D**: 21-50%
- **E**: >50%

**Best Practice**: Maintain rating A

### Reliability Rating

Based on number of bugs:
- **A**: 0 bugs
- **B**: at least 1 minor bug
- **C**: at least 1 major bug
- **D**: at least 1 critical bug
- **E**: at least 1 blocker bug

**Best Practice**: Maintain rating A (0 bugs)

### Security Rating

Based on number of vulnerabilities:
- **A**: 0 vulnerabilities
- **B**: at least 1 minor vulnerability
- **C**: at least 1 major vulnerability
- **D**: at least 1 critical vulnerability
- **E**: at least 1 blocker vulnerability

**Best Practice**: Maintain rating A (0 vulnerabilities)

### Security Hotspots

Code that requires manual security review.

**Best Practice**: Review 100% of security hotspots

## Project Settings

### Basic Configuration

Create `sonar-project.properties` in your project root:

```properties
sonar.projectKey=python-sample-app
sonar.projectName=Python Sample Application
sonar.projectVersion=1.0.0

sonar.sources=src
sonar.tests=tests

sonar.language=py
sonar.python.version=3.11

sonar.python.coverage.reportPaths=coverage.xml
sonar.python.xunit.reportPath=junit.xml

sonar.sourceEncoding=UTF-8

sonar.exclusions=**/*_test.py,**/tests/**,**/__pycache__/**,**/venv/**
```

### Advanced Configuration

```properties
# Additional Python settings
sonar.python.pylint.reportPaths=pylint-report.txt
sonar.python.bandit.reportPaths=bandit-report.json

# Code duplication
sonar.cpd.python.minimumtokens=100

# Issue exclusions
sonar.issue.ignore.multicriteria=e1

sonar.issue.ignore.multicriteria.e1.ruleKey=python:S1192
sonar.issue.ignore.multicriteria.e1.resourceKey=**/test_*.py

# SCM settings
sonar.scm.provider=git
sonar.scm.disabled=false

# Links
sonar.links.homepage=https://github.com/your-org/your-repo
sonar.links.ci=https://gitlab.com/your-org/your-repo/pipelines
sonar.links.issue=https://github.com/your-org/your-repo/issues
sonar.links.scm=https://github.com/your-org/your-repo
```

## Viewing Results

### Dashboard

After analysis, view your project dashboard at:
```
https://your-sonarqube-server/dashboard?id=python-sample-app
```

### Key Sections

1. **Overview**: Quick summary of quality metrics
2. **Issues**: List of bugs, vulnerabilities, and code smells
3. **Measures**: Detailed metrics and history
4. **Code**: Browse code with inline issues
5. **Activity**: History of analyses and quality gate status

### Understanding Issue Severity

- **Blocker**: Must be fixed immediately
- **Critical**: Should be reviewed and fixed quickly
- **Major**: Should be reviewed and fixed
- **Minor**: Can be fixed if time permits
- **Info**: Informational, not a problem

### Understanding Issue Types

- **Bug**: Code that is demonstrably wrong or highly likely to yield unexpected behavior
- **Vulnerability**: Security-related issue
- **Code Smell**: Maintainability issue (confusing code, technical debt)
- **Security Hotspot**: Security-sensitive code that requires manual review

## Webhooks

Configure webhooks to notify your CI/CD system when analysis completes.

### Setup

1. Go to **Administration** > **Configuration** > **Webhooks**
2. Click **"Create"**
3. Enter:
   - **Name**: `CI/CD Webhook`
   - **URL**: Your webhook endpoint
   - **Secret**: Optional authentication secret
4. Click **"Create"**

### Payload Example

```json
{
  "serverUrl": "https://your-sonarqube-server",
  "taskId": "AXouyxDpizdp4B1K",
  "status": "SUCCESS",
  "analysedAt": "2023-01-15T10:30:00+0000",
  "revision": "abc123",
  "project": {
    "key": "python-sample-app",
    "name": "Python Sample Application",
    "url": "https://your-sonarqube-server/dashboard?id=python-sample-app"
  },
  "qualityGate": {
    "name": "Lab 3 Python Quality Gate",
    "status": "OK",
    "conditions": [
      {
        "metric": "new_coverage",
        "operator": "LESS_THAN",
        "value": "85.5",
        "status": "OK",
        "errorThreshold": "80"
      }
    ]
  }
}
```

## Troubleshooting

### Analysis Fails with Authentication Error

**Problem**: `HTTP 401 Unauthorized`

**Solution**:
```bash
# Verify token is valid
curl -u YOUR_TOKEN: https://your-sonarqube-server/api/authentication/validate

# Should return: {"valid":true}
```

### Quality Gate Not Applied

**Problem**: Analysis completes but quality gate shows "None"

**Solution**:
1. Check project has a quality gate assigned
2. Verify quality gate conditions are properly configured
3. Ensure analysis includes quality gate check:
   ```bash
   sonar-scanner -Dsonar.qualitygate.wait=true
   ```

### Coverage Not Showing

**Problem**: Coverage shows 0% despite running tests

**Solution**:
1. Ensure `coverage.xml` exists:
   ```bash
   pytest --cov=src --cov-report=xml
   ls -la coverage.xml
   ```

2. Check `sonar-project.properties`:
   ```properties
   sonar.python.coverage.reportPaths=coverage.xml
   ```

3. Verify coverage file path in logs

### Issues Not Appearing

**Problem**: Known issues not shown in SonarQube

**Solution**:
1. Check file exclusions in `sonar-project.properties`
2. Verify source file encoding
3. Check SonarQube version supports your Python version
4. Review analysis logs for warnings

## Best Practices

### 1. Use Quality Profiles

- Create custom quality profiles for your team
- Enable/disable specific rules based on your standards
- Regularly review and update rules

### 2. Focus on New Code

- Prioritize fixing issues in new code
- Use "Clean as You Code" methodology
- Don't require 100% coverage on legacy code immediately

### 3. Regular Reviews

- Review quality gate results after each analysis
- Address blockers and critical issues immediately
- Plan time to reduce technical debt

### 4. Team Standards

- Agree on quality standards as a team
- Document exceptions and why they exist
- Regular retrospectives on code quality

### 5. Integration

- Integrate with your issue tracker
- Set up notifications for quality gate failures
- Make quality gates part of code review process

## Additional Resources

- [SonarQube Documentation](https://docs.sonarqube.org/latest/)
- [Python Plugin Documentation](https://docs.sonarqube.org/latest/analysis/languages/python/)
- [Quality Gates Documentation](https://docs.sonarqube.org/latest/user-guide/quality-gates/)
- [Metric Definitions](https://docs.sonarqube.org/latest/user-guide/metric-definitions/)
