from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Delivery(BaseModel):
    delivery_id: str
    bowler: str = Field(..., min_length=1)
    batter: str = Field(..., min_length=1)
    over_number: int = Field(..., ge=0)
    ball_number: int = Field(..., ge=1)
    batter_runs: int = Field(default=0, ge=0)
    extras: Dict[str, int] = Field(default_factory=dict)


class DisciplineRequest(BaseModel):
    innings_id: str = Field(..., min_length=1)
    deliveries: List[Delivery] = Field(default_factory=list)


class BowlerDiscipline(BaseModel):
    bowler: str
    total_deliveries: int
    legal_deliveries: int
    illegal_deliveries: int
    wide_deliveries: int
    no_ball_deliveries: int
    wide_runs: int
    no_ball_runs: int
    illegal_delivery_rate: float
    discipline_score: Optional[float]
    rating: str


class DisciplineReport(BaseModel):
    innings_id: str
    status: str
    message: str
    total_deliveries: int
    legal_deliveries: int
    illegal_deliveries: int
    wide_deliveries: int
    no_ball_deliveries: int
    wide_runs: int
    no_ball_runs: int
    legal_delivery_rate: float
    illegal_delivery_rate: float
    discipline_score: Optional[float]
    rating: str
    scoring_rule: str
    recommendations: List[str]
    bowlers: List[BowlerDiscipline]
