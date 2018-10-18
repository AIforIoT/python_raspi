from flask import (Blueprint, request)
import xmlrpc.client
from app.data_service.data_service import Data_service
from app.models.data_request_object import FrameData, ConfigParams

bp = Blueprint('voice_routes', __name__, url_prefix='/voice')

data_service = Data_service()

@bp.route('/impulse', methods=['POST'])
def get_impulse():

    data_frame = data_service.process_impulse_data(request.data)

    #EXAMPLE: PERFORM RPC REQUEST:
    rpc_server = xmlrpc.client.ServerProxy('http://localhost:8082/api')
    rpc_server.send_data_request_object(data_frame)

    return 'OK', 200
