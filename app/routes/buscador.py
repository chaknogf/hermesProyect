from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as SQLAlchemySession
from app.db.session import SessionLocal
from app.models.fuentes_externas import FuenteExterna
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.models.logs import LogConsumido
from app.schemas.logs import LogConsumidoConFuente, BuscarPacienteResult
from datetime import datetime
from typing import List
import httpx
from pydantic import Json

router = APIRouter(
    prefix="/pacientes",
    tags=["Búsqueda distribuida"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/buscar_paciente_cui/{cui}", response_model=BuscarPacienteResult)
async def buscar_paciente_por_cui(cui: str, db: SQLAlchemySession = Depends(get_db)):
    """
    Busca un paciente por CUI en todas las APIs externas activas y registra los resultados encontrados.
    """
    try:
        fuentes_consumidas = []
        # Obtener las fuentes activas de la base de datos
        fuentes = db.query(FuenteExterna).filter(FuenteExterna.activo == True).all()
        
            
        if not fuentes:
            raise HTTPException(status_code=404, detail="No hay fuentes externas activas registradas")
        fuentes_consumidas = [f.nombre for f in fuentes]
        print("Fuentes conectadas:", fuentes_consumidas)

        resultados = []
        async with httpx.AsyncClient() as client:
            for fuente in fuentes:
                try:
                    endpoint_config = fuente.endpoints[0] if isinstance(fuente.endpoints, list) else list(fuente.endpoints.values())[0]
                    headers = {"X-Internal-Request": "true"}
                    base = endpoint_config.get("base_url", "")
                    ruta = endpoint_config.get("ruta", "").replace("{valor}", cui)
                    metodo = endpoint_config.get("metodo", "GET").upper()
                    if endpoint_config.get("token"):
                        token = endpoint_config.get("token")
                        parametros = f"{cui}{token}"

                    url = f"{base.rstrip('/')}{ruta}{parametros}"
                    #print(f"URL solicitada: {url}")

                    response = await client.request(method=metodo, url=url, timeout=5.0, headers=headers)
                    print("Método:", response.request.method)
                    #print("URL usada:", str(response.request.url))
                    if response.status_code == 200:
                        pacientes = response.json()
                        if isinstance(pacientes, list) and pacientes:
                            for paciente in pacientes:
                                log = LogConsumido(
                                    cui=cui,
                                    unidad_salud=fuente.id,
                                    paciente=paciente,
                                    created_at=datetime.utcnow()
                                )
                                db.add(log)
                                db.flush()
                                
                                log_response = LogConsumidoConFuente(
                                    id=log.id,
                                    cui=log.cui,
                                    unidad_salud=log.unidad_salud,
                                    paciente=log.paciente,
                                    created_at=log.created_at,
                                    fuente_consumida=fuente.nombre
                                )
                                resultados.append(log_response.model_dump())
                except httpx.HTTPError as e:
                    print(f"Error al consultar {fuente.nombre}: {e}")

        db.commit()
        return BuscarPacienteResult(
            pacientes_encontrados=resultados
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))