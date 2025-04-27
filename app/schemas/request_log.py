from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RequestLogCreate(BaseModel):
    method: str
    path: str
    status_code: int
    request_size: int = 0
    response_size: int = 0
    process_time_seconds: float = 0.0

class RequestLogResponse(RequestLogCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True