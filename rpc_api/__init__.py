
from flaskext.xmlrpc import XMLRPCHandler

app = Flask(__name__)

handler = XMLRPCHandler('api')
handler.connect(app, '/api')