from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Optional, List, Dict, Callable
from uuid import UUID

from dacite import from_dict
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field

from common.events.events import Event
from config import OAUTH_SECRET_KEY, OAUTH_JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from endpoints.permissions import WorkspacePermissions, InitiativePermissions
from infrastruture.event import register_stream_handler

define_initiative_permission_id = UUID("b388caf0-baa3-4bd2-8e13-feb2fa7be097")


def workspace_defined_event_handler(event: Event):
    user = get_user_by_id(fake_users_db, event.user_id)

    if user is None:
        raise ValueError(f"Invalid user provided {event.user_id}")

    define_initiative_permission = next((permission for permission in user.permissions
                                         if define_initiative_permission_id == permission.id), None)

    if define_initiative_permission is None:
        can_define_initiative_permission = Permission(id=define_initiative_permission_id,
                                                      access_list=[AccessControlItem(id=event.aggregate_id,
                                                                                     relationship=Relationship.Single,
                                                                                     type="planning.workspace")])

        fake_users_db[user.username]["permissions"].append(can_define_initiative_permission)
    else:
        define_initiative_permission.access_list.append(AccessControlItem(id=event.aggregate_id,
                                                                          relationship=Relationship.Single,
                                                                          type="planning.workspace"))


workspace_stream_event_handlers = {
    "planning.workspace.workspace-defined": workspace_defined_event_handler

}


def workspace_stream_handler(event: Event):
    event_handler = workspace_stream_event_handlers.get(event.name)

    if event_handler is not None:
        event_handler(event)


register_stream_handler("planning.workspace", workspace_stream_handler)


class Relationship(Enum):
    Single = auto()
    Parent = auto()


@dataclass()
class AccessControlItem:
    type: str
    relationship: Relationship
    id: UUID


@dataclass()
class Permission:
    id: UUID
    access_list: Optional[List[AccessControlItem]] = Field(default_factory=list)


@dataclass()
class PermissionDefinition:
    id: UUID
    name: str


permissions_db = [
    PermissionDefinition(id="b388caf0-baa3-4bd2-8e13-feb2fa7be097", name="planning.initiative.define"),
    PermissionDefinition(id="7ea48216-2fd6-416d-a9f5-42faeda3898d", name="planning.workspace.define"),
    PermissionDefinition(id="c3ff3089-1f7d-42db-95c3-8fa558c6c153", name="planning.workspace.share"),
    PermissionDefinition(id="9e50b877-9188-4575-bf53-2a583cc8662e", name="planning.workspace.modify"),
]

fake_users_db = {
    "elvinv": {
        "id": UUID("713aec99-4f21-49d6-9996-5d083eafa9ea"),
        "username": "elvinv",
        "full_name": "Elvin Voh",
        "email": "elvinv@example.com",
        "hashed_password": "$2b$12$mNFOzbWeA9EIrTK0um5K7OlxYnRQcrB.5EtrlPFLbcRrHnF1XhPv2",
        "disabled": False,
        "permissions": [
            Permission(id=UUID("2c582119-b0e9-4b5a-97a9-9930d54350c5"))
        ]
    },
    "vivim": {
        "id": UUID("7451d72d-1a05-48c2-8f3d-f61a5fb63bfc"),
        "username": "vivim",
        "full_name": "Vivi Mo",
        "email": "vivim@example.com",
        "hashed_password": "$2b$12$mNFOzbWeA9EIrTK0um5K7OlxYnRQcrB.5EtrlPFLbcRrHnF1XhPv2",
        "disabled": False,
        "permissions": []
    }
}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


@dataclass()
class User:
    id: UUID
    username: str
    hashed_password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    permissions: List[Permission] = Field(default_factory=list)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db, username: str) -> Optional[User]:
    if username in db:
        user_dict = db[username]
        return from_dict(data_class=User, data=user_dict)

    return None


def get_user_by_id(db, user_id: UUID) -> Optional[User]:
    user_dict = next(user for user in db.values() if user.get("id") == user_id)
    if user_dict is not None:
        return from_dict(data_class=User, data=user_dict)

    return None


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, OAUTH_SECRET_KEY, algorithm=OAUTH_JWT_ALGORITHM)
    return encoded_jwt


async def user_is_authenticated(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, OAUTH_SECRET_KEY, algorithms=[OAUTH_JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=username)
    if user is None:
        raise credentials_exception
    return user


def workspace_define_permission_validator(user: User) -> bool:
    return any(permission.id == WorkspacePermissions.DEFINE.value for permission in user.permissions)


def initiative_define_permission_validator(user: User) -> bool:
    return any(permission.id == InitiativePermissions.DEFINE.value for permission in user.permissions)


permission_validators: Dict[UUID, Callable] = {
    WorkspacePermissions.DEFINE.value: workspace_define_permission_validator,
    InitiativePermissions.DEFINE.value: initiative_define_permission_validator
}


def user_is_authorized_for_permission(permission_id: UUID):
    if permission_id is None:
        raise ValueError(f"Missing Permission.")

    async def user_is_authorized(user: User = Depends(user_is_authenticated)):

        has_permission = permission_validators.get(permission_id)

        if has_permission is None or not has_permission(user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have access."
            )

        return user

    return user_is_authorized


# TODO: Might make sense to define in terms of crud vs domain (ie. switch define for create)
def authorized_to_define_initiative(workspace_id: str, user: User = Depends(user_is_authenticated)):
    define_initiative_permission = next((permission for permission in user.permissions
                                         if define_initiative_permission_id == permission.id), None)

    if define_initiative_permission is None or not any((access_item
                                                        for access_item in define_initiative_permission.access_list
                                                        if access_item.id == UUID(workspace_id))):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access."
        )

    return User


async def get_current_active_user(current_user: User = Depends(user_is_authenticated)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return UserResponse(user_name=current_user.username, )
