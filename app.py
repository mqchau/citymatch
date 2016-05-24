from flask import Flask, request, jsonify, send_from_directory, url_for, redirect
from rate_city import rate_city_single_core
app = Flask(__name__)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/index.html')
@app.route('/')
def send_index():
    return send_from_directory('static', 'index.html')

@app.route('/ratecity', methods = ['POST'])
def rate_city_api():

    city_char = {
        "temp_low" : int(request.form["temp_low"]),
        "temp_high" : int(request.form["temp_high"]),
        "precip" : int(request.form["precip"]),
        "settle_type": request.form["settle_type"].split(",")
    }
    occupation = request.form["occupation"]
    
    result = rate_city_single_core(occupation, city_char)
    return jsonify({"result":result})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
