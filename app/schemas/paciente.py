from typing import List, Optional
from pydantic import BaseModel

class Direccion(BaseModel):
    linea: List[str]                      # Equivalente a "line" en FHIR
    ciudad: str                           # city
    departamento: str                     # state
    codigo_postal: str                    # postalCode
    pais: str                             # country

class TelefonoCorreo(BaseModel):
    sistema: str                          # system (ej. phone, email)
    valor: str                            # value (número o dirección)
    uso: Optional[str]                    # use (ej. home, mobile)

class ExtensionFHIR(BaseModel):
    url: str                              # URL de la extensión
    valor_texto: str                      # valueString

class Metadatos(BaseModel):
    id_version: str                       # versionId
    ultima_actualizacion: str            # lastUpdated

class PacienteCrear(BaseModel):
    identificador: str                   # identifier (ej. CUI)
    id_fhir: Optional[str]               # fhir_id
    nombres: Optional[str]               # given
    apellidos: Optional[str]             # family
    fecha_nacimiento: str               # birth_date
    genero: Optional[str]                # gender
    direccion: Optional[List[Direccion]]            # address
    contacto: Optional[List[TelefonoCorreo]]        # telecom
    organizacion_gestora: Optional[str]             # managing_organization
    extensiones: Optional[List[ExtensionFHIR]]      # extension
    metadatos: Optional[Metadatos]                  # meta