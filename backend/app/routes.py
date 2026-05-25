from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
import requests

from .database import SessionLocal
from .models import Monitor
from .schemas import URLRequest

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/monitor")
def add_url(
    data: URLRequest,
    db: Session = Depends(get_db)
):

    try:
        response = requests.get(
            data.url,
            timeout=5
        )

        status = "UP"

        response_time = (
            response.elapsed.total_seconds() * 1000
        )

        status_code = response.status_code

    except Exception:
        status = "DOWN"
        response_time = 0
        status_code = 500

    new_monitor = Monitor(
        url=data.url,
        status=status,
        status_code=status_code,
        response_time=response_time
    )

    db.add(new_monitor)
    db.commit()
    db.refresh(new_monitor)

    return new_monitor


@router.get("/monitors")
def get_urls(
    db: Session = Depends(get_db)
):
    return db.query(Monitor).all()


@router.delete("/monitor/{monitor_id}")
def delete_url(
    monitor_id: int,
    db: Session = Depends(get_db)
):

    url = db.query(Monitor).filter(
        Monitor.id == monitor_id
    ).first()

    db.delete(url)
    db.commit()

    return {
        "message": "Deleted successfully"
    }


@router.get("/analytics")
def analytics(
    db: Session = Depends(get_db)
):

    monitors = db.query(Monitor).all()

    total = len(monitors)

    healthy = len([
        m for m in monitors
        if m.status == "UP"
    ])

    failed = total - healthy

    avg_response = (
        sum(m.response_time for m in monitors)
        / total
        if total > 0 else 0
    )

    return {
        "total_urls": total,
        "healthy": healthy,
        "failed": failed,
        "average_response_time": avg_response
    }