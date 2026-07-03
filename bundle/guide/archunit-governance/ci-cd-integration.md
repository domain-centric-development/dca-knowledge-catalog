---
type: Section
title: CI/CD Integration
chapter: ArchUnit Governance for Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/archunit-governance.md
tags: [guide, section]
---

### Maven Integration

ArchUnit tests run automatically with:
```bash
mvn clean verify
```

### Gradle Integration

```bash
./gradlew test
```

### GitHub Actions Example

```yaml
name: Architecture Tests

on: [push, pull_request]

jobs:
  architecture-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'
      - name: Run Architecture Tests
        run: mvn test -Dtest=*ArchitectureTest
```

### GitLab CI Example

```yaml
architecture-tests:
  stage: test
  script:
    - mvn test -Dtest=*ArchitectureTest
  only:
    - merge_requests
    - main
```

---
