from sqlalchemy import Column, Integer, Text, JSON, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from app.db.session import Base

Base = declarative_base()

class LogConsumido(Base):
    __tablename__ = "log_consumido"

    id = Column(Integer, primary_key=True, index=True)
    cui = Column(Text, nullable=False)
    unidad_salud = Column(Integer, nullable=False)
    paciente = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    