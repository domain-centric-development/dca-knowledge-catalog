---
type: Section
title: Framework annotations
chapter: Quick Reference
source: guide
resource: dca-guide/architecture/quick-reference.md
tags: [guide, section]
---

```text
Layer          | Framework annotations | Example
---------------+-----------------------+------------------------------------
Domain         | never                 | pure Java / C# only
Application    | minimal, or none      | possibly a stereotype on the use case
Adapter        | yes                   | @RestController, @Entity
Infrastructure | yes                   | @Configuration, @Bean
Shared kernel  | its domain: never       | @Nullable, own annotations
               | its adapters: yes       | the shared outbox, the transaction boundary
```
