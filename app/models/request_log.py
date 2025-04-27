from sqlalchemy import Column, Integer, String, Text, BigInteger, Float, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    method = Column(String(10), nullable=False)            # GET, POST, PUT, etc.
    path = Column(Text, nullable=False)                     # Ruta solicitada
    status_code = Column(Integer, nullable=False)           # Código HTTP
    request_size = Column(BigInteger, default=0)            # Tamaño de la petición
    response_size = Column(BigInteger, default=0)           # Tamaño de la respuesta
    process_time_seconds = Column(Float, default=0.0)       # Tiempo de procesamiento
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())  # Marca temporal