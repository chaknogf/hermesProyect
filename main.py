from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import test_database_connection
from app.middlewares.request_monitor import monitor_and_log_requests

from app.routes.logs import router as logs_router
from app.routes.paciente import router as pacientes


app = FastAPI(title="FHIR Interop API", version="1.0.10")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Aquí registramos el middleware de monitorización
@app.middleware("http")
async def monitor_requests(request, call_next):
    return await monitor_and_log_requests(request, call_next)

app.include_router(logs_router)
app.include_router(pacientes)


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

    


test_database_connection()