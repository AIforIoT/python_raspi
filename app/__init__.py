from flask import Flask
from app.database.database import db_session, init_db

def create_app():
    # create and configure the app
    app = Flask(__name__)

    from app.routes import voice_routes, data_controller
    app.register_blueprint(voice_routes.bp)
    app.register_blueprint(data_controller.bp)

    from app.data_service import data_service
    from app.models.data_request_object import FrameData

    init_db()

    return app

