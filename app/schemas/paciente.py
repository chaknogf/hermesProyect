from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class Identificador(BaseModel):
    tipo: str
    valor: str


class Contacto(BaseModel):
    telefono: Optional[str] = None
    email: Optional[str] = None
    departamento: Optional[str]  = None
    municipio: Optional[str] = None
    comunidad: Optional[str] = None
    direccion: Optional[str] = None


class Referencia(BaseModel):
    nombre: Optional[str] = None
    parentesco: Optional[str] = None
    telefono: Optional[str] = None


class DatosExtra(BaseModel):
    nacionalidad: Optional[str] = None
    ocupacion: Optional[str] = None
    idiomas: Optional[str] = None
    estado_civil: Optional[str] = None
    fecha_defuncion: Optional[date] = None


class ResumenClinico(BaseModel):
    unidad_salud: Optional[str] = None
    diagnostico: Optional[str] = None
    fecha: Optional[str] = None
    tratamiento: Optional[str] = None


class Metadatos(BaseModel):
    usuario: Optional[str] = None
    fecha_hora: Optional[str] = None


class PacienteSchema(BaseModel):
    id: Optional[int]  = None
    identificadores: List[Identificador]

    primer_nombre: Optional[str] = None
    segundo_nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    sexo: Optional[str] = None
    fecha_nacimiento: Optional[date] = None

    contacto: Optional[Contacto] = None
    referencias: Optional[List[Referencia]] = None
    datos_extra: Optional[DatosExtra] = None

    estado: Optional[str] = Field(default="A")
    metadatos: Optional[List[Metadatos]]  = None
    resumen_clinico: Optional[List[ResumenClinico]] = None

    @property
    def nombre_completo(self) -> str:
        """Concatenar nombres y apellidos en un solo campo."""
        nombres = filter(None, [self.primer_nombre, self.segundo_nombre])
        apellidos = filter(None, [self.primer_apellido, self.segundo_apellido])
        return " ".join(nombres) + " " + " ".join(apellidos)
    
    
    
    model_config = {
        "from_attributes": True  # Equivalente a orm_mode en Pydantic v2
    }