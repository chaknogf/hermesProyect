from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import test_database_connection

from app.routes.logs import router as logs_router
from app.routes.fuentes_externas import router as fuentes_externas_router
from app.routes.buscador import router as buscador_router

app = FastAPI(title="FHIR Interop API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(logs_router)
app.include_router(fuentes_externas_router)
app.include_router(buscador_router)

@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8800)

    


test_database_connection()