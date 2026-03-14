from flask import Blueprint, render_template
from .services import get_station_summary
from ..models import Station


stations_bp = Blueprint("stations", __name__)


@stations_bp.route("/")
def index():
    stations = Station.query.order_by(Station.station_code).all()
    return render_template("stations/index.html", stations=stations)


@stations_bp.route("/<station_code>")
def detail(station_code):
    station, completed_batches, total_delay, delay_rows = get_station_summary(station_code)
    return render_template(
        "stations/detail.html",
        station=station,
        completed_batches=completed_batches,
        total_delay=total_delay,
        delay_rows=delay_rows,
    )
