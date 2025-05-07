from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.db.session import Base

class Organizacion(Base):
    __tablename__ = "organizaciones"

    id = Column(Integer, primary_key=True, index=True)
    unidad = Column(Integer, nullable=False, unique=True)
    departamento = Column(String(30), nullable=False)
    depencia = Column(String(50), nullable=False)
    nombre = Column(String(50), nullable=False)
    estado = Column(Boolean, nullable=False)
    