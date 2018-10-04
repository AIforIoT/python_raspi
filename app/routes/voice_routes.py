from flask import (Blueprint, request, jsonify)
import json

bp = Blueprint('voice_routes', __name__, url_prefix='/voice')

@bp.route('/impulse', methods=['POST'])
def get_impulse():
    data_params = request.data
    jsonData = json.loads(data_params)
    esp_id = jsonData['esp_id']
    delay = jsonData['delay']
    power = jsonData['power']
    data = jsonData['data']
    print(', esp_id: '+str(esp_id)+', delay: '+str(delay)+', data: '+str(data))
    #TODO: redirect to impulse functionality
    return 'OK', 200
