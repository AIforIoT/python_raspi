from flask import (Blueprint, request)
import xmlrpc.client
from app.data_service.data_service import Data_service
from app.database.db_service import DBService
import logging


bp = Blueprint('test', __name__)

data_service = Data_service()
db_service = DBService()

timeout = None

@bp.route('/test', methods=['GET'])
def get_impulse():

    return str(db_service.get_all_esps()), 200
