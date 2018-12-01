from flask import (Blueprint, request)
import xmlrpc.client
from app.data_service.data_service import Data_service
from app.database.db_service import DBService
import logging, json


bp = Blueprint('test', __name__)

data_service = Data_service()
db_service = DBService()

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


@bp.route('/get_delay_by_esp_id', methods=['GET'])
def get_delay_by_esp_id():
    esp = db_service.get_delay_by_esp_id("192.168.2.26")
    if esp is None:
        return "", 404
    else:
        return json.dumps(esp), 200
