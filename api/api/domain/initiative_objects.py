from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID

from common.events.events import Event


@dataclass()
class Initiative:
    id: UUID
    name: str
    event_stream: List[Event] = field(default_factory=list)


@dataclass()
class InitiativeDefinedBody:  # TODO: Might be better to make it a namedtuple
    id: UUID
    name: str


@dataclass()
class InitiativeDefined(Event):
    body: InitiativeDefinedBody = None
    name: Optional[str] = "planning.initiative.initiative-defined"


@dataclass()
class InitiativeModifiedBody:  # TODO: Need to figure out how to set only modified properties
    name: Optional[str]


@dataclass()
class InitiativeModified(Event):
    body: InitiativeDefinedBody = None
    name: Optional[str] = "planning.initiative.initiative-modified"