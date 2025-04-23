# schemas/patient.py

from pydantic import BaseModel
from datetime import date
from typing import Optional

class PatientSchema(BaseModel):
    full_name: str
    cui: str
    birth_date: date
    address: str | None = None
    phone: str | None = None

    class Config:
        from_attributes = True

