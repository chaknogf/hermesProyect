from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.session import Base

class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True, index=True)
    organizacion_id = Column(Integer, ForeignKey("unidades_salud.id"), nullable=False)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    tipo_consulta = Column(Integer)
    especialidad = Column(Integer)
    servicio = Column(String(50))
    documento = Column(String(20))
    fecha_consulta = Column(Date)
    hora_consulta = Column(Time)

    ciclo = Column(JSON)
    indicadores = Column(JSON)
    detalle_clinico = Column(JSON)
    signos_vitales = Column(JSON)
    ansigmas = Column(JSON)
    antecedentes = Column(JSON)
    ordenes = Column(JSON)
    estudios = Column(JSON)
    metadatos = Column(JSON)

