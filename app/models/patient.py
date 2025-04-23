# models/patient.py

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.db.session import Base

class Patient(Base):
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    cui = Column(String(20), unique=True, nullable=False)
    birth_date = Column(Date, nullable=False)
    address = Column(String, nullable=True)
    phone = Column(String(20), nullable=True)

    # Relación con otras tablas si es necesario
    # Ejemplo: vacunas = relationship("Vaccine", back_populates="patient")