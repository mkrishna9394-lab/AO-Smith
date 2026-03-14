from datetime import date
from flask import Blueprint, render_template
from sqlalchemy import func
from ..extensions import db
from ..models import Station, BatchLog, DelayLog


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def home():
    stations = (
        db.session.query(
            Station,
            func.count(func.distinct(BatchLog.id)).label("completed_batches"),
            func.count(func.distinct(DelayLog.id)).label("delay_count"),
        )
        .outerjoin(BatchLog, db.and_(BatchLog.station_id == Station.id, func.date(BatchLog.started_at) == date.today()))
        .outerjoin(DelayLog, db.and_(DelayLog.station_id == Station.id, func.date(DelayLog.started_at) == date.today()))
        .group_by(Station.id)
        .order_by(Station.station_code)
        .all()
    )
    return render_template("dashboard/home.html", stations=stations)
