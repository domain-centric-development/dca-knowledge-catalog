---
type: Section
title: The backlog contract
chapter: "Delivering a story: backlog, stages, gates"
source: guide
resource: dca-guide/process/factory.md
tags: [guide, section]
---

The backlog is markdown with front matter, one file per item, readable and reviewable without any
tooling — no database, and no JSON as the source of truth.

```text
backlog/
  <epic>/
    epic.md          the epic
    <story>.md       one story
```

An **epic** carries four mandatory fields, and a story whose epic is missing one of them is
refused before any planning starts:

| Field | Meaning |
|---|---|
| `intent` | why the epic exists — the problem, not the solution |
| `goal` | what changes for the user when it is delivered |
| `metric` | the **outcome event** that measures it (see below) |
| `domain_contact` | who answers domain questions for this epic |

This is not bureaucracy. A stage that cannot read the intent invents one, and an invented intent is
indistinguishable from a stated one once it is in the code.

A **story** names the bounded context it changes — a context the project's context map already
carries — and states its acceptance criteria as observable end-user behaviour, one per line with a
**key**:

```markdown
## Acceptance criteria

- shows-empty-state: A reader who has recorded nothing sees an invitation to start, not an error.
- lists-newest-first: The entries appear with the most recent first.

## Assumptions

- open: Does an archived entry still count towards the list?
```

The key is lowercase, hyphenated and names the behaviour. It is committed: the test stage records it
next to the test that proves it, and the gate joins the two on it. A running number would point at
nothing the moment the list is reordered.

`## Assumptions` is the asynchronous channel to the domain contact — one line per assumption, `open:`
or `answered:`. An assumption is a question, never a decision the team took itself. A story whose
criterion silently answers one of its own open assumptions is not ready; that contradiction is worth
finding before the code exists, not after.

A `status` field (`draft` / `approved` / `superseded`) carries the one thing no script can check: a
human released this story for building. The most expensive mistake is well-built wrong code.
