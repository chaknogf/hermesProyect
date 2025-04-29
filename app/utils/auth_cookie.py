# auth_cookie.py
import httpx
from typing import Optional

class AutenticadorConCookie:
    def __init__(self, login_url: str, credenciales: dict, nombre_cookie: str = "PHPSESSID"):
        self.login_url = login_url
        self.credenciales = credenciales
        self.nombre_cookie = nombre_cookie
        self.session_cookie = None

    async def autenticar(self) -> Optional[str]:
        """
        Hace login al servidor y almacena la cookie de sesión.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.login_url, data=self.credenciales)
                response.raise_for_status()

                if self.nombre_cookie in response.cookies:
                    self.session_cookie = response.cookies[self.nombre_cookie]
                    print(f"✅ Autenticado. Cookie {self.nombre_cookie} obtenida: {self.session_cookie}")
                    return self.session_cookie
                else:
                    print("⚠️ Cookie no encontrada tras login")
                    return None
            except httpx.HTTPError as e:
                print(f"❌ Error en autenticación: {e}")
                return None

    def obtener_cookie_dict(self) -> dict:
        """
        Devuelve la cookie actual en formato dict para usar con httpx.AsyncClient(cookies=...)
        """
        if self.session_cookie:
            return {self.nombre_cookie: self.session_cookie}
        return {}

    def obtener_header_cookie(self) -> dict:
        """
        Devuelve la cookie en header si se quiere usar manualmente.
        """
        if self.session_cookie:
            return {"Cookie": f"{self.nombre_cookie}={self.session_cookie}"}
        return {}
