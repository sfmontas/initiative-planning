from dataclasses import asdict
from typing import List
from uuid import UUID

from fastapi import HTTPException, APIRouter, Depends

from common.events.events import EventResponse
from domain.initiative_command_handlers import define_initiative, modify_initiative, find_initiative
from endpoints.iam_endpoints import authorized_to_define_initiative
from endpoints.requests import InitiativeRequest
from endpoints.responses import InitiativeResponse

router = APIRouter()


@router.post("/workspace/{workspace_id}/initiatives",
             dependencies=[Depends(authorized_to_define_initiative)])
async def create_initiative(initiative_request: InitiativeRequest):
    initiative = await define_initiative(initiative_request)

    response = InitiativeResponse(id=initiative.id,
                                  name=initiative.name)

    return response


@router.put("/workspace/{workspace_id}/initiatives/{initiative_id}")
async def update_initiative(initiative_id: UUID, initiative_request: InitiativeRequest):
    initiative = await modify_initiative(initiative_id, initiative_request)

    if initiative is None:
        raise HTTPException(status_code=404, detail="Initiative not found")

    response = InitiativeResponse(id=initiative.id,
                                  name=initiative.name)

    return response


@router.get("/workspace/{workspace_id}/initiatives/{initiative_id}", response_model=InitiativeResponse)
async def get_initiative(initiative_id: UUID):
    initiative = await find_initiative(initiative_id)

    if initiative is None:
        raise HTTPException(status_code=404, detail="Initiative not found")

    return InitiativeResponse(id=initiative.id,
                              name=initiative.name)


@router.get("/workspace/{workspace_id}/initiatives/{initiative_id}/events", response_model=List[EventResponse])
async def get_initiative_events(initiative_id: UUID):
    initiative = await find_initiative(initiative_id)

    if initiative is None:
        raise HTTPException(status_code=404, detail="Initiative not found")

    stream = [EventResponse(**asdict(event)) for event in initiative.event_stream]

    return stream