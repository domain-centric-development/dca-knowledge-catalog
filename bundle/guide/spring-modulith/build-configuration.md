---
type: Section
title: Build Configuration
chapter: Spring Modulith Implementation
source: guide
resource: implementing-domain-centric-architecture/spring-modulith.md
tags: [guide, section]
---

### Maven

```xml
<!-- pom.xml -->
<dependencies>
    <dependency>
        <groupId>org.springframework.modulith</groupId>
        <artifactId>spring-modulith-starter-core</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.modulith</groupId>
        <artifactId>spring-modulith-starter-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.modulith</groupId>
        <artifactId>spring-modulith-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### Gradle

```groovy
dependencies {
    implementation 'org.springframework.modulith:spring-modulith-starter-core'
    implementation 'org.springframework.modulith:spring-modulith-starter-jpa'
    testImplementation 'org.springframework.modulith:spring-modulith-starter-test'
}
```
