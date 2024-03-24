from pydantic import BaseModel
from typing import Optional
from enum import Enum


class RoleType(str, Enum):
    patient = "patient"
    physician = "physician"
    pharmacist = "pharmacist"


class PersonBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    role_type: RoleType


class PersonCreate(PersonBase):
    pass


class PersonUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    role_type: Optional[RoleType] = None


class PersonRead(PersonBase):
    person_id: int
    is_returning: bool

    class Config:
        from_attributes = True
