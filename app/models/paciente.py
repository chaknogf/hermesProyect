# models/patient.py

from sqlalchemy import Column, Integer, String, Date, BigInteger as Bigint, Text, JSON, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from app.db.session import Base

class PacienteModel(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    identificadores = Column(JSON, nullable=False)

    primer_nombre = Column(String(50))
    segundo_nombre = Column(String(50))
    primer_apellido = Column(String(50))
    segundo_apellido = Column(String(50))
    sexo = Column(String(2))
    fecha_nacimiento = Column(Date)

    contacto = Column(JSON)
    referencias = Column(JSON)
    datos_extra = Column(JSON)

    estado = Column(String(2), default='A')
    metadatos = Column(JSON)
    resumen_clinico = Column(JSON)
        
    