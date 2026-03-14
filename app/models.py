from datetime import datetime
from .extensions import db


class Station(db.Model):
    __tablename__ = "stations"

    id = db.Column(db.Integer, primary_key=True)
    station_code = db.Column(db.String(20), unique=True, nullable=False)
    station_name = db.Column(db.String(120), nullable=False)
    line_name = db.Column(db.String(50), nullable=False, default="LINE 1")
    cycle_time_set = db.Column(db.Integer, nullable=False, default=0)
    target_batches = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, default=True)

    batch_logs = db.relationship("BatchLog", backref="station", lazy=True)
    delay_logs = db.relationship("DelayLog", backref="station", lazy=True)


class DelayReason(db.Model):
    __tablename__ = "delay_reasons"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(40), unique=True, nullable=False)
    reason_name = db.Column(db.String(120), nullable=False)
    reason_group = db.Column(db.String(80), nullable=True)

    delay_logs = db.relationship("DelayLog", backref="delay_reason", lazy=True)


class BatchLog(db.Model):
    __tablename__ = "batch_logs"

    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey("stations.id"), nullable=False)
    batch_no = db.Column(db.String(50), nullable=False)
    model_name = db.Column(db.String(120), nullable=True)
    started_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="completed")


class DelayLog(db.Model):
    __tablename__ = "delay_logs"

    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey("stations.id"), nullable=False)
    reason_id = db.Column(db.Integer, db.ForeignKey("delay_reasons.id"), nullable=False)
    started_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime, nullable=False)
    remarks = db.Column(db.String(255), nullable=True)

    @property
    def delay_minutes(self):
        return round((self.ended_at - self.started_at).total_seconds() / 60, 2)
