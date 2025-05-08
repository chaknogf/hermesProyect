from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OrganizacionBase(BaseModel):
    unidad: int
    departamento: str
    dependencia: str
    nombre: str
    estado: bool


class OrganizacionCreate(OrganizacionBase):
    pass


class OrganizacionUpdate(BaseModel):
    departamento: Optional[str]
    dependencia: Optional[str]
    nombre: Optional[str]
    estado: Optional[bool]


class OrganizacionOut(OrganizacionBase):
    id: int
    created_at: datetime

   
    model_config = {
        "from_attributes": True  # Equivalente a orm_mode en Pydantic v2
    }