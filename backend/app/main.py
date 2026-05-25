from fastapi import FastAPI
import psutil

from prometheus_fastapi_instrumentator import Instrumentator

from .s3_service import upload_monitor_report
from datetime import datetime
from .database import engine
from .models import Base
from .routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cloud URL Monitor API"
)

app.include_router(router)

Instrumentator().instrument(app).expose(app)


@app.get("/")
def home():
    return {
        "message":
        "Cloud URL Monitor Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/metrics/system")
def metrics():

    return {
        "cpu": psutil.cpu_percent(),
        "memory":
        psutil.virtual_memory().percent,
        "disk":
        psutil.disk_usage('/').percent
    }

@app.post("/backup")
def backup_report():

    report = {
        "status": "healthy",
        "timestamp":
        str(datetime.now()),
        "cpu":
        psutil.cpu_percent()
    }

    return upload_monitor_report(report)