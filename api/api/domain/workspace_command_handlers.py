from dataclasses import replace
from typing import Dict
from uuid import uuid4, UUID

from endpoints.requests import InitiativeRequest
from domain.workspace_objects import Workspace, WorkspaceDefinedBody, WorkspaceDefined, WorkspaceModifiedBody, \
    WorkspaceModified
from infrastruture.event import publish

repo: Dict[UUID, Workspace] = {}
planning_workspace_stream_name = "planning.workspace"


async def define_workspace(name: str, user_id: UUID) -> Workspace:
    workspace = Workspace(id=uuid4(), name=name)
    workspace_defined = WorkspaceDefined(aggregate_id=workspace.id,
                                         user_id=user_id,
                                         body=WorkspaceDefinedBody(id=workspace.id, name=workspace.name))

    workspace.event_stream.append(workspace_defined)
    repo[workspace.id] = workspace

    publish(planning_workspace_stream_name, workspace_defined)

    return workspace


async def find_workspace(workspace_id: UUID) -> Workspace:
    return repo.get(workspace_id)


async def modify_workspace(workspace_id: UUID, initiative_request: InitiativeRequest) -> Workspace:
    workspace = repo.get(workspace_id)

    if workspace is None:
        return None

    changes = initiative_request.dict(exclude_unset=True)
    updated_workspace = replace(workspace, **changes)

    updated_workspace.event_stream.append(WorkspaceModified(aggregate_id=workspace.id,
                                                            body=WorkspaceModifiedBody(**changes)))

    repo[updated_workspace.id] = updated_workspace

    return updated_workspace
