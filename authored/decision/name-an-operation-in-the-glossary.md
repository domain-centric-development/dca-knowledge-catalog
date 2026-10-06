---
type: Decision
title: Name an operation in the glossary — which verb, and who decides
tags: [decision, strategic, ubiquitous-language, naming, use-case, domain-event, error-handling]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules/domain-layer-rules.md, /guide/rules/application-layer-rules.md, /guide/rules/error-handling-rules.md, /guide/factory/the-project-description.md, /guide/factory/the-backlog-contract.md]
---

A story says what a person does in the words of the people who own the domain — often not the language the code is written in. A glossary that names only the nouns leaves every verb to whoever writes the code, and a verb is not a translation: one domain word can name operations with different effects. The German *anlegen* covers *create* — the thing comes into existence — and *add* — an existing thing goes into a collection; *löschen* covers *delete*, *cancel* and *archive* — gone, or kept with a state. Two implementations of the same story then name the same operation `CreateEntry` and `AddEntry`, its event `EntryCreated` and `EntryAdded`, and each is a defensible translation. Where the glossary gives the code word, they agree.

## The discriminator

Ask, for every operation a story's `When` names:

1. **What exists before the step and after it, and whose state changes?** The effect picks the verb and the aggregate. Two pairs that recur in every domain:
   - *Does the thing exist before?* If not, the operation brings it into existence — *create*, *register*, *open*, *place* — and the thing itself is the aggregate that holds the invariants from the first moment. If it does, the operation puts it somewhere — *add*, *assign*, *attach* — and the collection that receives it decides whether it may.
   - *Does the thing exist afterwards?* If not, *delete* or *remove*. If it stays with a new state — *cancel*, *archive*, *close* — the thing keeps its history, and a later step may still read or reopen it.
2. **What happened, in the past tense?** Ask for the domain event first. People who own the domain agree on a fact more readily than on a procedure, and the event's participle fixes the verb: `EntryCreated` or `EntryAdded`, `EntryDeleted` or `EntryCancelled` is the answer to question 1 in one word.
3. **And a read?** Looking at something changes nothing, so no event names it and question 2 never reaches its verb. Ask it on its own — *what do you call looking at this?* — and enter it with its code word: `ListEntries` and `ShowEntryList` are both defensible, and two runs that translate a read alone pick one each.
4. **Does the glossary already carry it?** Then use its code word, verbatim. If not, the verb is a question for the people who own the domain — not a choice for whoever writes the code, and not a translation.

## Options

### The glossary names the operation, with its code word (do this)

Enter the operation beside the term it acts on, in the domain's word and the code's word: `anlegen (create)`, `erledigen (complete)`, `leeren (clear)`, each with one line that says what it means where the language does not. Then every name follows mechanically:

- the use case is the code word plus the term: `CreateEntry`, `CompleteEntry`
- its command or query follows the use case's name
- its domain event is the term plus the past participle: `EntryCreated`, `EntryCompleted`
- a read model is named by what the person looks at to decide, and is a glossary line of its own; the verb for looking at it is an operation like the others, with its code word: `anzeigen (list)`

Decide it before the first story that needs it — in the project's description where the operation is already known, in the backlog's question pass where a story brings a new one.

### The story's prose decides

The verb is whatever the first implementation translated. Cheap the first time; afterwards every later story inherits the word, and a second implementation of the same story — another run, another team, another language — picks again. The divergence is not a defect of the model that translated; it is a gap in the input.

## Where the field already has words — per bounded context

Before the question is asked, look up how the field of **this** context names its operations: a published standard of its subdomain where one exists (healthcare, payments and logistics have them), the vocabulary of widely used systems in that field, and the operations they keep apart although they look alike. The lookup is per context, because one word names different operations in different contexts — *cancel* an authorization in a payment context, *cancel* an order in an ordering context — and a lookup for the whole product finds the wrong one.

The distinctions are the most useful finding, more than the words: where the systems of a field disagree on a word, there is no right one to adopt, but that two look-alike operations exist is exactly what a story leaves open. What the lookup finds is offered with its source; the people who own the domain decide, and nothing enters the glossary unconfirmed. A **generic** context usually adopts the field's vocabulary — it often conforms to a product it integrates; a **core** context keeps its own language and takes the distinctions.

## Failures follow the same rule

A failure is named by the rule it breaks, in the domain's words — `InsufficientStock`, `EntryAlreadyCompleted` — never by the mechanism (`InvalidInput`, `ValidationError`). The suffix is the project's choice, recorded once: `Exception` by default, as Java and .NET expect, or none where the project's language reads better without. A choice left open is picked again by every run.

## What this is not

Not a rule a dependency check can enforce: whether `create` or `add` is right is a statement about the domain, and only the people who own it can make it. Not a workshop either. The questions borrow Event Storming's grammar — domain event, command, aggregate, read model, policy, hot spot — so they can be asked in any session, by a person or a pipeline; an open hot spot is an assumption on the story, not a decision someone takes alone.

## Anchors

- Guide: [Domain layer rules](/guide/rules/domain-layer-rules.md) — glossary, operations, event names · [Application layer rules](/guide/rules/application-layer-rules.md) — use-case names · [Error handling rules](/guide/rules/error-handling-rules.md) — failure names and the suffix · [The project description](/guide/factory/the-project-description.md) · [The backlog contract](/guide/factory/the-backlog-contract.md)
- Related decisions: [Domain event or integration event](/decision/domain-event-vs-integration-event.md) · [Failure channel: exception or result](/decision/failure-channel-exception-or-result.md)
- Related pitfall: [Repository name does not match the aggregate](/pitfall/repository-name-does-not-match-aggregate.md)
