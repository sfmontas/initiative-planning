from enum import Enum
from uuid import UUID


class InitiativePermissions(Enum):
    DEFINE = UUID("b388caf0-baa3-4bd2-8e13-feb2fa7be097")


class WorkspacePermissions(Enum):
    DEFINE = UUID("2c582119-b0e9-4b5a-97a9-9930d54350c5")
