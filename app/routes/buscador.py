import asyncio
import httpx
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
from pydantic import Json
from httpx import BasicAuth

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

class AutenticacionAPI:
    def __init__(self, tipo_autenticacion, user=None, password=None, token=None, cookies=None):
        self.tipo_autenticacion = tipo_autenticacion
        self.user = user
        self.password = password
        self.token = token
        self.cookies = cookies  
        self.timeout = httpx.Timeout(
            connect=5.0,    
            read=30.0,      
            write=5.0,      
            pool=5.0       
        )
    def obtener_headers(self):
        """
        Genera los encabezados de autenticación según el tipo.
        """
        if self.tipo_autenticacion == "basic":
            return {"Authorization": f"Basic {self._encode_basic_auth()}"}
        elif self.tipo_autenticacion == "bearer":
            return {"Authorization": f"Bearer {self.token}"}
        elif self.tipo_autenticacion == "none":
            return {}
        elif self.tipo_autenticacion == "cookie":
            return {}  # En este caso no es necesario agregar Authorization, se maneja con cookies
        else:
            raise ValueError(f"Tipo de autenticación {self.tipo_autenticacion} no soportado.")

    def _encode_basic_auth(self):
        """
        Codifica el usuario y la contraseña para autenticación básica en formato Base64.
        """
        import base64
        credentials = f"{self.user}:{self.password}"
        return base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
   
    async def hacer_solicitud(self, url, params=None):
        headers = self.obtener_headers()
        async with httpx.AsyncClient(cookies=self.cookies, timeout=self.timeout) as client:
            if self.tipo_autenticacion == "none":
                response = await client.get(url, params=params)
            else:
                response = await client.get(url, headers=headers, params=params)
        return response

@router.get("/buscar_paciente_cui/{cui}", response_model=BuscarPacienteResult)
async def buscar_paciente_por_cui(cui: str, db: SQLAlchemySession = Depends(get_db)):
    try:
        fuentes_consumidas = []
        # Obtener las fuentes activas de la base de datos
        fuentes = db.query(FuenteExterna).filter(FuenteExterna.activo == True).all()

        if not fuentes:
            raise HTTPException(status_code=404, detail="No hay fuentes externas activas registradas")
        
        fuentes_consumidas = [f.nombre for f in fuentes]
        print("Fuentes conectadas:", fuentes_consumidas)

        resultados = []

        async def consultar_fuente(fuente, cui, db, client):
            try:
                # Obtener la configuración del endpoint
                endpoint_config = fuente.endpoints[0] if isinstance(fuente.endpoints, list) else list(fuente.endpoints.values())[0]
                base = endpoint_config.get("base_url", "")
                ruta = endpoint_config.get("ruta", "").replace("VALORBUSCADO", cui)
                metodo = endpoint_config.get("metodo", "GET").upper()

                # Obtener el token, usuario y contraseña de la configuración
                token = endpoint_config.get("token")
                user = endpoint_config.get("user")
                password = endpoint_config.get("password")
                cookies = endpoint_config.get("cookies", {})  # Obtener cookies si es necesario

                # Construcción de la URL con token si es necesario
                url = f"{base.rstrip('/')}{ruta}"
                if token:
                    token = f"&{token}" if not token.startswith("&") else token
                    url += token

                # Usar la clase AutenticacionAPI para manejar la autenticación
                if cookies:
                    autenticacion = AutenticacionAPI(
                        tipo_autenticacion="cookie",  # Usar autenticación por cookies
                        cookies=cookies  # Pasar cookies a la clase
                    )
                else:
                    autenticacion = AutenticacionAPI(
                        tipo_autenticacion="basic" if user and password else "bearer" if token else "none",
                        user=user,
                        password=password,
                        token=token
                    )

                response = await autenticacion.hacer_solicitud(url)
                print(f"Headers enviados: {autenticacion.obtener_headers()}")  # Depuración para verificar los encabezados

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

                    # Log de éxito cuando se obtienen datos
                    log_exito = LogConsumido(
                        cui=cui,
                        unidad_salud=fuente.id,
                        paciente={"mensaje": f"Datos encontrados para CUI {cui} en {fuente.nombre}"},
                        created_at=datetime.utcnow()
                    )
                    db.add(log_exito)
                    db.flush()

                else:
                    # Log de error si la respuesta no es 200
                    log_error = LogConsumido(
                        cui=cui,
                        unidad_salud=fuente.id,
                        paciente={"error": response.text, "headers": dict(response.headers)},
                        created_at=datetime.utcnow()
                    )
                    db.add(log_error)
                    db.flush()
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

        # Consultar todas las fuentes en paralelo
        async with httpx.AsyncClient() as client:
            tasks = [consultar_fuente(fuente, cui, db, client) for fuente in fuentes]
            await asyncio.gather(*tasks)

        db.commit()

        print(f"Resultados encontrados: {resultados}")
        return BuscarPacienteResult(pacientes_encontrados=resultados)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))