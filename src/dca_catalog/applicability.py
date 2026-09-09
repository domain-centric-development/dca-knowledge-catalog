"""Reviewed positive selector mappings. Prose mentions never create applicability.

Reviewed 2026-09-09 against each selector and implementation. Deliberately small;
add a pair only after reviewing inclusion/exclusion and both language readings.
"""
APPLIES_TO = {
    "DCA-TAC-003": ("AggregateRoot",),
    "DCA-TAC-008": ("Value",),
    "DCA-TAC-009": ("Value",),
    "DCA-TAC-010": ("Value",),
    "DCA-TAC-011": ("Value",),
    "DCA-ADV-001": ("DomainEvent",),
    "DCA-ADV-005": ("IntegrationEvent",),
    "DCA-ADV-006": ("IntegrationEvent",),
    "DCA-ADV-009": ("DomainService",),
    "DCA-ADV-010": ("DomainService",),
    "DCA-USE-001": ("InputPort",),
}
