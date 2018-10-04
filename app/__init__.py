from flask import Flask

def create_app():
    # create and configure the app
    app = Flask(__name__)

    from .routes import voice_routes
    app.register_blueprint(voice_routes.bp)

    from .data_service import data_service

    return app