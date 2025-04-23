from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc
from app.db.session import SessionLocal
from app.models.patient import Paciente as PatientModel
from app.schemas.patient import PatientSchema 
from app.utils.hl7_to_fhir import hl7_to_fhir_patient as hl7_patient

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

        
@router.get("/pacientes/", tags=["pacientes"])
async def get_pacientes(
    id = Query(None, description="ID del paciente"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
    # token: str = Depends(oauth2_scheme),
    db: SQLAlchemySession = Depends(get_db)
    ):
    try:
        query = db.query(PatientModel).order_by(desc(PatientModel.id))

        if id:
            query = query.filter(PatientModel.id == id)

        result = query.offset(skip).limit(limit).all()

        # Si no hay resultados, devolver []
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    
    
@router.post("/paciente/crear/", tags=["pacientes"])
async def create_paciente(
    paciente: PatientSchema, 
    # token: str = Depends(oauth2_scheme),
    db: SQLAlchemySession = Depends(get_db)):
    try:
        new_paciente = PatientModel(**paciente.model_dump())
        db.add(new_paciente)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Paciente creado exitosamente"})
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/paciente/actualizar/{paciente_id}", tags=["pacientes"])
async def update_paciente(
    paciente_id: int, 
    paciente: PatientSchema, 
    # token: str = Depends(oauth2_scheme),
    db: SQLAlchemySession = Depends(get_db)):
    try:
        db_paciente = db.query(PatientModel).filter(PatientModel.id == paciente_id).first()
        if db_paciente is None:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        for key, value in paciente.model_dump().items():
            setattr(db_paciente, key, value)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Paciente actualizado exitosamente"})
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    
    
@router.delete("/paciente/eliminar/{paciente_id}", tags=["pacientes"])
async def delete_paciente(
    paciente_id: int,
    # token: str = Depends(oauth2_scheme), 
    db: SQLAlchemySession = Depends(get_db)):
    try:
        db_paciente = db.query(PatientModel).filter(PatientModel.id == paciente_id).first()
        if db_paciente is None:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        db.delete(db_paciente)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Paciente eliminado exitosamente"})
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))     
    
@router.post("/paciente/hl7/", tags=["pacientes"])
async def convertir_mensaje(hl7: str):
    try:
        fhir_patient = hl7_patient(hl7)
        return JSONResponse(status_code=200, content=fhir_patient.dict())
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})