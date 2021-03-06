from flask import Flask
from app.database.database import db_session, init_db
from app.routes import voice_routes, data_controller, test_db_endpoints
from app.data_service import data_service
from app.models.data_request_object import FrameData
import os

try:
    os.remove('/tmp/test.db')
except:
    print("Database does not exist")

app = Flask(__name__)
app.register_blueprint(voice_routes.bp)
app.register_blueprint(data_controller.bp)
app.register_blueprint(test_db_endpoints.bp)

init_db()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)