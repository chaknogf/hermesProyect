from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(title="FHIR Interop API", version="1.0.0")

@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.get("/hola")
def root():
    return {
        "mensaje": "Bienvenido a la API FHIR Interoperable 🩺",
        "estado": "operativa",
        "documentacion": "/docs"
    }