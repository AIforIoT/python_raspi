from flask import (Blueprint, request)
import xmlrpc.client
from app.data_service.data_service import Data_service

bp = Blueprint('voice_routes', __name__, url_prefix='/voice')

data_service = Data_service()

@bp.route('/impulse', methods=['POST'])
def get_impulse():
    data_service.process_impulse_data(request.data)

    #EXAMPLE: PERFORM RPC REQUEST:
    print('dataRequest: *****************'+str(request.data))
    rpc_server = xmlrpc.client.ServerProxy('http://localhost:8082/api')
    print(rpc_server.hello("PLEASE"))

    return 'OK', 200
