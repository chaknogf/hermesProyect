from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import date, time, datetime

class ConsultaBase(BaseModel):
    organizacion_id: int
    paciente_id: int
    tipo_consulta: Optional[int] = None
    especialidad: Optional[int] = None
    servicio: Optional[str] = None
    documento: Optional[str] = None
    fecha_consulta: Optional[date] = None
    hora_consulta: Optional[time] = None

    ciclo: Optional[Dict[str, datetime]] = None
    indicadores: Optional[Dict[str, Any]] = None
    detalle_clinico: Optional[Dict[str, Any]] = None
    signos_vitales: Optional[Dict[str, Any]] = None
    ansigmas: Optional[Dict[str, Any]] = None
    antecedentes: Optional[Dict[str, Any]] = None
    ordenes: Optional[Dict[str, Any]] = None
    estudios: Optional[Dict[str, Any]] = None
    metadatos: Optional[Dict[str, Any]] = None

class ConsultaCreate(ConsultaBase):
    pass

class ConsultaOut(ConsultaBase):
    id: int
    creado_en: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)