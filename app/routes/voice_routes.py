from flask import (Blueprint, request)
from app.data_service.data_service import Data_service

bp = Blueprint('voice_routes', __name__, url_prefix='/voice')

data_service = Data_service()

@bp.route('/impulse', methods=['POST'])
def get_impulse():
    data_service.process_impulse_data(request.data)
    return 'OK', 200
