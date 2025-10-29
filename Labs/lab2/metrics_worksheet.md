# Metrics Analysis Worksheet

## Part 2: Calculate Metrics Manually (20 minutes)

Use this worksheet to document your findings from analyzing `bad_etl_pipeline.py`

---

### 1. Cyclomatic Complexity

**Function:** `transform_sales_data()`

**Instructions:** Count each decision point (if, for, while, and, or, etc.)

Decision points found:
1. `if data is not None:` → +1
2. `if len(data) > 0:` → +1
3. `if 'price' in data.columns:` → +1
4. `if 'quantity' in data.columns:` → +1
5. `if data['total'].sum() > 1000:` → +1
6. `if data['price'].mean() > 50:` → +1
7. `if 'discount' in data.columns:` → +1
8. `if data['discount'].mean() > 0.1:` → +1

**Your calculated Cyclomatic Complexity:** _____

**SonarQube reported Cyclomatic Complexity:** _____ (fill after analysis)

---

### 2. Code Duplication

**Instructions:** Count duplicated lines across the file

Total lines in file: _____

Lines in `transform_sales_data()`: _____
Lines in `transform_product_data()`: _____
Lines in `transform_inventory_data()`: _____

Duplicated lines: _____

**Duplication Percentage Calculation:**
```
(Duplicated Lines / Total Lines) × 100 = _____%
```

**SonarQube reported Duplication:** _____% (fill after analysis)

---

### 3. Cognitive Complexity

**Function:** `transform_sales_data()`

**Instructions:** Calculate cognitive complexity
- Each nesting level adds to complexity
- Breaks in linear flow add complexity

Nested structures found:
- Level 1: _____
- Level 2: _____
- Level 3: _____
- Level 4: _____

**Your calculated Cognitive Complexity:** _____

**SonarQube reported Cognitive Complexity:** _____ (fill after analysis)

---

### 4. Issues Count

After running SonarQube analysis, fill in the counts:

| Issue Type | Count | Severity Breakdown |
|-----------|-------|-------------------|
| **Bugs** | _____ | Critical: _____ High: _____ Medium: _____ Low: _____ |
| **Code Smells** | _____ | Critical: _____ High: _____ Medium: _____ Low: _____ |
| **Security Vulnerabilities** | _____ | Critical: _____ High: _____ Medium: _____ Low: _____ |
| **Security Hotspots** | _____ | High: _____ Medium: _____ Low: _____ |

---

### 5. Specific Issues to Document

**Security Issues:**
1. Issue: _________________________________
   - Location: Line _____
   - Description: _________________________________

2. Issue: _________________________________
   - Location: Line _____
   - Description: _________________________________

3. Issue: _________________________________
   - Location: Line _____
   - Description: _________________________________

**Code Smells:**
1. Issue: _________________________________
   - Location: Line _____
   - Description: _________________________________

2. Issue: _________________________________
   - Location: Line _____
   - Description: _________________________________

3. Issue: _________________________________
   - Location: Line _____
   - Description: _________________________________

**Bugs:**
1. Issue: _________________________________
   - Location: Line _____
   - Description: _________________________________

2. Issue: _________________________________
   - Location: Line _____
   - Description: _________________________________

---

### 6. Code Coverage (Before Refactoring)

**Test Coverage Metrics:**
- Line Coverage: _____%
- Branch Coverage: _____%
- Function Coverage: _____%

**Untested Functions:**
1. _________________________________
2. _________________________________
3. _________________________________
4. _________________________________
5. _________________________________

---

## Part 3: After Refactoring Metrics

### Comparison Table

| Metric | Before (bad_etl_pipeline.py) | After (good_etl_pipeline.py) | Improvement |
|--------|------------------------------|------------------------------|-------------|
| **Lines of Code** | _____ | _____ | _____ |
| **Cyclomatic Complexity (max)** | _____ | _____ | _____ |
| **Cognitive Complexity (max)** | _____ | _____ | _____ |
| **Code Duplication %** | _____ | _____ | _____ |
| **Security Issues** | _____ | _____ | _____ |
| **Bugs** | _____ | _____ | _____ |
| **Code Smells** | _____ | _____ | _____ |
| **Test Coverage %** | _____ | _____ | _____ |
| **Maintainability Rating** | _____ | _____ | _____ |

---

### 7. Test Coverage (After Refactoring)

**Test Coverage Metrics:**
- Line Coverage: _____%
- Branch Coverage: _____%
- Function Coverage: _____%

**Coverage Target:** >80%
**Coverage Achieved:** _____%
**Target Met:** [ ] Yes  [ ] No

---

### 8. Key Improvements Identified

List the top 5 improvements made during refactoring:

1. _________________________________
2. _________________________________
3. _________________________________
4. _________________________________
5. _________________________________

---

### 9. Lessons Learned

What are the three most important lessons from this workshop?

1. _________________________________

2. _________________________________

3. _________________________________

---

### 10. Action Items

What practices will you apply to your own projects?

1. _________________________________
2. _________________________________
3. _________________________________

---

**Completed by:** _________________
**Date:** _________________
**Total Time:** _____ minutes
