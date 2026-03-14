from datetime import date
from sqlalchemy import func
from ..extensions import db
from ..models import Station, BatchLog, DelayLog, DelayReason


def get_station_summary(station_code: str):
    station = Station.query.filter_by(station_code=station_code).first_or_404()

    completed_batches = (
        db.session.query(func.count(BatchLog.id))
        .filter(BatchLog.station_id == station.id, func.date(BatchLog.started_at) == date.today())
        .scalar()
    ) or 0

    delay_rows = (
        db.session.query(
            DelayReason.reason_name,
            func.count(DelayLog.id).label("delay_count"),
            func.sum(func.timestampdiff(db.text("MINUTE"), DelayLog.started_at, DelayLog.ended_at)).label("delay_minutes"),
        )
        .join(DelayReason, DelayReason.id == DelayLog.reason_id)
        .filter(DelayLog.station_id == station.id, func.date(DelayLog.started_at) == date.today())
        .group_by(DelayReason.reason_name)
        .order_by(func.sum(func.timestampdiff(db.text("MINUTE"), DelayLog.started_at, DelayLog.ended_at)).desc())
        .all()
    )

    total_delay = sum((row.delay_minutes or 0) for row in delay_rows)
    return station, completed_batches, total_delay, delay_rows
