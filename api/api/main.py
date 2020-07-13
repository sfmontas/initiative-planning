from dataclasses import dataclass, field, asdict, replace
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4

import uvicorn
from fastapi import FastAPI, HTTPException

from pydantic import BaseModel, Field


@dataclass()
class Event:  # TODO: Move this to it's own module
    body: Any = None
    name: Optional[str] = None  # TODO: Should not have to set to none, but failing if I don't.
    created: datetime = field(default_factory=datetime.utcnow)
    effective_date: datetime = field(default_factory=datetime.utcnow)
    user_id: Optional[UUID] = None
    aggregate_id: Optional[UUID] = None


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


class InitiativeRequest(BaseModel):
    name: Optional[str] = "New Initiative"


class InitiativeResponse(BaseModel):
    id: UUID
    name: str


class EventResponse(BaseModel):
    body: Any
    name: Optional[str] = None  # TODO: Should not have to set to none, but failing if I don't.
    created: datetime = Field(default_factory=datetime.utcnow)
    effective_date: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[UUID] = None
    aggregate_id: Optional[UUID] = None


app = FastAPI()

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


async def modify_initiative(initiative_id: UUID, initiative_request: InitiativeRequest):
    initiative = repo.get(initiative_id)

    if initiative is None:
        return None

    changes = initiative_request.dict(exclude_unset=True)
    updated_initiative = replace(initiative, **changes)

    updated_initiative.event_stream.append(InitiativeModified(aggregate_id=initiative.id,
                                                              body=InitiativeModifiedBody(**changes)))

    repo[updated_initiative.id] = updated_initiative

    return updated_initiative


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.post("/initiatives")
async def create_initiative(initiative_request: InitiativeRequest):
    initiative = await define_initiative(initiative_request)

    response = InitiativeResponse(id=initiative.id,
                                  name=initiative.name)

    return response


@app.put("/initiatives/{initiative_id}")
async def update_initiative(initiative_id: UUID, initiative_request: InitiativeRequest):
    initiative = await modify_initiative(initiative_id, initiative_request)

    if initiative is None:
        raise HTTPException(status_code=404, detail="Initiative not found")

    response = InitiativeResponse(id=initiative.id,
                                  name=initiative.name)

    return response


@app.get("/initiatives/{initiative_id}", response_model=InitiativeResponse)
async def get_initiative(initiative_id: UUID):
    initiative = await find_initiative(initiative_id)

    if initiative is None:
        raise HTTPException(status_code=404, detail="Initiative not found")

    return InitiativeResponse(id=initiative.id,
                              name=initiative.name)


@app.get("/initiatives/{initiative_id}/events", response_model=List[EventResponse])
async def get_initiative_events(initiative_id: UUID):
    initiative = await find_initiative(initiative_id)

    if initiative is None:
        raise HTTPException(status_code=404, detail="Initiative not found")

    stream = [EventResponse(**asdict(event)) for event in initiative.event_stream]

    return stream


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
