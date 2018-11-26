from flask import (Blueprint, request)
import xmlrpc.client
from app.data_service.data_service import Data_service
from app.database.db_service import DBService
import logging


bp = Blueprint('voice_routes', __name__)

data_service = Data_service()
db_service = DBService()

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


@bp.route('/error', methods=['POST'])
def get_volume_err():
    logging.error("ESP ERROR: "+ str(request.data))
    return 'OK', 200



@bp.route('/esps', methods=['GET'])
def get_esps():
    esps = db_service.print_all_registered_esp_id()
    if not esps:
        return str(esps), 200
    else:
        return "", 404

