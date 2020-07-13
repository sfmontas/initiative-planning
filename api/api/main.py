from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4

import uvicorn
from fastapi import FastAPI, HTTPException

from pydantic import BaseModel


@dataclass()
class Event:  # TODO: Move this to it's own module
    body: Any
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


class InitiativeDefined(Event):
    name: Optional[str] = "planning.initiative.initiative-defined"
    body: InitiativeDefinedBody


class InitiativeRequest(BaseModel):
    name: Optional[str] = "New Initiative"


class InitiativeResponse(BaseModel):
    id: UUID
    name: str


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


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.post("/initiatives")
async def create_initiative(initiative_request: InitiativeRequest):
    initiative = await define_initiative(initiative_request)

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
