# Workshop #2: Deep Dive into Metrics & Code Quality

## Overview

This workshop provides hands-on experience with code quality metrics, refactoring, and achieving high test coverage. You'll analyze a problematic codebase, calculate metrics manually, compare them with SonarQube's analysis, and then work with a refactored version to understand best practices.

## Objectives

By the end of this workshop, you will be able to:
- Understand and manually calculate quality metrics (Cyclomatic Complexity, Cognitive Complexity, Code Duplication)
- Identify and classify code quality issues
- Improve code coverage from ~0% to >80%
- Eliminate code duplication through refactoring
- Apply security best practices to eliminate vulnerabilities

## Duration

90 minutes

## Prerequisites

- Completed Workshop #1 (SonarQube Setup & First Analysis)
- SonarQube running locally (http://localhost:9000)
- Python 3.9+
- Understanding of basic Python programming

---

## Lab Structure

This lab is divided into three parts:

### Part 1: Analyzing a Problematic Codebase
- Review `bad_etl_pipeline.py` - a poorly written ETL pipeline
- Manually calculate complexity metrics
- Run SonarQube analysis
- Document all findings

### Part 2: Calculate Metrics Manually
- Use the provided `metrics_worksheet.md` to document your analysis
- Calculate Cyclomatic Complexity
- Calculate Code Duplication percentage
- Count and classify issues by type

### Part 3: Fix and Improve
- Review `good_etl_pipeline.py` - the refactored version
- Run comprehensive test suite with coverage
- Compare before/after metrics
- Verify all issues resolved

---

## Setup Instructions

### 1. Install Dependencies

```bash
cd labs/lab2

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Verify SonarQube is Running

```bash
# Check if SonarQube is running
curl http://localhost:9000/api/system/status

# If not running, start it:
docker start sonarqube

# Or create new container:
docker run -d --name sonarqube \
  -p 9000:9000 \
  -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true \
  sonarqube:community
```

### 3. Generate SonarQube Token

1. Navigate to http://localhost:9000
2. Login (admin/admin or your changed password)
3. Go to: My Account > Security > Generate Token
4. Name: `workshop2-token`
5. Copy the token for later use

---

## Part 1: Analyzing the Problematic Codebase

### Step 1: Review the Bad Code

Open and read through `bad_etl_pipeline.py`. Look for:

**Security Issues:**

**Code Smells:**

**Bugs:**

### Step 2: Run SonarQube Analysis on Bad Code

```bash
# Make sure you're in the lab2 directory
cd labs/lab2

# Run SonarQube scanner on the bad code only
sonar-scanner \
  -Dsonar.projectKey=bad-etl-pipeline \
  -Dsonar.projectName="Bad ETL Pipeline" \
  -Dsonar.sources=bad_etl_pipeline.py \
  -Dsonar.python.version=3.9 \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=YOUR_TOKEN_HERE

pysonar \
  --sonar-project-key=bad-etl-pipeline \
  --sonar-project-name="Bad ETL Pipeline" \
  --sonar-sources=bad_etl_pipeline.py \
  --sonar-python-version=3.9 \
  --sonar-host-url=http://3.250.2.41/ \
  --sonar-login=YOUR_TOKEN_HERE
```

### Step 3: Explore SonarQube Dashboard

Navigate to http://localhost:9000/dashboard?id=bad-etl-pipeline

Explore these sections:
1. **Overview** - See overall quality gate status
2. **Issues** - Browse all detected issues
3. **Measures** - Review metrics in detail
4. **Code** - See issues highlighted in source code

### Step 4: Document Findings

Use the `metrics_worksheet.md` to document:
- Issue counts by type and severity
- Specific examples of each issue type
- Security vulnerabilities found
- Code duplication percentage

---

## Part 2: Calculate Metrics Manually

### Task 1: Cyclomatic Complexity

Analyze `transform_sales_data()` function:

**How to Calculate:**
- Start with 1 (base complexity)
- Add 1 for each: if, elif, for, while, and, or, except

**Example:**
```python
def example():           # 1 (base)
    if x > 0:            # +1 = 2
        if y > 0:        # +1 = 3
            return True
    return False
# Cyclomatic Complexity = 3
```

**Your Turn:**
Count decision points in `transform_sales_data()` and record in worksheet.

### Task 2: Code Duplication

**How to Calculate:**
```
Duplication % = (Duplicated Lines / Total Lines) × 100
```

**Steps:**
1. Count total lines in `bad_etl_pipeline.py`
2. Identify duplicated blocks (hint: look at transform functions)
3. Count duplicated lines
4. Calculate percentage

Record your findings in the worksheet.

### Task 3: Cognitive Complexity

**Cognitive Complexity** measures how difficult code is to understand.

**Key Rules:**
- +1 for each break in linear flow (if, for, while, etc.)
- +1 for each level of nesting
- +1 for recursion

**Example:**
```python
def example(data):
    if data is not None:      # +1 (break) +1 (nesting=1) = 2
        if len(data) > 0:     # +1 (break) +2 (nesting=2) = 5
            if 'x' in data:   # +1 (break) +3 (nesting=3) = 9
                return True
```

Calculate for `transform_sales_data()` and record in worksheet.

### Task 4: Compare with SonarQube

After manual calculations:
1. Find the same metrics in SonarQube
2. Compare your calculations
3. Understand any differences

---

## Part 3: Fix and Improve

### Step 1: Review the Refactored Code

Open `good_etl_pipeline.py` and observe improvements:

**Architecture Changes:**
- ✅ Separated concerns into distinct classes
- ✅ Used dependency injection
- ✅ Environment variables for sensitive data
- ✅ Comprehensive error handling
- ✅ Type hints throughout

**Security Fixes:**
- ✅ No hardcoded credentials
- ✅ Parameterized SQL queries
- ✅ No eval() usage
- ✅ SSL verification enabled
- ✅ Safe file operations

**Code Quality Improvements:**
- ✅ Eliminated duplication (DRY principle)
- ✅ Reduced complexity (single responsibility)
- ✅ Proper logging instead of print
- ✅ Comprehensive docstrings
- ✅ Clean code structure

### Step 2: Review the Test Suite

Open `test_good_etl_pipeline.py` to see:

**Testing Best Practices:**
- ✅ Fixtures for reusable test data
- ✅ Mocking external dependencies
- ✅ Testing edge cases (None, empty data)
- ✅ Testing error conditions
- ✅ Integration tests
- ✅ Clear test names and docstrings

**Coverage Areas:**
- All classes and methods
- Happy paths and error paths
- Edge cases and boundary conditions
- Integration scenarios

### Step 3: Run Tests with Coverage

```bash
# Run tests with coverage report
pytest test_good_etl_pipeline.py \
  --cov=good_etl_pipeline \
  --cov-report=xml \
  --cov-report=term \
  --cov-report=html

# View detailed coverage report
# Open htmlcov/index.html in your browser
```

**Expected Results:**
- ✅ All tests pass
- ✅ Coverage >80% (target: >90%)
- ✅ Branch coverage reported

### Step 4: Analyze Refactored Code in SonarQube

```bash
# Run SonarQube scanner on the good code with tests
sonar-scanner \
  -Dsonar.projectKey=good-etl-pipeline \
  -Dsonar.projectName="Good ETL Pipeline" \
  -Dsonar.sources=good_etl_pipeline.py \
  -Dsonar.tests=test_good_etl_pipeline.py \
  -Dsonar.python.coverage.reportPaths=coverage.xml \
  -Dsonar.python.version=3.9 \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=YOUR_TOKEN_HERE
```

### Step 5: Compare Metrics

Navigate to both projects in SonarQube:
- http://localhost:9000/dashboard?id=bad-etl-pipeline
- http://localhost:9000/dashboard?id=good-etl-pipeline

**Create a comparison table in your worksheet:**

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Bugs | ? | ? | ? |
| Vulnerabilities | ? | ? | ? |
| Code Smells | ? | ? | ? |
| Coverage | 0% | ?% | ?% |
| Duplication | ?% | ?% | ?% |
| Complexity | ? | ? | ? |

### Step 6: Verify Quality Gate

Check that the refactored code passes the quality gate:

**Quality Gate Conditions (default):**
- ✅ No new bugs
- ✅ No new vulnerabilities
- ✅ No new security hotspots
- ✅ Coverage on new code ≥ 80%
- ✅ Duplication on new code < 3%
- ✅ Maintainability rating = A

---

## Key Metrics Explained

### Cyclomatic Complexity
- **What:** Number of linearly independent paths through code
- **Range:** 1 (simple) to ∞ (complex)
- **Good:** ≤10
- **Refactor when:** >15

### Cognitive Complexity
- **What:** How difficult code is to understand
- **Good:** ≤15
- **Refactor when:** >25

### Code Duplication
- **What:** Percentage of duplicated code
- **Good:** <3%
- **Acceptable:** <5%
- **Poor:** >10%

### Code Coverage
- **What:** Percentage of code executed by tests
- **Minimum:** 60%
- **Good:** 80%
- **Excellent:** >90%

---


## Bonus Challenges

If you finish early, try these:

### Challenge 1: Achieve 95% Coverage
Add more tests to `test_good_etl_pipeline.py` to reach 95% coverage

### Challenge 2: Add New Feature
Add a new data validation rule with tests:
- Implement validation for product names
- Write tests for the new validation
- Ensure coverage stays >80%

