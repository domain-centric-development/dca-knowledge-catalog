---
type: Section
title: "Deployment & Operations"
chapter: Team Topologies Integration
source: guide
resource: dca-guide/topics/team-topologies.md
tags: [guide, section]
---

### Team Deployment Responsibilities

**Stream-Aligned Team:**
- Deploys their own bounded context
- Owns CI/CD pipeline for their context
- Independent deployment schedule
- Blue/green or canary deployments

**Platform Team:**
- Provides deployment infrastructure
- Provides CI/CD platform
- Ensures deployment self-service

**Example:**
```text
Order Team Deployment:
├── CI/CD Pipeline: TeamCity (provided by Platform)
├── Deployment: Kubernetes (provided by Platform)
├── Schedule: Independent (10+ deploys/day possible)
└── Strategy: Blue/green deployment
```

> **For deployment patterns:** See [Deployment Patterns](/guide/deployment-patterns.md)

### Monitoring & Observability

**Stream-Aligned Team:**
- Monitors their own bounded context
- Own dashboards and alerts
- On-call rotation for their context
- Domain events provide audit trail

**Platform Team:**
- Provides monitoring infrastructure
- Provides centralized logging
- Provides distributed tracing
- Self-service dashboards

**Example:**
```text
Order Team Monitoring:
├── Infrastructure: Prometheus + Grafana (Platform Team)
├── Dashboards: Custom Order metrics (Order Team)
├── Alerts: Order-specific thresholds (Order Team)
└── On-call: Order Team rotation
```
