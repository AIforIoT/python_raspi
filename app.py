from flask import Flask
from flask import request
from flask import jsonify
import requests
app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'index': "PAE IoT"}), 200

@app.route('/impulse', methods=["POST"])
def treat_impulse():
    return jsonify({'impulse': request.POST.get('data')}), 200

@app.route('/voice', methods=["POST"])
def treat_voice():
    return jsonify({'voice': request.POST.get('data')}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=911)
