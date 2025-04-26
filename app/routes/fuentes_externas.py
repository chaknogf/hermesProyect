from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc
from app.db.session import SessionLocal
from app.models.fuentes_externas import FuenteExterna
from app.schemas.fuentes_externas import FuenteExternaCreate, FuenteExternaOut, FuenteExternaBase
from typing import List

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(prefix="/fuentes", tags=["fuentes externas"])

@router.post("/crearFuente", response_model=FuenteExternaOut)
async def crear_fuente_externa(
    fuente: FuenteExternaCreate,
    db: SQLAlchemySession = Depends(get_db)
):
    try:
        # Dump para convertir objetos Pydantic a tipos nativos (dict)
        nueva_fuente = FuenteExterna(
            nombre=fuente.nombre,
            endpoints=[e.model_dump() for e in fuente.endpoints],  # Aquí el cambio clave
            activo=fuente.activo
        )
        db.add(nueva_fuente)
        db.commit()
        db.refresh(nueva_fuente)
        return nueva_fuente
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
   

@router.get("/fuentesExternas", response_model=List[FuenteExternaOut])
async def listar_fuentes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
    db: SQLAlchemySession = Depends(get_db)
    ):
    try:
        result = db.query(FuenteExterna).order_by(desc(FuenteExterna.id)).offset(skip).limit(limit).all()
        return JSONResponse(status_code=200, content=jsonable_encoder([FuenteExternaOut.model_validate(f) for f in result]))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/fuenteExterna/{fuente_id}", response_model=FuenteExternaOut)
async def obtener_fuente(
    fuente_id: int,
    db: SQLAlchemySession = Depends(get_db)
    ):
    try:
        result = db.query(FuenteExterna).filter(FuenteExterna.id == fuente_id).first()
        return JSONResponse(status_code=200, content=jsonable_encoder(FuenteExternaOut.model_validate(result)))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/fuenteExterna/editar/{fuente_id}", response_model=FuenteExternaBase)
async def actualizar_fuente(
    fuente_id: int,
    fuente: FuenteExternaBase,
    db: SQLAlchemySession = Depends(get_db)
    ):
    try:
        result = db.query(FuenteExterna).filter(FuenteExterna.id == fuente_id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Fuente no encontrada")
        for key, value in fuente.model_dump().items():
            setattr(result, key, value)
        db.commit()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/fuenteExterna/eliminar/{fuente_id}")
async def eliminar_fuente(
    fuente_id: int,
    db: SQLAlchemySession = Depends(get_db)
    ):
    try:
        result = db.query(FuenteExterna).filter(FuenteExterna.id == fuente_id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Fuente no encontrada")
        db.delete(result)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Fuente externa eliminada exitosamente"})
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))