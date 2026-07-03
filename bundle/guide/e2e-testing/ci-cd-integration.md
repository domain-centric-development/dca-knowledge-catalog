---
type: Section
title: CI/CD Integration
chapter: E2E Testing for Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/e2e-testing.md
tags: [guide, section]
---

### Gradle Configuration

```groovy
// build.gradle
sourceSets {
    'test-e2e' {
        java.srcDirs = ['src/test-e2e/java']
        resources.srcDirs = ['src/test-e2e/resources']
        compileClasspath += sourceSets.main.output
        runtimeClasspath += sourceSets.main.output
    }
}

task 'test-e2e'(type: Test) {
    testClassesDirs = sourceSets.'test-e2e'.output.classesDirs
    classpath = sourceSets.'test-e2e'.runtimeClasspath

    systemProperty 'e2e.baseUrl', System.getProperty('e2e.baseUrl', 'http://localhost:8080')
    systemProperty 'e2e.headless', System.getProperty('e2e.headless', 'true')
}
```

### Running Tests

```bash
# Run with defaults (headless, localhost:8080)
./gradlew test-e2e

# Run against staging environment
./gradlew test-e2e -De2e.baseUrl=https://staging.example.com

# Run with visible browser (debugging)
./gradlew test-e2e -De2e.headless=false
```

### CI Pipeline Example

```yaml
e2e-tests:
  stage: test
  services:
    - name: application:latest
      alias: app
  script:
    - ./gradlew test-e2e -De2e.baseUrl=http://app:8080 -De2e.headless=true
  artifacts:
    when: always
    paths:
      - build/reports/test-e2e/
```

---
