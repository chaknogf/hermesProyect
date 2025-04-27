# middlewares/request_monitor.py

from fastapi import Request
from sqlalchemy.orm import Session
from datetime import datetime
import time
from starlette.responses import StreamingResponse

from app.db.session import SessionLocal
from app.models.request_log import RequestLog

# Variable para llevar la cuenta diaria en memoria
daily_metrics = {}

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def monitor_and_log_requests(request: Request, call_next):
    global daily_metrics
    start_time = time.time()

    # Ignorar peticiones internas
    if request.headers.get("X-Internal-Request") == "true":
        return await call_next(request)

    request_size = 0
    try:
        if request.method not in ["GET", "HEAD", "OPTIONS"]:
            content_length = request.headers.get('content-length')
            if content_length and int(content_length) > 0:
                body = await request.body()
                request_size = len(body)
    except Exception as e:
        print(f"Error leyendo el body de la solicitud: {e}")
        request_size = 0

    response = await call_next(request)
    process_time = time.time() - start_time

    response_size = 0
    try:
        if "content-length" in response.headers:
            response_size = int(response.headers["content-length"])
    except Exception as e:
        print(f"Error accediendo a content-length: {e}")
        response_size = 0

    # Consolidar métricas como antes...
    date_key = datetime.utcnow().strftime("%Y-%m-%d")

    if date_key not in daily_metrics:
        daily_metrics[date_key] = {
            "total_requests": 0,
            "total_bytes_in": 0,
            "total_bytes_out": 0,
            "total_processing_time": 0.0
        }

    daily = daily_metrics[date_key]
    daily["total_requests"] += 1
    daily["total_bytes_in"] += request_size
    daily["total_bytes_out"] += response_size
    daily["total_processing_time"] += process_time

    db: Session = next(get_db())
    log_entry = RequestLog(
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        request_size=request_size,
        response_size=response_size,
        process_time_seconds=process_time,
    )
    db.add(log_entry)
    db.commit()

    avg_time = daily["total_processing_time"] / daily["total_requests"]
    print(f"[{date_key}] Requests: {daily['total_requests']} | "
          f"In: {daily['total_bytes_in']} bytes | Out: {daily['total_bytes_out']} bytes | "
          f"Avg Response Time: {avg_time:.4f}s")

    return response