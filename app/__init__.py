from flask import Flask
from config import Config
from .extensions import db, migrate
from .dashboard.routes import dashboard_bp
from .stations.routes import stations_bp
from .reports.routes import reports_bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(stations_bp, url_prefix="/stations")
    app.register_blueprint(reports_bp, url_prefix="/reports")

    from . import models  # noqa: F401

    @app.context_processor
    def inject_branding():
        return {
            "app_name": "AO Smith Production Monitoring",
            "sidebar_items": [
                {"name": "Home", "endpoint": "dashboard.home", "icon": "🏠"},
                {"name": "Time Sheet", "endpoint": "reports.time_sheet", "icon": "🕒"},
                {"name": "Plan Entry", "endpoint": "reports.plan_entry", "icon": "📋"},
                {"name": "Reports", "endpoint": "reports.index", "icon": "📊"},
            ],
        }

    return app
