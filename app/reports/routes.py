from datetime import date
from flask import Blueprint, jsonify, render_template, request
from sqlalchemy import func
from ..extensions import db
from ..models import Station, BatchLog, DelayLog, DelayReason


reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/")
def index():
    return render_template("reports/index.html")


@reports_bp.route("/time-sheet")
def time_sheet():
    return render_template("reports/time_sheet.html")


@reports_bp.route("/plan-entry")
def plan_entry():
    return render_template("reports/plan_entry.html")


@reports_bp.route("/api/station-report")
def station_report_api():
    station_code = request.args.get("station_code", "ST10")
    report_date = request.args.get("date", str(date.today()))

    station = Station.query.filter_by(station_code=station_code).first_or_404()

    completed_batches = (
        db.session.query(func.count(BatchLog.id))
        .filter(BatchLog.station_id == station.id, func.date(BatchLog.started_at) == report_date)
        .scalar()
    ) or 0

    delay_details = (
        db.session.query(
            DelayReason.reason_name.label("reason"),
            func.count(DelayLog.id).label("count"),
            func.sum(func.timestampdiff(db.text("MINUTE"), DelayLog.started_at, DelayLog.ended_at)).label("minutes"),
        )
        .join(DelayReason, DelayReason.id == DelayLog.reason_id)
        .filter(DelayLog.station_id == station.id, func.date(DelayLog.started_at) == report_date)
        .group_by(DelayReason.reason_name)
        .order_by(func.sum(func.timestampdiff(db.text("MINUTE"), DelayLog.started_at, DelayLog.ended_at)).desc())
        .all()
    )

    return jsonify(
        {
            "station": station.station_name,
            "station_code": station.station_code,
            "report_date": report_date,
            "completed_batches": completed_batches,
            "delay_count": sum(row.count for row in delay_details),
            "total_delay_minutes": sum((row.minutes or 0) for row in delay_details),
            "reasons": [
                {"reason": row.reason, "count": row.count, "minutes": row.minutes or 0}
                for row in delay_details
            ],
        }
    )
