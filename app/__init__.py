from flask import Flask
from app.database.database import db_session, init_db

def create_app():
    # create and configure the app
    app = Flask(__name__)

    from .routes import voice_routes
    app.register_blueprint(voice_routes.bp)

    from .data_service import data_service
    from .models.data_request_object import FrameData, ConfigParams

    init_db()

    return app
