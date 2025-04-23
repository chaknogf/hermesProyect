from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import test_database_connection

from app.routes.patient import router as patient

app = FastAPI(title="FHIR Interop API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    
app.include_router(patient)

test_database_connection()