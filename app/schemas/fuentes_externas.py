from pydantic import BaseModel, HttpUrl, Field
from typing import Dict, Optional
from datetime import datetime

class EndpointConfig(BaseModel):
    base_url: Optional[str] = None
    metodo: Optional[str] = "GET"
    ruta: Optional[str] = None
    token: Optional[str] = None

class FuentesExternas(BaseModel):
    id: int
    nombre: str
    activo: bool
    creado_en: datetime
class FuenteExternaBase(BaseModel):
    nombre: str
    endpoints: Optional[list[EndpointConfig]]
    activo: bool = True


class FuenteExternaCreate(FuenteExternaBase):
    pass

class FuenteExternaOut(BaseModel):
    id: int
    nombre: str
    endpoints: list[EndpointConfig]
    activo: bool
    creado_en: datetime
    
    

    

    model_config = {
        "from_attributes": True  # Equivalente a orm_mode en Pydantic v2
    }