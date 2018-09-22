from flask import Flask
from flask import request
from flask import jsonify
import requests
app = Flask(__name__)

@app.route('/')
def index():
    return jsonify('index': "PAE IoT"), 200

@app.route('/getip', methods=["GET"])
def get_ip():
    path = 'https://{0}:{1}/{2}'.format(request.remote_addr, "5000", "getstring")
    r = requests.get(path)
    return jsonify({'ip': request.remote_addr.to_s+" GOT you!", 'string': r.text}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
