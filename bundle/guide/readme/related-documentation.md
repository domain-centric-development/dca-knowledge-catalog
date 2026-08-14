---
type: Section
title: Related Documentation
chapter: Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/README.md
tags: [guide, section]
---

This document describes the core Domain-Centric Architecture patterns and principles. For specific topics, see:

### Reference Implementation
- **[AI Architecture Sample](https://github.com/chbloemer/ai-architecture-sample)** - Complete reference implementation in Java/Spring Boot demonstrating all concepts in practice

> **📝 Note on Examples:** This documentation uses **generic examples** (Order, Customer, Inventory contexts) for educational clarity. The actual reference implementation uses **Product Catalog**, **Shopping Cart**, and **Portal** contexts. Both approaches are valid - use examples that match your domain. Package names shown as `com.company.project.*` are placeholders; the reference implementation uses `de.sample.aiarchitecture.*`

### Supplementary Documentation
- **[Clean Architecture Comparison](/guide/clean-architecture-comparison.md)** - Differences from Clean Architecture and when to use each
- **[Deployment Patterns](/guide/deployment-patterns.md)** - Self-Contained Systems, service decomposition, and deployment strategies
- **[Spring Modulith Implementation](/guide/spring-modulith.md)** - Practical implementation using Spring Modulith framework
- **[Team Topologies Integration](/guide/team-topologies.md)** - Organizational patterns and team structure alignment
- **[ArchUnit Governance](/guide/archunit-governance.md)** - Automated architecture testing and enforcement
- **[Domain Services with Data Dependencies](/guide/domain-services-with-data-dependencies.md)** - DomainGateway and Strategy/Callback patterns for Domain Services that need external data

## Related markers

- [DomainGateway](/marker/tactical/domaingateway.md)
