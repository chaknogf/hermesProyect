# models/patient.py

from sqlalchemy import Column, Integer, String, Date, BigInteger as Bigint, Text, JSON, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from app.db.session import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(Text, unique=True)
    fhir_id = Column(Text, unique=True)
    given = Column(Text)
    family = Column(Text)
    birth_date = Column(Date)
    gender = Column(String)
    address = Column(JSON)
    telecom = Column(JSON)
    managing_organization = Column(Text)
    extension = Column(JSON)
    meta = Column(JSON)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relación con otras tablas si es necesario
    # Ejemplo: vacunas = relationship("Vaccine", back_populates="patient")
    
class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    identificador = Column(Text, unique=True)
    id_fhir = Column(Text, unique=True)
    nombres = Column(Text)
    apellidos = Column(Text)
    fecha_nacimiento = Column(Date)
    genero = Column(String)
    direccion = Column(JSON)
    contacto = Column(JSON)
    organizacion_gestora = Column(Text)
    extensiones = Column(JSON)
    metadatos = Column(JSON)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())