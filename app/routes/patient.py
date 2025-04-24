from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc
from app.db.session import SessionLocal
from app.models.patient import Paciente as PacienteModel
from app.models.patient import Patient as PatientModel
from app.schemas.patient import PatientCreate as PatientSchema
from app.utils.hl7_to_fhir import hl7_to_fhir_patient as hl7_patient

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

        
@router.get("/patients/", tags=["patients"])
async def get_patients(
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
    
    
@router.post("/patient/create/", tags=["patients"])
async def create_patient(
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
    

@router.put("/patient/update/{patient_id}", tags=["patients"])
async def update_patient(
    patient_id: int, 
    patient: PatientSchema, 
    # token: str = Depends(oauth2_scheme),
    db: SQLAlchemySession = Depends(get_db)):
    try:
        db_paciente = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
        if db_paciente is None:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        for key, value in patient.model_dump().items():
            setattr(db_paciente, key, value)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Paciente actualizado exitosamente"})
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    
    
@router.delete("/patient/delet/{patient_id}", tags=["patients"])
async def delete_patient(
    patient_id: int,
    # token: str = Depends(oauth2_scheme), 
    db: SQLAlchemySession = Depends(get_db)):
    try:
        db_paciente = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
        if db_paciente is None:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        db.delete(db_paciente)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Paciente eliminado exitosamente"})
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))     
    
@router.post("/patient/hl7/", tags=["patients"])
async def message_convertion(hl7: str):
    try:
        fhir_patient = hl7_patient(hl7)
        return JSONResponse(status_code=200, content=fhir_patient.dict())
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})