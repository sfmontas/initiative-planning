from uuid import UUID

from pydantic.main import BaseModel


class InitiativeResponse(BaseModel):
    id: UUID
    name: str


