
from flask import render_template, jsonify, Flask

app = Flask(__name__)

app.run(debug=True, host='127.0.0.1', port=5000)

@app.route('/')
def index():
    return('Привет')



@app.route('/find', methods=['POST', 'GET'])
def find():
    return jsonify(result= "it works")