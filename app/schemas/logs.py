from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime

class LogConsumidoBase(BaseModel):
    cui: str
    unidad_salud: int
    paciente: Dict[str, Any]

class LogConsumidoCreate(LogConsumidoBase):
    pass

# Esta clase ahora es personalizada con fuente_consumida
class LogConsumidoResponse(BaseModel):
    id: int
    cui: str
    unidad_salud: int
    paciente: Any
    created_at: datetime
    fuente_consumida: str
    
class LogConsumidoConFuente(BaseModel):
    id: int
    cui: str
    unidad_salud: int
    paciente: Any
    created_at: datetime
    fuente_consumida: str

    class Config:
        orm_mode = True

class BuscarPacienteResult(BaseModel):
    pacientes_encontrados: List[LogConsumidoResponse]
   