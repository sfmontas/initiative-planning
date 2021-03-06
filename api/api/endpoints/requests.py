from typing import Optional

from pydantic.main import BaseModel


class InitiativeRequest(BaseModel):
    name: Optional[str] = "New Initiative"


class WorkspaceRequest(BaseModel):
    name: Optional[str] = "New Workspace"
