---
type: Section
title: Best Practices
chapter: E2E Testing for Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/e2e-testing.md
tags: [guide, section]
---

### 1. Keep Tests Focused
One user flow per test. If a test does multiple things, split it.

### 2. Use Descriptive Names
```java
@DisplayName("Guest checkout completes with confirmation number")
void completeGuestCheckoutFlow() { }
```

### 3. Fail Fast with URL Validation
Page objects validate URLs in constructors to catch navigation errors immediately.

### 4. Prefer Explicit Waits
```java
// ✅ GOOD: Wait for specific element
waitFor("product-card-container");

// ❌ BAD: Arbitrary sleep
Thread.sleep(1000);
```

### 5. Test Only Critical Paths
E2E tests are expensive. Reserve them for:
- Happy path user journeys
- Critical business flows
- Cross-context integration

### 6. Run Headless in CI
```bash
./gradlew test-e2e -De2e.headless=true
```

---
