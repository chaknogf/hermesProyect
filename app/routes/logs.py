from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc
from app.db.session import SessionLocal
from app.models.logs import LogConsumido
from app.schemas.logs import LogConsumidoCreate, LogConsumidoResponse
from typing import List

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        


router = APIRouter(
    prefix="/logs",
    tags=["Log de consumo"]
)

@router.post("/registrar", response_model=LogConsumidoResponse)
async def registrar_consulta(
    consumo: LogConsumidoCreate, 
    db: SQLAlchemySession = Depends(get_db)):
    try:
        new_consumo = LogConsumido(**consumo.model_dump())
        db.add(new_consumo)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Consumo registrado exitosamente"})
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/consumos", response_model=List[LogConsumidoResponse])
async def obtener_logs(
    id = Query(None, description="ID del paciente"),
    cui = Query(None, description="CUI del paciente"),
    nombre = Query(None, description="Nombre del paciente"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
    db: SQLAlchemySession = Depends(get_db)):
    try:
        query = db.query(LogConsumido).order_by(desc(LogConsumido.id))

        if id:
            query = query.filter(LogConsumido.id == id)

        if cui:
            query = query.filter(LogConsumido.cui == cui)

        if nombre:
            query = query.filter(LogConsumido.cui == nombre)

        result = query.offset(skip).limit(limit).all()

        # Si no hay resultados, devolver []
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))