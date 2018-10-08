from flask import (Blueprint, request)
from app.data_service.data_service import Data_service
import xmlrpc.client

bp = Blueprint('voice_routes', __name__, url_prefix='/voice')

data_service = Data_service()

@bp.route('/impulse', methods=['POST'])
def get_impulse():
    data_service.process_impulse_data(request.data)

    #EXAMPLE: PERFORM RPC REQUEST:
    print('dataRequest: *****************'+str(request.data))
    #rpc_server = xmlrpc.client.ServerProxy('http://localhost:8092')
    #print(rpc_server.pow(2,3))

    return 'OK', 200
