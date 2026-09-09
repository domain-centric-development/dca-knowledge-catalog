---
type: Pitfall
title: Default construction can bypass value validation
tags: [pitfall, tactical, value-object]
review: reviewed
owner: DCA catalog maintainers
evidence: [/marker/tactical/value.md, /rule/tactical/dca-tac-010.md]
---

A validated constructor does not protect every entry: readonly structs have a default value, and deserialisation or
reconstitution can bypass normal creation. Check representation invariants at the receiving boundary before mutation,
including an update to an existing position. Reject an invalid default with no state change or event. Reconstitution
suppresses creation events; it does not authorise invalid values. Every monetary value declares its numeric range,
currency contract and rounding. Keep those business-specific limits in the consuming system's shared specification.

## Anchors

- [Value contract](/marker/tactical/value.md)
- [Value immutability check](/rule/tactical/dca-tac-010.md)
