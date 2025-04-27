from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import SessionLocal
from app.models.request_log import RequestLog
from app.schemas.request_log import RequestLogResponse
from datetime import datetime, timedelta


router = APIRouter()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Endpoint para filtrar por un solo día
@router.get("/request_logs/consolidado/{date}")
def get_logs_consolidado(date: str, db: Session = Depends(get_db)):
    try:
        day_start = datetime.strptime(date, "%Y-%m-%d")
        day_end = day_start + timedelta(days=1)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Usa YYYY-MM-DD")

    # Consulta para sacar los datos consolidados
    total_requests = db.query(func.count(RequestLog.id)).filter(
        RequestLog.created_at >= day_start,
        RequestLog.created_at < day_end
    ).scalar()

    total_bytes_in = db.query(func.sum(RequestLog.request_size)).filter(
        RequestLog.created_at >= day_start,
        RequestLog.created_at < day_end
    ).scalar() or 0

    total_bytes_out = db.query(func.sum(RequestLog.response_size)).filter(
        RequestLog.created_at >= day_start,
        RequestLog.created_at < day_end
    ).scalar() or 0

    avg_process_time = db.query(func.avg(RequestLog.process_time_seconds)).filter(
        RequestLog.created_at >= day_start,
        RequestLog.created_at < day_end
    ).scalar() or 0

    max_process_time = db.query(func.max(RequestLog.process_time_seconds)).filter(
        RequestLog.created_at >= day_start,
        RequestLog.created_at < day_end
    ).scalar() or 0

    # Opcional: agrupar por métodos y códigos de estado
    methods_used = db.query(RequestLog.method, func.count(RequestLog.id)).filter(
        RequestLog.created_at >= day_start,
        RequestLog.created_at < day_end
    ).group_by(RequestLog.method).all()

    status_codes = db.query(RequestLog.status_code, func.count(RequestLog.id)).filter(
        RequestLog.created_at >= day_start,
        RequestLog.created_at < day_end
    ).group_by(RequestLog.status_code).all()

    return {
        "date": date,
        "total_requests": total_requests,
        "total_bytes_in": total_bytes_in,
        "total_bytes_out": total_bytes_out,
        "average_response_time_seconds": round(avg_process_time, 4),
        "max_response_time_seconds": round(max_process_time, 4),
        "methods_used": {method: count for method, count in methods_used},
        "status_codes": {code: count for code, count in status_codes}
    }