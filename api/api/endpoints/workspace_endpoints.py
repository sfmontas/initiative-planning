from dataclasses import asdict
from typing import List
from uuid import UUID

from fastapi import HTTPException, APIRouter, Depends

from common.events.events import EventResponse
from domain.workspace_command_handlers import define_workspace, modify_workspace, find_workspace
from endpoints.iam_endpoints import user_is_authorized_for_permission, User
from endpoints.permissions import WorkspacePermissions
from endpoints.requests import WorkspaceRequest
from endpoints.responses import WorkspaceResponse

router = APIRouter()


@router.post("/workspaces",
             dependencies=[])
async def create_workspace(workspace_request: WorkspaceRequest,
                           user: User = Depends(user_is_authorized_for_permission(WorkspacePermissions.DEFINE.value))):
    workspace = await define_workspace(name=workspace_request.name, user_id=user.id)

    response = WorkspaceResponse(id=workspace.id,
                                 name=workspace.name)

    return response


@router.put("/workspaces/{workspace_id}")
async def update_workspace(workspace_id: UUID, workspace_request: WorkspaceRequest):
    workspace = await modify_workspace(workspace_id, workspace_request)

    if workspace is None:
        raise HTTPException(status_code=404, detail="Initiative not found")

    response = WorkspaceResponse(id=workspace.id,
                                 name=workspace.name)

    return response


@router.get("/workspaces/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(workspace_id: UUID):
    workspace = await find_workspace(workspace_id)

    if workspace is None:
        raise HTTPException(status_code=404, detail="Initiative not found")

    return WorkspaceResponse(id=workspace.id,
                             name=workspace.name)


@router.get("/workspaces/{workspace_id}/events", response_model=List[EventResponse])
async def get_workspace_events(workspace_id: UUID):
    workspace = await find_workspace(workspace_id)

    if workspace is None:
        raise HTTPException(status_code=404, detail="Initiative not found")

    stream = [EventResponse(**asdict(event)) for event in workspace.event_stream]

    return stream
