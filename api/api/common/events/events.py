from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import Field
from pydantic.main import BaseModel


@dataclass()
class Event:  # TODO: Move this to it's own module
    body: Any = None
    name: Optional[str] = None  # TODO: Should not have to set to none, but failing if I don't.
    created: datetime = field(default_factory=datetime.utcnow)
    effective_date: datetime = field(default_factory=datetime.utcnow)
    user_id: Optional[UUID] = None
    aggregate_id: Optional[UUID] = None


class EventResponse(BaseModel):
    body: Any
    name: Optional[str] = None  # TODO: Should not have to set to none, but failing if I don't.
    created: datetime = Field(default_factory=datetime.utcnow)
    effective_date: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[UUID] = None
    aggregate_id: Optional[UUID] = None