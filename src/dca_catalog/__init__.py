"""dca_catalog — generates an Open Knowledge Format (OKF) bundle from the
DCA reference implementation's marker interfaces, ArchUnit rules and ADRs.

The bundle is a *derived artifact*: never hand-edit ``bundle/``; edit the
source (markers / ArchUnit tests / ADRs) and re-run the generator.
"""

__version__ = "0.1.0"
