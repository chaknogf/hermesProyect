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
        if self.tipo_autenticacion == "basic":
            return {"Authorization": f"Basic {self._encode_basic_auth()}"}
        elif self.tipo_autenticacion == "bearer":
            return {"Authorization": f"Bearer {self.token}"}
        elif self.tipo_autenticacion in ["cookie", "login-cookie"]:
            return {}
        elif self.tipo_autenticacion == "cookie-header":
            if self.cookies and isinstance(self.cookies, dict):
                cookies_header = "; ".join(f"{k}={v}" for k, v in self.cookies.items())
                return {"Cookie": cookies_header}
            else:
                raise ValueError("Se esperaba un diccionario de cookies para autenticación tipo 'cookie-header'.")
        elif self.tipo_autenticacion == "none":
            return {}
        else:
            raise ValueError(f"Tipo de autenticación '{self.tipo_autenticacion}' no soportado.")

    def _encode_basic_auth(self):
        import base64
        credentials = f"{self.user}:{self.password}"
        return base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    async def login_y_obtener_cookies(self, login_url, login_data: dict):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(login_url, data=login_data)
            resp.raise_for_status()
            self.cookies = resp.cookies

    async def verificar_permiso(self, permiso_url: str, nombre_permiso: str) -> bool:
        url = f"{permiso_url}?SegStrNomPermiso={nombre_permiso}"
        print(f"\n🔍 Verificando permiso: {nombre_permiso} en {url}")
        async with httpx.AsyncClient(cookies=self.cookies, timeout=self.timeout) as client:
            try:
                resp = await client.get(url)
                resp.raise_for_status()
                data = resp.json()
                permisos = data.get("data", [])
                for permiso in permisos:
                    if permiso.get("SegStrNomPermiso") == nombre_permiso:
                        print(f"✅ Permiso '{nombre_permiso}' concedido")
                        return True
                print(f"❌ Permiso '{nombre_permiso}' no encontrado")
                return False
            except Exception as e:
                print(f"💥 Error al verificar permiso: {e}")
                return False

    async def hacer_solicitud(self, url, params=None, login_url=None, login_data=None):
        if self.tipo_autenticacion == "login-cookie" and login_url and login_data:
            await self.login_y_obtener_cookies(login_url, login_data)
        headers = self.obtener_headers()
        print("\n🔍 Realizando solicitud HTTP:")
        print(f"📡 URL: {url}")
        print(f"🔐 Tipo de autenticación: {self.tipo_autenticacion}")
        if self.user: print(f"👤 Usuario: {self.user}")
        if self.password: print(f"🔑 Contraseña: {'*' * len(self.password)}")
        if self.token: print(f"🪪 Token: {'***' + self.token[-8:]}")
        if self.cookies: print(f"🍪 Cookies: {self.cookies}")
        async with httpx.AsyncClient(cookies=self.cookies, timeout=self.timeout) as client:
            response = await client.get(url, headers=headers, params=params)
        return response

@router.get("/buscar_paciente_cui/{cui}", response_model=BuscarPacienteResult)
async def buscar_paciente_por_cui(cui: str, db: SQLAlchemySession = Depends(get_db)):
    try:
        fuentes = db.query(FuenteExterna).filter(FuenteExterna.activo == True).all()

        if not fuentes:
            raise HTTPException(status_code=404, detail="No hay fuentes externas activas registradas")

        print("Fuentes conectadas:", [f.nombre for f in fuentes])
        resultados = []

        async def consultar_fuente(fuente, cui, db):
            try:
                endpoint_config = fuente.endpoints[0] if isinstance(fuente.endpoints, list) else list(fuente.endpoints.values())[0]
                base = endpoint_config.get("base_url", "")
                ruta = endpoint_config.get("ruta", "").replace("VALORBUSCADO", cui)
                metodo = endpoint_config.get("metodo", "GET").upper()

                token = endpoint_config.get("token")
                user = endpoint_config.get("user")
                password = endpoint_config.get("password")
                cookies = endpoint_config.get("cookies", {})
                auth_type = endpoint_config.get("auth_type", "none")
                login_url = endpoint_config.get("login_url")
                permiso_url = endpoint_config.get("permiso_url")
                nombre_permiso = endpoint_config.get("nombre_permiso")
                login_data = {"user": user, "password": password} if auth_type == "login-cookie" else None

                url = f"{base.rstrip('/')}{ruta}"
                if token:
                    token = f"&{token}" if not token.startswith("&") else token
                    url += token

                autenticacion = AutenticacionAPI(
                    tipo_autenticacion=auth_type,
                    user=user,
                    password=password,
                    token=token,
                    cookies=cookies
                )

                if permiso_url and nombre_permiso:
                    tiene_permiso = await autenticacion.verificar_permiso(permiso_url, nombre_permiso)
                    if not tiene_permiso:
                        print(f"❌ El usuario no tiene el permiso requerido '{nombre_permiso}' para la fuente {fuente.nombre}")
                        return

                response = await autenticacion.hacer_solicitud(
                    url=url,
                    login_url=login_url,
                    login_data=login_data
                )

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

                    log_exito = LogConsumido(
                        cui=cui,
                        unidad_salud=fuente.id,
                        paciente={"mensaje": f"Datos encontrados para CUI {cui} en {fuente.nombre}"},
                        created_at=datetime.utcnow()
                    )
                    db.add(log_exito)
                    db.flush()

                else:
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

        tasks = [consultar_fuente(fuente, cui, db) for fuente in fuentes]
        await asyncio.gather(*tasks)

        db.commit()
        print(f"Resultados encontrados: {resultados}")
        return BuscarPacienteResult(pacientes_encontrados=resultados)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))