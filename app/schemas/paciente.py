from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


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


class ResumenClinico(BaseModel):
    unidad_salud: Optional[str]
    diagnostico: Optional[str]
    fecha: Optional[str]
    tratamiento: Optional[str]


class Metadatos(BaseModel):
    usuario: Optional[str]
    fecha_hora: Optional[str]


class PacienteSchema(BaseModel):
    id: Optional[int]  # Solo si va a usarse como schema de respuesta
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
    metadatos: Optional[List[Metadatos]]
    resumen_clinico: Optional[List[ResumenClinico]]

    @property
    def nombre_completo(self) -> str:
        """Concatenar nombres y apellidos en un solo campo."""
        nombres = filter(None, [self.primer_nombre, self.segundo_nombre])
        apellidos = filter(None, [self.primer_apellido, self.segundo_apellido])
        return " ".join(nombres) + " " + " ".join(apellidos)
    
    
    
    model_config = {
        "from_attributes": True  # Equivalente a orm_mode en Pydantic v2
    }