from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import desc
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.exc import SQLAlchemyError
from app.models.consultas import Consulta
from app.schemas.consultas import ConsultaCreate, ConsultaOut
from app.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

router = APIRouter(prefix="/consultas")

@router.post("/consulta/crear/", tags=["consultas"])
def crear_consulta(
    consulta: ConsultaCreate,
    db: SQLAlchemySession = Depends(get_db)
    ):
    try:
        new_consulta = Consulta(**consulta.model_dump())
        db.add(new_consulta)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Consulta creada exitosamente"})
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/consulta/{consulta_id}", tags=["consultas"])
def obtener_consulta(
    consulta_id: int,
    db: SQLAlchemySession = Depends(get_db)
    ):
    try:
        result = db.query(Consulta).filter(Consulta.id == consulta_id).first()
        if result is None:
            raise HTTPException(status_code=404, detail=f"Consulta con id {consulta_id} no encontrada.")
        return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/consultas/", tags=["consultas"])
def listar_consultas(
    db: SQLAlchemySession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
    ):
    try:
        query = db.query(Consulta).order_by(desc(Consulta.id))

        result = query.offset(skip).limit(limit).all()

        # Si no hay resultados, devolver []
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/consulta/eliminar/{consulta_id}", tags=["consultas"])
def eliminar_consulta(
    consulta_id: int,
    db: SQLAlchemySession = Depends(get_db)
    ):
    try:
        result = db.query(Consulta).filter(Consulta.id == consulta_id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Consulta no encontrada")
        db.delete(result)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Consulta eliminada exitosamente"})
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/consulta/actualizar/{consulta_id}", tags=["consultas"])
async def actualizar_consulta(
    consulta_id: int, 
    consulta: ConsultaOut, 
    # token: str = Depends(oauth2_scheme),
    db: SQLAlchemySession = Depends(get_db)):
    try:
        db_consulta = db.query(Consulta).filter(Consulta.id == consulta_id).first()
        if db_consulta is None:
            raise HTTPException(status_code=404, detail="Consulta no encontrada")
        for key, value in consulta.model_dump().items():
            setattr(db_consulta, key, value)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Consulta actualizada exitosamente"})
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
