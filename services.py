from typing import Dict, List

from schemas import (
    BowlerDiscipline,
    Delivery,
    DisciplineReport,
)


SCORING_RULE = (
    "The score starts at 100. "
    "Each wide delivery reduces the score by 2 points. "
    "Each no-ball delivery reduces the score by 3 points. "
    "The minimum score is 0."
)


def get_extra_value(
    extras: Dict[str, int],
    field_names: List[str]
) -> int:
    """
    Supports different names for the same extra field.
    """

    for field_name in field_names:
        if field_name in extras:
            return extras[field_name]

    return 0


def get_rating(score: float) -> str:
    if score >= 95:
        return "Excellent"

    if score >= 85:
        return "Good"

    if score >= 70:
        return "Needs improvement"

    return "Poor"


def get_recommendations(
    wide_deliveries: int,
    no_ball_deliveries: int
) -> List[str]:

    recommendations = []

    if wide_deliveries > 0:
        recommendations.append(
            "Improve line and length control to reduce wides."
        )

    if no_ball_deliveries > 0:
        recommendations.append(
            "Improve front-foot control to reduce no-balls."
        )

    if not recommendations:
        recommendations.append(
            "Excellent discipline with no wides or no-balls."
        )

    return recommendations


def calculate_discipline(
    innings_id: str,
    deliveries: List[Delivery]
) -> DisciplineReport:

    if not deliveries:
        return DisciplineReport(
            innings_id=innings_id,
            status="no_data",
            message="No deliveries were provided.",
            total_deliveries=0,
            legal_deliveries=0,
            illegal_deliveries=0,
            wide_deliveries=0,
            no_ball_deliveries=0,
            wide_runs=0,
            no_ball_runs=0,
            legal_delivery_rate=0.0,
            illegal_delivery_rate=0.0,
            discipline_score=None,
            rating="No data",
            scoring_rule=SCORING_RULE,
            recommendations=[
                "Add delivery data before calculating discipline."
            ],
            bowlers=[]
        )

    total_deliveries = len(deliveries)
    legal_deliveries = 0
    illegal_deliveries = 0
    wide_deliveries = 0
    no_ball_deliveries = 0
    wide_runs = 0
    no_ball_runs = 0

    bowler_stats: Dict[str, dict] = {}

    for delivery in deliveries:
        extras = delivery.extras

        wides = get_extra_value(
            extras,
            ["wides", "wide"]
        )

        no_balls = get_extra_value(
            extras,
            ["noballs", "no_balls", "no_ball"]
        )

        has_wide = wides > 0
        has_no_ball = no_balls > 0
        is_illegal = has_wide or has_no_ball

        if is_illegal:
            illegal_deliveries += 1
        else:
            legal_deliveries += 1

        if has_wide:
            wide_deliveries += 1
            wide_runs += wides

        if has_no_ball:
            no_ball_deliveries += 1
            no_ball_runs += no_balls

        bowler = delivery.bowler

        if bowler not in bowler_stats:
            bowler_stats[bowler] = {
                "bowler": bowler,
                "total_deliveries": 0,
                "legal_deliveries": 0,
                "illegal_deliveries": 0,
                "wide_deliveries": 0,
                "no_ball_deliveries": 0,
                "wide_runs": 0,
                "no_ball_runs": 0
            }

        stats = bowler_stats[bowler]
        stats["total_deliveries"] += 1

        if is_illegal:
            stats["illegal_deliveries"] += 1
        else:
            stats["legal_deliveries"] += 1

        if has_wide:
            stats["wide_deliveries"] += 1
            stats["wide_runs"] += wides

        if has_no_ball:
            stats["no_ball_deliveries"] += 1
            stats["no_ball_runs"] += no_balls

    legal_rate = round(
        (legal_deliveries / total_deliveries) * 100,
        2
    )

    illegal_rate = round(
        (illegal_deliveries / total_deliveries) * 100,
        2
    )

    discipline_score = max(
        0,
        100
        - (wide_deliveries * 2)
        - (no_ball_deliveries * 3)
    )

    bowlers = []

    for stats in bowler_stats.values():
        bowler_total = stats["total_deliveries"]

        bowler_illegal_rate = round(
            (stats["illegal_deliveries"] / bowler_total) * 100,
            2
        )

        bowler_score = max(
            0,
            100
            - (stats["wide_deliveries"] * 2)
            - (stats["no_ball_deliveries"] * 3)
        )

        bowlers.append(
            BowlerDiscipline(
                bowler=stats["bowler"],
                total_deliveries=stats["total_deliveries"],
                legal_deliveries=stats["legal_deliveries"],
                illegal_deliveries=stats["illegal_deliveries"],
                wide_deliveries=stats["wide_deliveries"],
                no_ball_deliveries=stats["no_ball_deliveries"],
                wide_runs=stats["wide_runs"],
                no_ball_runs=stats["no_ball_runs"],
                illegal_delivery_rate=bowler_illegal_rate,
                discipline_score=bowler_score,
                rating=get_rating(bowler_score)
            )
        )

    return DisciplineReport(
        innings_id=innings_id,
        status="success",
        message="Discipline report calculated successfully.",
        total_deliveries=total_deliveries,
        legal_deliveries=legal_deliveries,
        illegal_deliveries=illegal_deliveries,
        wide_deliveries=wide_deliveries,
        no_ball_deliveries=no_ball_deliveries,
        wide_runs=wide_runs,
        no_ball_runs=no_ball_runs,
        legal_delivery_rate=legal_rate,
        illegal_delivery_rate=illegal_rate,
        discipline_score=discipline_score,
        rating=get_rating(discipline_score),
        scoring_rule=SCORING_RULE,
        recommendations=get_recommendations(
            wide_deliveries,
            no_ball_deliveries
        ),
        bowlers=bowlers
    )
