from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID

from common.events.events import Event


@dataclass()
class Workspace:
    id: UUID
    name: str
    event_stream: List[Event] = field(default_factory=list)


@dataclass()
class WorkspaceDefinedBody:  # TODO: Might be better to make it a namedtuple
    id: UUID
    name: str


@dataclass()
class WorkspaceDefined(Event):
    body: WorkspaceDefinedBody = None
    name: Optional[str] = "planning.workspace.workspace-defined"


@dataclass()
class WorkspaceModifiedBody:  # TODO: Need to figure out how to set only modified properties
    name: Optional[str]


@dataclass()
class WorkspaceModified(Event):
    body: WorkspaceDefinedBody = None
    name: Optional[str] = "planning.workspace.workspace-modified"
