import httpx
from fastapi import HTTPException
from typing import List, Dict, Any

# Lista de URLs de las APIs de los hospitales
HOSPITAL_APIS = [
    "http://hospitalA/pacientes",
    "http://hospitalSalud1/paciente",
    "http://duck/pacientes:8000"
]

async def buscar_paciente_en_apis(cui: str) -> Dict[str, Any]:
    """
    Busca si un paciente existe en las diferentes APIs de hospitales.
    
    :param cui: El CUI o ID del paciente a buscar.
    :return: Un diccionario con los resultados de las consultas a las APIs.
    """
    async with httpx.AsyncClient() as client:
        resultados = {}  # Diccionario para almacenar los resultados

        # Iterar a través de las APIs de los hospitales
        for api_url in HOSPITAL_APIS:
            try:
                # Realizar la solicitud GET para buscar el paciente en cada API
                response = await client.get(api_url, params={"cui": cui})

                # Si el paciente está registrado en la API, almacenamos la respuesta
                if response.status_code == 200:
                    resultados[api_url] = response.json()  # Guardamos la respuesta como JSON
                else:
                    # Si la respuesta no es 200, consideramos que no se encontró
                    resultados[api_url] = "Paciente no encontrado en esta base"
            except httpx.RequestError as e:
                # Si ocurre un error en la solicitud HTTP
                resultados[api_url] = f"Error al conectar con la API: {str(e)}"

        return resultados