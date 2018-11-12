from flask import (Blueprint, request)
import xmlrpc.client
from app.data_service.data_service import Data_service

bp = Blueprint('voice_routes', __name__)

data_service = Data_service()

timeout = None

@bp.route('/impulse', methods=['POST'])
def get_impulse():

    data_frame = data_service.process_impulse_data(request.data)

    #PERFORM RPC REQUEST:
    rpc_server = xmlrpc.client.ServerProxy('http://localhost:8082/api')
    rpc_server.send_data_request_object(data_frame)

    return 'OK', 200


@bp.route('/setUp', methods=['POST'])
def save_esp_setup_data():
    data_service.save_esp_setup_data(request.data)
    return 'OK', 200


@bp.route('/volume', methods=['POST'])
def get_volume():
    data_service.process_volume(request.data)
    return 'OK', 200


