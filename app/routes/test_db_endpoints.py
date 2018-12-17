from flask import (Blueprint , request)
from app.data_service.data_service import Data_service
from app.database.db_service import DBService
from app.processor.process_info import Info_processor
from app.models.AI_outMessage import outputMessage
from app.AI.AI_service import send_data_request_object
from app.models.ESP_data import ESP_data
import json

bp = Blueprint('test', __name__)

data_service = Data_service()
db_service = DBService()
info_processor = Info_processor()


timeout = None

@bp.route('/test_get_coordenates_by_esp_id', methods=['GET'])
def get_impulse():
    x, y = db_service.get_coordenates_by_esp_id("192.168.1.186")
    if x is None or y is None:
        return "", 404
    else:
        return json.dumps([x,y]), 200


@bp.route('/esps', methods=['GET'])
def get_esps():

    var = chr(1)
    var2 = chr(2)
    var3 = chr(19)

    varX = var+var2+var3

    print(varX)
    #print(ord(''))

    esps = db_service.get_all_esps()
    if esps is None:
        return "", 404
    else:
        return json.dumps(esps), 200


@bp.route('/get_esp_with_esp_id_different_from', methods=['GET'])
def get_esps_dif_id():
    esps = db_service.get_esp_with_esp_id_different_from("192.168.1.18")
    if esps is None:
        return "", 404
    else:
        return json.dumps(esps), 200


@bp.route('/get_esp_by_type', methods=['GET'])
def get_esp_by_type():
    esps = db_service.get_esp_by_type("bling")
    if esps is None:
        return "", 404
    else:
        return json.dumps(esps), 200


@bp.route('/get_esp_with_type_different', methods=['GET'])
def get_esp_with_type_different():
    esps = db_service.get_esp_with_type_different("light")
    if esps is None:
        return "", 404
    else:
        return json.dumps(esps), 200


@bp.route('/get_esp_by_esp_id', methods=['GET'])
def get_esp_by_esp_id():
    esp = db_service.get_delay_by_esp_id("192.168.2.26")
    if esp is None:
        return "", 404
    else:
        return json.dumps(esp), 200


@bp.route('/delete_all_volumes', methods=['GET'])
def delete_all_volumes():
    num_rows_deleted = db_service.delete_all_volumes()
    return json.dumps({'number_of_rows_deleted': num_rows_deleted}), 200


@bp.route('/get_all_volumes_by_timestamp', methods=['GET'])
def get_all_volumes_by_timestamp():
    volumes = db_service.get_all_volumes_by_timestamp("123456789")
    if volumes is None:
        return "", 404
    else:
        return json.dumps(volumes), 200


@bp.route('/get_all_volumes', methods=['GET'])
def get_all_volumes():
    volumes = db_service.get_all_volumes()
    if volumes is None:
        return "", 404
    else:
        return json.dumps(volumes), 200



@bp.route('/get_delay_by_esp_id', methods=['GET'])
def get_delay_by_esp_id():
    delay = db_service.get_delay_by_esp_id("192.168.1.24")
    if delay is None:
        return "", 404
    else:
        return json.dumps({'delay': delay}), 200


@bp.route('/get_volume_data_by_timestamp_and_volume_is_max', methods=['GET'])
def get_volume_data_by_timestamp_and_volume_is_max():
    volume = db_service.get_volume_data_by_timestamp_and_volume_is_max("123456789")
    if volume is None:
        return "", 404
    else:
        return json.dumps(volume), 200


@bp.route('/get_last_timestamp', methods=['GET'])
def get_last_timestamp():
    timestamp = db_service.get_last_timestamp()
    if timestamp is None:
        return "", 404
    else:
        return json.dumps({'last_timestamp': timestamp}), 200


@bp.route('/get_volume_data_by_timestamp_and_volume_is_different', methods=['GET'])
def get_volume_data_by_timestamp_and_volume_is_different():
    volume = db_service.get_volume_data_by_timestamp_and_volume_is_different("123456789", "192.168.1.26")
    if volume is None:
        return "", 404
    else:
        return json.dumps(volume), 200


@bp.route('/test_process_data', methods=['GET'])
def test_process_data():

    iouti = False
    status = 0
    location = False
    typeObj = 'light'

    output_message = outputMessage(iouti, status, location, typeObj)
    info_processor.process_AI_data(output_message)

    return 'OK', 200


@bp.route('/delete_all_ESPs', methods=['GET'])
def delete_all_ESPs():
    num_rows_deleted = db_service.delete_all_ESPs()
    return json.dumps({'number_of_rows_deleted': num_rows_deleted}), 200


@bp.route('/update_ESP_data', methods=['POST'])
def update_ESP_data():

    jsonData = json.loads(request.data.decode("utf-8"))
    esp_id = jsonData['esp_id']
    esp_ip = jsonData['esp_ip']
    esp_type = jsonData['esp_type']
    esp_x_axis = jsonData['esp_x_axis']
    esp_y_axis = jsonData['esp_y_axis']
    side = jsonData['side']
    location = jsonData['location']
    esp_data = ESP_data(esp_id, esp_ip, esp_x_axis, esp_y_axis, esp_type, side, location)
    db_service.update_registered_esp(esp_data)

    return 'OK', 200


@bp.route('/testAI', methods=['GET'])
def test_ai():
    print("**************************ESTIC FENT EL PUTO TEST")
    data = [10, 20]
    response = send_data_request_object(data, "192.168.5.12", 344234, 1)