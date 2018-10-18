from flask_xmlrpcre.xmlrepcre import Fault
from rpc_api import handler


@handler.register
def hello(data_request_object):
    print("HELLO: ")
    print(data_request_object)



