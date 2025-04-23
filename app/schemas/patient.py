# schemas/patient.py

from pydantic import BaseModel
from datetime import date
from typing import Optional

class PatientSchema(BaseModel):
    cui: int 
    id_fhir: str
    nombres: str
    apellidos: str
    fecha_nacimiento: date
    genero: str
    datos_paciente: dict

    class Config:
        from_attributes = True

