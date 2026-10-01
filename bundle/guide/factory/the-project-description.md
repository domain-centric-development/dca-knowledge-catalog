---
type: Section
title: The project description
chapter: "Delivering a story: backlog, stages, gates"
source: guide
resource: dca-guide/process/factory.md
tags: [guide, section]
---

Before the first story, two files describe what is to be built and a third, optional one describes
the designed cut. They are written with the person who decides, one question per heading, and nothing
in them is invented: a stage that reads an invented look builds it.

**The product** — `product.md`:

| Heading | Says |
|---|---|
| What and for whom | the product in two or three sentences, and its actors |
| Surfaces | pages, notifications, an API, a tool — and on which devices |
| How it works | the main flow across epics; where state lives and what is persisted |
| Look and feel | style direction, language, accessibility level, the styling approach |
| Qualities | security and authorisation stance, privacy, performance, availability |
| Not part of the product | what it deliberately will not do |

**The technical decisions** — `tech.md`:

| Heading | Says |
|---|---|
| Stack | language, framework and build tool |
| Frontend approach | server-rendered pages, a client application or none — and what that excludes |
| Persistence | where state is kept and how, and what the product does not use |
| Runtime | where and how it runs |
| Integrations | the external systems it talks to |
| Version policy | how dependencies are chosen and kept current |

**The designed domain** — `domain.md`:

| Part | Says |
|---|---|
| Bounded contexts | each context, its responsibility and its subdomain type (core, supporting, generic) |
| Relationships | upstream and downstream, the pattern, where the translation happens, and the reason |
| Glossary | one section per context: the terms and the operations as the people who own the domain say them, each with the word the code uses — until the context has code; then they move into its own glossary |

The glossary names **operations as well as terms**, because a verb is a modelling decision, not a
translation. A domain word can name more than one operation with a different effect: the German
*anlegen* covers *create* (the thing comes into existence) and *add* (an existing thing goes into a
collection); *löschen* covers *delete*, *cancel* and *archive* (gone, or kept with a state). Which one
the operation is says where its invariants live. A model that has to translate the word picks one of
them, and the next run may pick another;
where the glossary gives the code word, every run uses it. So the code word of an operation is decided
before the first story: the description names the operations it already knows, and the backlog skill
asks for each one a story brings.

The questions behind the domain part follow the grammar of Event Storming, without the workshop: first
the **domain events** — what happened, in the past tense, in the words of the people who own the
domain, because people agree on a fact more readily than on a procedure — then the **command** that
caused each event, the **aggregate** that accepts the command and holds the invariants, the **read
model** a person looks at to decide, the **policies** ("whenever this happens, do that") and the **hot
spots**, the questions nobody can answer yet. An event, a command and a read model each become a
glossary line; a hot spot becomes an open assumption.

Where the words can be looked up, they are looked up **per bounded context** before the question is
asked: a published standard of the context's subdomain, the vocabulary of widely used systems in that
field, and above all the operations those systems keep apart although they look alike — holding an
amount and collecting it, returning goods and refunding money. *Cancel* in a payment context and
*cancel* in an ordering context are different operations, so a lookup for the whole product finds the
wrong one. What the lookup finds is offered with its source; the people who own the domain decide. A
generic context usually adopts the field's vocabulary, a core context keeps its own and takes the
distinctions.

They hold decisions, never code design. "The client keeps the draft; the server stores what is
submitted" belongs in the product; "server-rendered pages, no client framework" in the technical
decisions; an endpoint or a package in neither.

Two failures make the description the first artefact rather than an optional one. A decision nobody
took lands in the first story that needs it. There it surfaces as a plan that stops for a human, at
the moment nobody is there to answer. And what no artefact states does not get built: a build stage
that makes the smallest change that works builds a page without a stylesheet, correctly, when no
look was stated. So the backlog skill writes no story while the product or the technical description
is missing, and it checks each new story against all three before the story is released: a context
not on the designed map, an actor or a surface the product does not have, a need the technical
decisions exclude — each is a question asked while the person is there. The stages plan and build
within the description, and a change that contradicts it is a review finding.

The project instructions name the three files and bind every implementation to them — a stage of the
factory, and a person developing by hand in a session alike: read them first, and treat a
contradiction as a finding, not as something to fix in the code. A session has what a stage has.
