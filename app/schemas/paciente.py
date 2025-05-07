from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date, datetime

class Identificador(BaseModel):
    tipo: str
    valor: str

class Contacto(BaseModel):
    telefono: Optional[str]
    email: Optional[str]
    departamento: Optional[str]
    municipio: Optional[str]
    comunidad: Optional[str]
    direccion: Optional[str]

class Referencia(BaseModel):
    nombre: str
    parentesco: str
    telefono: Optional[str]

class DatosExtra(BaseModel):
    nacionalidad: Optional[str]
    ocupacion: Optional[str]
    idiomas: Optional[str]
    estado_civil: Optional[str]
    fecha_defuncion: Optional[date]

class resumen_clinico(BaseModel):
    unidad_salud: Optional[str]
    diagnostico: Optional[str]
    fecha: Optional[str]
    tratamiento: Optional[str]
    
class metadatos(BaseModel):
    usuario: Optional[str]
    fecha_hora: Optional[str]
    
    

class PacienteSchema(BaseModel):
    identificadores: List[Identificador]
    

    primer_nombre: Optional[str]
    segundo_nombre: Optional[str]
    primer_apellido: Optional[str]
    segundo_apellido: Optional[str]
    sexo: Optional[str]
    fecha_nacimiento: Optional[date]

    contacto: Optional[Contacto]
    referencias: Optional[List[Referencia]]
    datos_extra: Optional[DatosExtra]

    estado: Optional[str] = Field(default="A")
    metadatos: Optional[List[metadatos]]
    resumen_clinico: Optional[List[resumen_clinico]]
    
