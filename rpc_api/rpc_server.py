from flask_xmlrpcre.xmlrepcre import Fault
from rpc_api import handler


@handler.register
def hello(name="world"):
    if not name:
        raise Fault("unknown_recipient", "I need someone to greet!")
    return "Hello, %s!" % name


