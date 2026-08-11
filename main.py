from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import DisciplineReport, DisciplineRequest
from services import calculate_discipline


app = FastAPI(
    title="Khel AI Discipline Report API",
    version="1.0.0",
    description=(
        "Measures bowling discipline using legal deliveries, "
        "illegal deliveries, wides, and no-balls."
    )
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {
        "message": "Khel AI Discipline Report API is live",
        "endpoint": "POST /discipline-report",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post(
    "/discipline-report",
    response_model=DisciplineReport
)
def create_discipline_report(
    request: DisciplineRequest
):
    return calculate_discipline(
        innings_id=request.innings_id,
        deliveries=request.deliveries
    )
