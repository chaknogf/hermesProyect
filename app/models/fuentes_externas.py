from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.db.session import Base


class FuenteExterna(Base):
    __tablename__ = "fuentes_externas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(Text, nullable=False)
    endpoints = Column(JSONB, nullable=False)  # Ahora es un JSONB para endpoints flexibles
    activo = Column(Boolean, default=True)
    creado_en = Column(TIMESTAMP, server_default=func.now())