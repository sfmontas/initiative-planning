from dataclasses import replace
from typing import Dict
from uuid import uuid4, UUID

from endpoints.requests import InitiativeRequest
from domain.initiative_objects import Initiative, InitiativeDefinedBody, InitiativeDefined, InitiativeModifiedBody, \
    InitiativeModified

repo: Dict[UUID, Initiative] = {}


async def define_initiative(initiative_request: InitiativeRequest) -> Initiative:
    initiative = Initiative(id=uuid4(), **initiative_request.dict())
    initiative.event_stream.append(InitiativeDefined(aggregate_id=initiative.id,
                                                     body=InitiativeDefinedBody(id=initiative.id,
                                                                                name=initiative.name)))
    repo[initiative.id] = initiative

    return initiative


async def find_initiative(initiative_id: UUID) -> Initiative:
    return repo.get(initiative_id)


async def modify_initiative(initiative_id: UUID, initiative_request: InitiativeRequest) -> Initiative:
    initiative = repo.get(initiative_id)

    if initiative is None:
        return None

    changes = initiative_request.dict(exclude_unset=True)
    updated_initiative = replace(initiative, **changes)

    updated_initiative.event_stream.append(InitiativeModified(aggregate_id=initiative.id,
                                                              body=InitiativeModifiedBody(**changes)))

    repo[updated_initiative.id] = updated_initiative

    return updated_initiative
