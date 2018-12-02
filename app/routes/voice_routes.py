from flask import (Blueprint, request)
from app.data_service.data_service import Data_service
import logging

bp = Blueprint('voice_routes', __name__)
data_service = Data_service()

#Method to register an ESP
@bp.route('/setUp', methods=['POST'])
def save_esp_setup_data():
    data_service.save_esp_setup_data(request.data)
    return 'OK', 200

#Volume information from any registered ESP
@bp.route('/volume', methods=['POST'])
def get_volume():
    print("*********************RECEIVED!!!!!!***********")
    print(request.data)
    data_service.process_volume(request.data)
    return 'OK', 200


@bp.route('/error', methods=['POST'])
def get_volume_err():
    logging.error("ESP ERROR: "+ str(request.data))
    return 'OK', 200

