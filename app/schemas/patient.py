from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class Address(BaseModel):
    line: List[str]
    city: str
    state: str
    postalCode: str
    country: str

class Telecom(BaseModel):
    system: str
    value: str
    use: Optional[str]

class Extension(BaseModel):
    url: str
    valueString: str

class Meta(BaseModel):
    versionId: str
    lastUpdated: str

class PatientCreate(BaseModel):
    identifier: str
    fhir_id: Optional[str]
    given: Optional[str]
    family: Optional[str]
    birth_date: str
    gender: Optional[str]
    address: Optional[List[Address]]
    telecom: Optional[List[Telecom]]
    managing_organization: Optional[str]
    extension: Optional[List[Extension]]
    meta: Optional[Meta]