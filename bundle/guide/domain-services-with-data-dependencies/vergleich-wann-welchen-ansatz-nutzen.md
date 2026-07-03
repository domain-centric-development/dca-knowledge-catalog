---
type: Section
title: "Vergleich: Wann welchen Ansatz nutzen"
chapter: Domain Services mit Datenabhängigkeiten
source: guide
resource: implementing-domain-centric-architecture/domain-services-with-data-dependencies.md
tags: [guide, section]
---

| Kriterium                        | Pure Domain Service     | DomainGateway              | Strategy/Callback          |
|----------------------------------|-------------------------|----------------------------|----------------------------|
| **Komplexität der Datenabfrage** | Einfach (1-2 Quellen)  | Mittel bis komplex         | Einfach (1 Quelle)        |
| **Abhängigkeiten im Domain**     | Keine                   | Abstraktes Interface       | Keine                      |
| **Testbarkeit**                  | Trivial                 | Mock des Gateway           | Lambda inline              |
| **Lesbarkeit**                   | Sehr gut                | Gut (explizites Interface) | Mäßig (lange Signaturen)  |
| **Wiederverwendbarkeit**         | Hoch                    | Hoch (Interface geteilt)   | Niedrig (pro Aufruf)      |
| **Anzahl Klassen**               | Minimal                 | +2 (Interface + Impl)      | Optional +1 (Func. Interf.)|
| **Domain Model Explizitheit**    | —                       | Hoch (Ubiquitous Language) | Niedrig                    |
| **Empfohlen wenn...**            | Daten vorab ladbar      | Domain entscheidet über Datenbedarf, mehrere Services nutzen gleiche Abfrage | Einzelne, einfache Abfrage bei einem Service |

### Entscheidungsbaum

```
START: Domain Service braucht Daten, die er nicht hat
   │
   ├─ Kann der Application Service alle Daten vorab laden?
   │     JA → Pure Domain Service (Default)
   │     │
   │     NEIN ↓
   │
   ├─ Entscheidet der Domain Service dynamisch, welche Daten er braucht?
   │     JA → DomainGateway Pattern
   │     │
   │     NEIN ↓
   │
   ├─ Ist es eine einzelne, einfache Datenabfrage?
   │     JA → Strategy/Callback Pattern
   │     │
   │     NEIN ↓
   │
   └─ Brauchen mehrere Domain Services die gleiche Abfrage?
         JA → DomainGateway Pattern (wiederverwendbares Interface)
         NEIN → Strategy/Callback Pattern (leichtgewichtig)
```

---

## Related markers

- [DomainGateway](/marker/tactical/domaingateway.md)
