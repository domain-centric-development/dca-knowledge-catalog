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
project/backlog/
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

A **story** names the bounded context it changes — a context the designed map already carries,
built or not yet — and states its acceptance criteria as observable end-user behaviour. Each criterion is a
scenario with a **key**, grouped under the business rule it illustrates:

```markdown
## Acceptance criteria

### Rule: An entry nobody has recorded is not an error

#### shows-empty-state (happy path)
- Given the reader has recorded nothing
- When they open the list
- Then they see an invitation to start
- And no error is shown

### Rule: The newest entry comes first

#### lists-newest-first
- Given entries recorded on Monday and on Tuesday
- When the reader opens the list
- Then Tuesday's entry is shown first

## Out of scope

- Archiving entries — a story of its own.

## Assumptions

- open: Does an archived entry still count towards the list?
```

A scenario may carry a `Title:` line under its heading; without one, its title is the key in words. The
scenario's end-to-end test carries that title verbatim as its display name, and the gate checks it: two
implementations of one story then name the test alike, and a test report names the scenario it proves.

A scenario has exactly one `When`. Two triggers are two scenarios, and every rule has at least one
scenario. A check can count both, and does. Concrete values belong in the steps, because a value is
what turns a range or a default into a question someone answers. A criterion may also be one line,
`- <key>: <criterion>`; the scenario form is what makes the gaps visible. `## Out of scope` names
what the story deliberately leaves to another, so no stage builds it on the way.

The key is lowercase, hyphenated and names the behaviour. It is committed: the test stage records it
next to the test that proves it, and the gate joins the two on it. A running number would point at
nothing the moment the list is reordered.

`## Assumptions` is the asynchronous channel to the domain contact — one line per assumption, `open:`
or `answered:`. An assumption is a question, never a decision the team took itself. A story whose
criterion silently answers one of its own open assumptions is not ready; that contradiction is worth
finding before the code exists, not after.

A `status` field (`draft` / `approved` / `superseded`) carries the one thing no script can check: a
human released this story for building. The most expensive mistake is well-built wrong code.

**A story is planned when it is written, not when it runs.** A question the story leaves open stops
the plan stage later, at the moment nobody is there to answer it. So before a story is released, the
backlog skill goes through a fixed list of questions against the story, the project description and
the code the story touches, while the person who writes it is still there:

- Does a trigger or an outcome need a way in the system does not have yet — a page, an endpoint, a
  message — and who may use it? The question asks *whether*, never *which* one to build.
- Is the story's context on the designed map, and does it need nothing the technical decisions
  exclude — a second persistence, a client framework on server-rendered pages?
- Does the story rely on an external system neither the designed map nor the technical decisions
  carry? Then it is a question about the description first, and the system's contract belongs
  there, not in every story.
- For every input: the format, the allowed range, what happens at the boundaries.
- For every default: one stated value.
- For every dependency: what the user sees when it fails, and after how long a slow answer counts
  as a failure.
- For every state a rule names: each transition, including the case where two sources of the same
  value meet.
- Which behaviour the system shows today will look different afterwards?
- Does a scenario already hold before the build? "Nothing is shown" is often true today, because
  the element does not exist yet. Such a scenario is a guarantee for the existing tests, not a
  criterion, and a gate refuses a criterion that is green before the build.
- Can a user probe or exhaust a rule by repeating it?
- Does every rule have a scenario, and does every scenario have one cause?

What the project description already answers is not asked again. What stays open becomes an `open:`
assumption, and a story whose open assumption fixes an observable result stays a draft.
