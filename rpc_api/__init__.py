from flask import Flask
from flask_xmlrpcre.xmlrepcre import XMLRPCHandler


# create and configure the app
rpc_api = Flask(__name__)

handler = XMLRPCHandler('api')
handler.connect(rpc_api, '/api')

from . import rpc_server

