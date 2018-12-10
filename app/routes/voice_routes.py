from flask import (Blueprint, request)
from app.data_service.data_service import Data_service
import logging, time

bp = Blueprint('voice_routes', __name__)
data_service = Data_service()
SET_UP_TIMER = 2.0

#Method to register an ESP
@bp.route('/setUp', methods=['POST'])
def save_esp_setup_data():
    #Wait SET_UP_TIMER time until the ESP changes state
    print(request.data.decode('utf-8'))
    time.sleep(SET_UP_TIMER)

    try:
        data_service.save_esp_setup_data(request.data)
        return 'OK', 200
    except:
        return 'Unable to register ESP', 500


#Volume information from any registered ESP
@bp.route('/volume', methods=['POST'])
def get_volume():
    print(request.data.decode("utf-8"))
    data_service.process_volume(request.data)
    return 'OK', 200


@bp.route('/error', methods=['POST'])
def get_volume_err():
    logging.error("ESP ERROR: "+ str(request.data.decode("utf-8")))
    return 'OK', 200

