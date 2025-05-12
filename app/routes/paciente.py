from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc, func, text
from app.db.session import SessionLocal
from app.models.paciente import PacienteModel
from app.schemas.paciente import PacienteSchema
from app.utils.hl7_to_fhir import hl7_to_fhir_patient as hl7_patient

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

        
@router.get("/pacientes/", tags=["pacientes"])
async def obtener_pacientes(
    id = Query(None, description="ID del paciente"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
    cui: str = Query(None, description="CUI del paciente"),
    nombre_completo: str = Query(None, description="Nombre completo del paciente"),
    
    # token: str = Depends(oauth2_scheme),
    db: SQLAlchemySession = Depends(get_db)
    ):
    try:
        query = db.query(PacienteModel).order_by(desc(PacienteModel.id))

        if id:
            query = query.filter(PacienteModel.id == id)

        if cui:
            query = query.filter(
                text(f"""
                EXISTS (
                    SELECT 1 FROM jsonb_array_elements(identificadores) AS elem
                    WHERE elem->>'valor' ILIKE '%{cui}%'
                )
                """)
            )
        if nombre_completo:
            nombre_completo_expr = func.concat_ws(
                ' ',
                PacienteModel.primer_nombre,
                PacienteModel.segundo_nombre,
                PacienteModel.primer_apellido,
                PacienteModel.segundo_apellido
            )
            query = query.filter(nombre_completo_expr.ilike(f"%{nombre_completo}%"))

       

        result = query.offset(skip).limit(limit).all()

        # Si no hay resultados, devolver []
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    
    
@router.post("/paciente/crear/", tags=["pacientes"])
async def crear_patient(
    paciente: PacienteSchema, 
    # token: str = Depends(oauth2_scheme),
    db: SQLAlchemySession = Depends(get_db)):
    try:
        new_paciente = PacienteModel(**paciente.model_dump())
        db.add(new_paciente)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Paciente creado exitosamente"})
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/paciente/actualizar/{paciente_id}", tags=["pacientes"])
async def actualizar_patient(
    paciente_id: int, 
    paciente: PacienteSchema, 
    # token: str = Depends(oauth2_scheme),
    db: SQLAlchemySession = Depends(get_db)):
    try:
        db_paciente = db.query(PacienteModel).filter(PacienteModel.id == paciente_id).first()
        if db_paciente is None:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        for key, value in paciente.model_dump().items():
            setattr(db_paciente, key, value)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Paciente actualizado exitosamente"})
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    
    
@router.delete("/paciente/eliminar/{paciente_id}", tags=["pacientes"])
async def eliminar_patient(
    paciente_id: int,
    # token: str = Depends(oauth2_scheme), 
    db: SQLAlchemySession = Depends(get_db)):
    try:
        db_paciente = db.query(PacienteModel).filter(PacienteModel.id == paciente_id).first()
        if db_paciente is None:
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        db.delete(db_paciente)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Paciente eliminado exitosamente"})
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))     
    
