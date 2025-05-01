import asyncio
import json
import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as SQLAlchemySession
from app.db.session import SessionLocal
from app.models.fuentes_externas import FuenteExterna
from fastapi.encoders import jsonable_encoder
from app.models.logs import LogConsumido
from app.schemas.logs import LogConsumidoConFuente, BuscarPacienteResult
from datetime import datetime

router = APIRouter(prefix="/pacientes", tags=["Búsqueda distribuida"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ClienteHTTP:
    def __init__(self):
        self.timeout = httpx.Timeout(connect=5.0, read=30.0, write=5.0, pool=5.0)

    async def hacer_solicitud(self, url):
        print("\n🔍 Realizando solicitud HTTP:")
        print(f"📡 URL: {url}")
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            return await client.get(url)

@router.get("/buscar_paciente_cui/{cui}", response_model=BuscarPacienteResult)
async def buscar_paciente_por_cui(cui: str, db: SQLAlchemySession = Depends(get_db)):
    try:
        fuentes = db.query(FuenteExterna).filter(FuenteExterna.activo == True).all()
        if not fuentes:
            raise HTTPException(status_code=404, detail="No hay fuentes externas activas registradas")

        print("Fuentes conectadas:", [f.nombre for f in fuentes])
        resultados = []
        cliente = ClienteHTTP()

        async def consultar_fuente(fuente):
            try:
                raw_endpoints = fuente.endpoints
                if isinstance(raw_endpoints, str):
                    raw_endpoints = json.loads(raw_endpoints)

                if not isinstance(raw_endpoints, list):
                    raise ValueError(f"Formato de 'endpoints' no válido para {fuente.nombre}, se esperaba una lista.")

                for endpoint_config in raw_endpoints:
                    base_url = endpoint_config.get("base_url", "").replace("VALORBUSCADO", cui)
                    response = await cliente.hacer_solicitud(url=base_url)

                    if response.status_code == 200:
                        pacientes = response.json()
                        if "data" in pacientes:
                            pacientes = pacientes["data"]
                        for paciente in pacientes:
                            paciente_json = jsonable_encoder(paciente)
                            log = LogConsumido(
                                cui=cui,
                                unidad_salud=fuente.id,
                                paciente=paciente_json,
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

                        break  # salir del loop si una respuesta fue exitosa
                    else:
                        print(f"Error en la respuesta de {fuente.nombre}: {response.text}")

            except Exception as e:
                log_error = LogConsumido(
                    cui=cui,
                    unidad_salud=fuente.id,
                    paciente={"error": str(e)},
                    created_at=datetime.utcnow()
                )
                db.add(log_error)
                db.flush()
                print(f"Error al consultar {fuente.nombre}: {e}")

        tasks = [consultar_fuente(fuente) for fuente in fuentes]
        await asyncio.gather(*tasks)

        db.commit()
        print(f"Resultados encontrados: {resultados}")
        return BuscarPacienteResult(pacientes_encontrados=resultados)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))