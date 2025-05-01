from pydantic import BaseModel, HttpUrl, Field
from typing import Dict, Optional
from datetime import datetime

class EndpointConfig(BaseModel):
    base_url: Optional[str] = None
    metodo: Optional[str] = "GET"
    ruta: Optional[str] = None
    # auth_type: Optional[str] = None
    # login_url: Optional[str] = None
    # token: Optional[str] = None
    # user: Optional[str] = None
    # password: Optional[str] = None
    # cookies: Optional[Dict[str, str]] = None
    

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
    creado_en: Optional[datetime] = datetime
    
    

    

    model_config = {
        "from_attributes": True  # Equivalente a orm_mode en Pydantic v2
    }