# models/patient.py

from sqlalchemy import Column, Integer, String, Date, BigInteger as Bigint, Text, JSON, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from app.db.session import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    cui = Column(Bigint, unique=True, nullable=False)
    id_fhir = Column(Text, unique=True)
    nombres = Column(Text)
    apellidos = Column(Text)
    fecha_nacimiento = Column(Date)
    genero = Column(String)
    datos_paciente = Column(JSON)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

    # Relación con otras tablas si es necesario
    # Ejemplo: vacunas = relationship("Vaccine", back_populates="patient")