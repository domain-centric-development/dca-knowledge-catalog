---
type: Reference
title: ERROR HANDLING RULES — Overview
tags: [reference]
evidence_for: /guide/rules/error-handling-rules.md
---

[Full node and context](/guide/rules/error-handling-rules.md). This is an evidence excerpt; retain the parent selection and caveats.

Every failure carries its own type, and only the adapter turns it into an answer. An expected refusal a caller
answers is thrown or returned as a case of the use case's result — one way per bounded context; every other failure
is an exception.
