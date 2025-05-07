from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import desc
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import SessionLocal
from app.models.organizaciones import Organizacion
from app.schemas.organizaciones import OrganizacionCreate, OrganizacionOut, OrganizacionUpdate
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        


@router.post("/organizacion/crear/", tags=["organizaciones"], response_model=OrganizacionOut)
def crear_organizacion(
    org: OrganizacionCreate,
    db: SQLAlchemySession = Depends(get_db)
    ):
    try:
        new_org = Organizacion(**org.model_dump())
        db.add(new_org)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Organización creada exitosamente"})
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    


@router.get("/organizaciones/", tags=["organizaciones"], response_model=List[OrganizacionOut])
def listar_organizaciones(
    db: SQLAlchemySession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
    ):
    try:
        query = db.query(Organizacion).order_by(desc(Organizacion.id))

        result = query.offset(skip).limit(limit).all()

        # Si no hay resultados, devolver []
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/organizacion/{org_id}", tags=["organizaciones"], response_model=OrganizacionOut)
def obtener_organizacion(
    org_id: int,
    db: SQLAlchemySession = Depends(get_db)
    ):
    try:
        result = db.query(Organizacion).filter(Organizacion.id == org_id).first()
        if result is None:
            raise HTTPException(status_code=404, detail=f"Organización con id {org_id} no encontrada.")
        return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/organizacion/actualizar/{org_id}", tags=["organizaciones"], response_model=OrganizacionOut)
def actualizar_organizacion(
    org_id: int, 
    org: OrganizacionUpdate, 
    db: SQLAlchemySession = Depends(get_db)):
    try:
        db_org = db.query(Organizacion).filter(Organizacion.id == org_id).first()
        if db_org is None:
            raise HTTPException(status_code=404, detail="Organización no encontrada")
        for key, value in org.model_dump().items():
            setattr(db_org, key, value)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Organización actualizada exitosamente"})
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/organizacion/eliminar/{org_id}", tags=["organizaciones"])
def eliminar_organizacion(
    org_id: int,
    db: SQLAlchemySession = Depends(get_db)
    ):
    try:
        result = db.query(Organizacion).filter(Organizacion.id == org_id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Organización no encontrada")
        db.delete(result)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Organización eliminada exitosamente"})
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))